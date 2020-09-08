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
from ..common import RdBadRequest, RdNotFound, cfg, date2datetime

log = logging.getLogger('reddevil')


class DbFile:
    COLLECTION = 'rd_file'
    DOCUMENTTYPE = 'File'
    SIMPLEFIELDS = [ 'archived', 'created_ts', 'filelength', 'locale', 'mimetype',
        'modified_ts', 'name', 'topic', 'topic_ts', 'url']
    

    # the fields for this class are for documentation purposes
    # they are not used in the code

    archived: bool
    created_by: str
    created_ts: datetime
    filelength: int
    locale: str
    id: str
    mimetype: str
    modified_ts: datetime
    name: str
    path: str
    topic: str     # report BM, report GA, ....
    topic_ts: datetime
    url: str

    @classmethod
    def create_file(cls, doc_in: dict ) -> str:
        """
        create a new file, starting form doc_in 
        """
        from ..common import conn
        doc_in['_id'] = doc_in.get('_id', ObjectId())
        doc_in['_documenttype'] = cls.DOCUMENTTYPE
        doc_in['created_ts'] = doc_in['modified_ts'] = datetime.now(timezone.utc)
        date2datetime(doc_in, 'topic_ts')
        try:
            conn[1][cls.COLLECTION].insert_one(doc_in)
        except DuplicateKeyError:
            log.exception('file with duplicate key')
            raise RdBadRequest(description="DuplicateKeyError")
        except:
            log.exception('error inserting filedict')
            raise RdBadRequest(description="CannotInsertFile")
        return str(doc_in['_id'])

    @classmethod
    def find_files(cls, options: dict = {}) -> List[dict]:
        """
        find all files, 
        filtering on certain fields is enabled.
        """
        from ..common import conn
        files = []
        filter: Dict[str, Any] = {}
        _fieldlist = options.pop('_fieldlist', cls.SIMPLEFIELDS)
        if '_in' in options:
            for inexpr in options['_in']:
                filter[inexpr[0]] = {'$in': inexpr[1]}
        projfields = {k:1 for k in _fieldlist}
        cursor = conn[1][cls.COLLECTION].find(filter, projection=projfields)
        for doc in cursor:
            doc['id'] = str(doc.pop('_id'))
            files.append(doc)
        return files

    @classmethod
    def find_file(cls, options: dict) -> dict:
        """
        find a file, 
        raises NotFound if nothing is found
        """
        from ..common import conn
        if 'id' in options:
            try:
                options['_id'] = ObjectId(options.pop('id'))
            except:
                raise RdBadRequest(description='InvalidFileId')                
        _fieldlist = options.pop('_fieldlist', None)
        projfields = { k:1 for k in _fieldlist} if _fieldlist else None
        file = conn[1][cls.COLLECTION].find_one(options, projection=projfields)
        if not file:
            raise RdNotFound(description="FileNotFound")
        file['id'] = str(file.pop('_id'))
        return file

    @classmethod
    def update_file(cls, id: str, fileupdate: Dict[str, Any] ) -> dict:
        """
        update a file
        raises NotFound if file is not found
        """
        from ..common import conn
        try:
            oid = ObjectId(id)
        except:
            raise RdBadRequest(description="InvalidFileId")
        fileupdate['modified_ts'] = datetime.now(timezone.utc)
        date2datetime(fileupdate, 'topic_ts')
        file = conn[1][cls.COLLECTION].find_one_and_update({'_id': oid}, 
            {'$set': fileupdate}, return_document=ReturnDocument.AFTER)
        if not file:
            raise RdNotFound(description="FileNotFound")
        file['id'] = str(file.pop('_id'))
        return file

    @classmethod
    def remove_file(cls, id: str) -> None:
        """
        delete a file 
        """
        from ..common import conn
        try:
            oid = ObjectId(id)
        except:
            raise RdBadRequest(description="InvalidFileId")
        rs = conn[1][cls.COLLECTION].delete_one({'_id': oid})
        if rs.deleted_count != 1:
            raise RdNotFound(description="FileNotFound")