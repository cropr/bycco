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
from ..common import db_conn, RdBadRequest, RdNotFound

log = logging.getLogger('reddevil')

class DbBoardMember:
    COLLECTION = 'rd_boardmembers'
    DOCUMENTTYPE = 'BoardMember'
    SIMPLEFIELDS = [ 'enabled', 'boardroles', 'email', 'first_name', 
        'last_name', 'membertype', 'mobile', 'priority', 'showemail', 'showmobile']

    # the fields for this class are for documentation purposes
    # they are not used in the code

    enabled: bool
    boardroles: List[str]
    email: str
    first_name: str
    id: str
    last_name: str
    mobile: str
    picture: bytes
    picturemimetype: str
    priority: int
    showemail: bool
    showmobile: bool

    @classmethod
    def create_bmember(cls, doc_in: dict ) -> str:
        """
        create a new Docement, starting form doc_in 
        """
        from ..common import db_conn
        doc_in['_id'] = doc_in.get('_id', ObjectId())
        doc_in['_documenttype'] = DbBoardMember.DOCUMENTTYPE
        try:
            db_conn[1][DbBoardMember.COLLECTION].insert_one(doc_in)
        except:
            log.exception('error inserting bmemberdict')
            raise RdBadRequest(description="CannotInsertBMember")
        return str(doc_in['_id'])

    @classmethod
    def find_bmembers(cls, options: dict = {}) -> List[dict]:
        """
        find all bord memerbs, 
        filtering on certain fields is enabled.
        """
        from ..common import db_conn
        docs = []
        filter: Dict[str, Any] = {}
        _fieldlist = options.pop('_fieldlist', DbBoardMember.SIMPLEFIELDS)
        if options.get('active'):
            filter['active'] = True
        projfields = { k:1 for k in _fieldlist}
        cursor = db_conn[1][DbBoardMember.COLLECTION].find(filter, projection=projfields)
        for doc in cursor:
            doc['id'] = str(doc.pop('_id'))
            docs.append(doc)
        return docs

    @classmethod
    def find_bmember(cls, options: dict) -> dict:
        """
        find a baord member, 
        raises NotFound if nothing is found
        """
        from ..common import db_conn
        if 'id' in options:
            try:
                options['_id'] = ObjectId(options.pop('id'))
            except:
                raise RdBadRequest(description='InvalidBMemberId')                
        _fieldlist = options.pop('_fieldlist', None)
        projfields = { k:1 for k in _fieldlist} if _fieldlist else None
        doc = db_conn[1][DbBoardMember.COLLECTION].find_one(options, projection=projfields)
        if not doc:
            raise RdNotFound(description="BMemberNotFound")
        doc['id'] = str(doc.pop('_id'))
        return doc

    @classmethod
    def update_bmember(cls, id: str, docupdate: Dict[str, Any] ) -> dict:
        """
        update a board member
        raises NotFound if bmember is not found
        """
        from ..common import db_conn
        try:
            oid = ObjectId(id)
        except:
            raise RdBadRequest(description="InvalidBMemberId")
        doc = db_conn[1][DbBoardMember.COLLECTION].find_one_and_update({'_id': oid}, 
            {'$set': docupdate}, return_document=ReturnDocument.AFTER)
        if not doc:
            raise RdNotFound(description="BMemberNotFound")
        doc['id'] = str(doc.pop('_id'))
        return doc

    @classmethod
    def remove_bmember(cls, id: str) -> None:
        """
        delete a document 
        """
        from ..common import db_conn
        try:
            oid = ObjectId(id)
        except:
            raise RdBadRequest(description="InvalidBMemberId")
        rs = db_conn[1][DbBoardMember.COLLECTION].delete_one({'_id': oid})
        if rs.deleted_count != 1:
            raise RdNotFound(description="BMemberNotFound")