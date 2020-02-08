# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

from __future__ import annotations

import logging

from datetime import datetime, date, timezone
from werkzeug.exceptions import BadRequest, NotFound, InternalServerError
from dataclasses import dataclass, field, asdict, fields
from dacite import from_dict
from typing import Dict, Any, List, Optional, Type
from pymongo import ReturnDocument
from pymongo.errors import DuplicateKeyError
from bson import ObjectId
from . import MongoModel, dbconfig

log = logging.getLogger('bycco')


def isactive(dd: dict) -> bool:
    p = dd.get('publishedtime', None)
    e = dd.get('expirytime', None)
    published = p and (p < datetime.now(timezone.utc))
    expired = e and (e < datetime.now(timezone.utc))
    return bool(published and not expired)

@dataclass
class BasicDocument:
    """
    A readonly view used in overviews
    """
    active: bool
    creationtime: datetime
    doctype: str
    expirytime: Optional[datetime]
    id: str
    modificationtime: datetime
    publishedtime: Optional[datetime]
    name: str
    slug: str

@dataclass
class I18nFields:
    """
    contains the localized fields of a document
    """
    content: str = ""
    intro: str = ""
    title: str = ""

@dataclass
class I18nView:
    """
    A localized readonly view of a Document
    """
    active: bool
    creationtime: datetime
    i18n_fields: I18nFields
    id: str
    locale: str
    name: str              
    modificationtime: datetime
    owner: str
    slug: str

@dataclass
class DocumentModel(MongoModel):
    """
    A Document in the database
    """
    name: str
    owner: str 
    slug: str

    active: bool = False
    creationtime: Optional[datetime] = None
    doctype: str = "page"   # or: "calendaritem", "article"
    expirytime: Optional[datetime] = None
    i18n_fields: Dict[str, I18nFields] = field(default_factory=dict)
    languages: List[str] = field(default_factory=list)
    modificationtime: Optional[datetime] = None
    publishedtime: Optional[datetime] = None

    id: str = ""    
    _id: ObjectId = field(default_factory=ObjectId)

    _collection = 'doc'
    _hidden = ['_id']

    def __post_init__(self):
        # attribute id is created automatically as stringified version of _id
        self.id = str(self._id)
        if not self.creationtime:
            self.creationtime = datetime.now(timezone.utc)
        if not self.modificationtime:
            self.modificationtime = datetime.now(timezone.utc)
        if not self.languages:
            self.languages = ['en']

    @classmethod
    def create_doc(cls, docdict: Dict[str, Any] ) -> DocumentModel:
        """
        create a new doc
        """
        docdict['_id'] = docdict.get('_id', ObjectId())
        try:
            doc = from_dict(data_class=DocumentModel, data=docdict)
        except:
            log.exception('error encoding docdict')
            raise BadRequest(description="CannotEncodeCreatedDoc")
        try:
            docnewdict = asdict(doc)
            docnewdict.pop('id', None)
            cls.coll().insert_one(docnewdict)
        except DuplicateKeyError:
            log.exception('doc with duplicate key')
            raise BadRequest(description="DuplicateKeyError")
        except:
            log.exception('error inserting docdict')
            raise BadRequest(description="CannotInsertDoc")
        return doc

    @classmethod
    def find(cls, options: dict = {}) -> List[BasicDocument]:
        """
        find all pages as a list of BasicDocuments, 
        filtering on certain fields is enabled.
        """
        docs = []
        filter: Dict[str, Any] = {}
        if options.get('doctype'):
            filter['doctype'] = { '$in': options['doctype'].split(',')}
        if options.get('active'):
            filter['active'] = True
        log.info(f'find filter: {filter}')
        projfields = { k.name:1 for k in fields(BasicDocument)}
        cursor = cls.coll().find(filter, projfields)
        for doc in cursor:
            doc['id'] = str(doc.pop('_id'))
            try:
                docs.append(from_dict(data_class=BasicDocument, data=doc))
            except:
                log.exception('error encoding BasicDocument')
                raise InternalServerError(description="CannotEncodeDoc")
        return docs

    @classmethod
    def find_byslug(cls, slug: str) -> DocumentModel:
        """
        find a page by slug
        raises NotFound if nothing is found
        """
        docdict = cls.coll().find_one({'slug': slug})
        if not docdict:
            raise NotFound(description="DocNotFound")
        try:
            return from_dict(data_class=cls, data=docdict)
        except:
            log.exception('error encoding pagedoc')
            raise InternalServerError(description="ErrorEncodingDoc")

    @classmethod
    def find_localized(cls, slug: str, lang: str) -> I18nView:        
        """
        find a doc by slug and locale.  Filters out the correct language
        raises NotFound if nothing is found
        """
        pagedoc = cls.coll().find_one({'slug': slug}, 
            {'doctype': 0, 'expirytime': 0, 'languages': 0, 'publishedtime': 0})
        if not pagedoc:
            raise NotFound(description="PageNotFound")
        try:
            pagedoc['id'] = str(pagedoc.pop('_id'))
            pagedoc['locale'] = lang
            pagedoc['i18n_fields'] = pagedoc.pop('i18n_fields', {}).get(lang, 
                I18nFields())
            i18nview = from_dict(data_class=I18nView, data=pagedoc)
            return i18nview
        except:
            log.exception('error encoding docdict')
            raise InternalServerError(description="ErrorEncodingI18nView")

    @classmethod
    def get_byid(cls, id: str) -> DocumentModel:
        """
        get a doc by id
        raises NotFound if nothing is found
        """
        try:
            oid = ObjectId(id)
        except:
            raise BadRequest(description="InvalidDocId")
        docdict = cls.coll().find_one(oid)
        if not docdict:
            raise NotFound(description="DocNotFound")
        try:
            return from_dict(data_class=cls, data=docdict)
        except:
            log.exception('error encoding document')
            raise InternalServerError(description="ErrorEncodingDoc")

    @classmethod
    def update_doc(cls, id: str, docupdate: Dict[str, Any] ) -> DocumentModel:
        """
        update a document
        """
        try:
            oid = ObjectId(id)
        except:
            raise BadRequest(description="InvalidDocId")
        docupdate['modificationtime'] = datetime.now(timezone.utc)
        docupdate['active'] = isactive(docupdate)
        docdict = cls.coll().find_one_and_update({'_id': oid}, 
            {'$set': docupdate}, return_document=ReturnDocument.AFTER)
        if not docdict:
            raise NotFound(description="DocNotFound")
        try:
            return from_dict(data_class=cls, data=docdict)
        except:
            log.exception('error encoding doc')
            raise InternalServerError(description="ErrorEncodingDoc")

    @classmethod
    def remove_doc(cls, id: str) -> None:
        """
        delete a document 
        """
        try:
            oid = ObjectId(id)
        except:
            raise BadRequest(description="InvalidDocumentId")
        rs = cls.coll().delete_one({'_id': oid})
        if rs.deleted_count != 1:
            raise NotFound(description="DocumentNotFound")