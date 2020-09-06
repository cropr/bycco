# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

# all database request come in here, but we do not use dataclasess
# if needed we define extra models an do marshalling functions at the service level
# All _id are translatesd to stringified id on output
# All functions expect stringified id as input 

import logging

from datetime import datetime, date, timezone
from typing import Dict, List, Any 
from pymongo import ReturnDocument
from pymongo.errors import DuplicateKeyError
from bson import ObjectId
from ..common import RdBadRequest, RdNotFound, date2datetime
from .helpers import isactive

log = logging.getLogger('reddevil')

class PageI18nFields:

    # the fields for this class are for documentation purposes
    # they are not used in the code

    body: str
    intro: str
    title: str

class DbPage:
    COLLECTION = 'rd_page'
    DOCUMENTTYPE = 'Page'
    SIMPLEFIELDS = [ 'enabled', 'created_ts', 'doctype', 'expired_ts', 
        'modified_ts', 'publishedtime', 'name', 'slug', ]
    

    # the fields for this class are for documentation purposes
    # they are not used in the code

    component: str    # the name of the vue component that renders the page
    created_by: str
    created_ts: datetime
    doctype: str 
    enabled: bool
    expired_ts: datetime
    page_i18n_fields: Dict[str, PageI18nFields]
    id: str   
    languages: List[str] 
    name: str
    modified_by: str
    modified_ts: datetime
    published_ts: datetime
    slug: str

    @classmethod
    def create_page(cls, doc_in: dict ) -> str:
        """
        create a new page, starting form doc_in 
        """
        from ..common import db_conn
        doc_in['_id'] = doc_in.get('_id', ObjectId())
        doc_in['_documenttype'] = cls.DOCUMENTTYPE
        doc_in['created_ts'] = doc_in['modified_ts'] = datetime.now(timezone.utc)
        date2datetime(doc_in, 'published_ts')
        date2datetime(doc_in, 'expired_ts')
        try:
            db_conn[1][cls.COLLECTION].insert_one(doc_in)
        except DuplicateKeyError:
            log.exception('page with duplicate key')
            raise RdBadRequest(description="DuplicateKeyError")
        except:
            log.exception('error inserting pagedict')
            raise RdBadRequest(description="CannotInsertPage")
        return str(doc_in['_id'])

    @classmethod
    def find_pages(cls, options: dict = {}) -> List[dict]:
        """
        find all pages, 
        filtering on certain fields is enabled.
        """
        from ..common import db_conn
        pages = []
        filter: Dict[str, Any] = {}
        _fieldlist = options.pop('_fieldlist', cls.SIMPLEFIELDS)
        _order = options.pop('_order', None)
        _exists = options.pop('_exists', None)
        log.info(f'finding pages')
        if options.get('doctype'):
            filter['doctype'] = { '$in': options['doctype'].split(',')}
        if options.get('enabled'):
            filter['enabled'] = True
        if _exists:
            for f in _exists:
                filter[f] = {'$exists': True}
        projfields = {k:1 for k in _fieldlist}
        cursor = db_conn[1][cls.COLLECTION].find(filter, projection=projfields, 
            sort=_order)
        for doc in cursor:
            doc['id'] = str(doc.pop('_id'))
            pages.append(doc)
        return pages

    @classmethod
    def find_page(cls, options: dict) -> dict:
        """
        find a page, 
        if locale option is provided only show localized content
        raises NotFound if nothing is found
        """
        from ..common import db_conn
        if 'id' in options:
            try:
                options['_id'] = ObjectId(options.pop('id'))
            except:
                raise RdBadRequest(description='InvalidPageId')                
        locale =  options.pop('locale', None)
        _fieldlist = options.pop('_fieldlist', None)
        projfields = { k:1 for k in _fieldlist} if _fieldlist else None
        page = db_conn[1][cls.COLLECTION].find_one(options, projection=projfields)
        if not page:
            raise RdNotFound(description="PageNotFound")
        page['id'] = str(page.pop('_id'))
        if locale:
            page['locale'] = locale
            page.update(page.pop('page_i18n_fields', {}).get(locale, {}))
        return page

    @classmethod
    def update_page(cls, id: str, pageupdate: Dict[str, Any] ) -> dict:
        """
        update a page
        raises NotFound if page is not found
        """
        from ..common import db_conn
        try:
            oid = ObjectId(id)
        except:
            raise RdBadRequest(description="InvalidPageId")
        pageupdate['modified_ts'] = datetime.now(timezone.utc)
        date2datetime(pageupdate,'published_ts')
        date2datetime(pageupdate,'expired_ts')
        page = db_conn[1][cls.COLLECTION].find_one_and_update({'_id': oid}, 
            {'$set': pageupdate}, return_document=ReturnDocument.AFTER)
        if not page:
            raise RdNotFound(description="PageNotFound")
        page['id'] = str(page.pop('_id'))
        return page

    @classmethod
    def remove_page(cls, id: str) -> None:
        """
        delete a page 
        """
        from ..common import db_conn
        try:
            oid = ObjectId(id)
        except:
            raise RdBadRequest(description="InvalidPageId")
        rs = db_conn[1][cls.COLLECTION].delete_one({'_id': oid})
        if rs.deleted_count != 1:
            raise RdNotFound(description="PageNotFound")