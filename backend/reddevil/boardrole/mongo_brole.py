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
from ..common import RdBadRequest, RdNotFound

log = logging.getLogger('reddevil')

class DbBoardRole:
    COLLECTION = 'rd_boardroles'
    DOCUMENTTYPE = 'BoardRole'

    # the fields for this class are for documentation purposes
    # they are not used in the code

    i18n: Dict[str,str]
    id: str
    name: str

    @classmethod
    def create_brole(cls, doc_in: dict ) -> str:
        """
        create a new Docement, starting form doc_in 
        """
        from ..common import db_conn
        coll = db_conn[1][DbBoardRole.COLLECTION]
        doc_in['_id'] = doc_in.get('_id', ObjectId())
        doc_in['_documenttype'] = DbBoardRole.DOCUMENTTYPE
        doc_in['i18n'] = doc_in.get('i18n', [])
        try:
            coll.insert_one(doc_in)
        except:
            log.exception('error inserting broledict')
            raise RdBadRequest(description="CannotInsertBRole")
        return str(doc_in['_id'])

    @classmethod
    def find_broles(cls, options: dict = {}) -> List[dict]:
        """
        find all bord roles, 
        """
        from ..common import db_conn
        coll = db_conn[1][DbBoardRole.COLLECTION]
        docs = []
        cursor = coll.find({})
        for doc in cursor:
            doc['id'] = str(doc.pop('_id'))
            docs.append(doc)
        return docs

    @classmethod
    def find_brole(cls, options: dict) -> dict:
        """
        find a board role, 
        raises NotFound if nothing is found
        """
        from ..common import db_conn
        coll = db_conn[1][DbBoardRole.COLLECTION]
        if 'id' in options:
            try:
                options['_id'] = ObjectId(options.pop('id'))
            except:
                raise RdBadRequest(description='InvalidBRoleId')                
        doc = coll.find_one(options)
        if not doc:
            raise RdNotFound(description="BRoleNotFound")
        doc['id'] = str(doc.pop('_id'))
        return doc

    @classmethod
    def update_brole(cls, id: str, docupdate: Dict[str, Any] ) -> dict:
        """
        update a board role
        raises NotFound if brole is not found
        """
        from ..common import db_conn
        coll = db_conn[1][DbBoardRole.COLLECTION]
        try:
            oid = ObjectId(id)
        except:
            raise RdBadRequest(description="InvalidRoleId")
        doc = coll.find_one_and_update({'_id': oid}, 
            {'$set': docupdate}, return_document=ReturnDocument.AFTER)
        if not doc:
            raise RdNotFound(description="BRoleNotFound")
        doc['id'] = str(doc.pop('_id'))
        return doc

    @classmethod
    def remove_brole(cls, id: str) -> None:
        """
        delete a brole
        """
        from ..common import db_conn
        coll = db_conn[1][DbBoardRole.COLLECTION]
        try:
            oid = ObjectId(id)
        except:
            raise RdBadRequest(description="InvalidBRoleId")
        rs = coll.delete_one({'_id': oid})
        if rs.deleted_count != 1:
            raise RdNotFound(description="BRoleNotFound")
