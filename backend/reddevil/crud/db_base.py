# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging
import uuid
from datetime import datetime, date, timezone
from typing import List, Dict, Any, Optional
from pymongo import ReturnDocument
from pymongo.errors import DuplicateKeyError

from ..common import RdNotFound, RdBadRequest
from reddevil.common import get_db

log = logging.getLogger('election')

class DbBase:
    """
    Base class for Mongo collection async operations
    Input parameters are scalars, stringigfied ids and dicts, we do not use dataclasess
    Output parameters are scalars, stringigfied ids and dicts, we do not use dataclasess
    All operations are dumb, unaware of any business logic
    RdExceptions can be raised   
    """

    COLLECTION: Optional[str] = None    # should be overriden
    DOCUMENTTYPE = 'Base'               # should be overriden
    VERSION = 1
    SIMPLEFIELDS: list = []
    HIDDENFIELDS: list = []

    @classmethod
    async def add(cls, doc_in: dict ) -> str:
        """
        create a new record, starting form doc_in, return the id 
        """
        coll = get_db()[cls.COLLECTION]
        doc_in['_id'] = doc_in.pop('id', str(uuid.uuid4()))
        doc_in['_documenttype'] = cls.DOCUMENTTYPE
        doc_in['_version'] = cls.VERSION
        try:
            await coll.insert_one(doc_in)
        except:
            log.exception(f'error inserting {cls.COLLECTION} record')
            raise RdBadRequest(description=f"CannotCreate{cls.COLLECTION}")
        return doc_in['_id']

    @classmethod
    async def find_multiple(cls, options: dict={}) -> List[dict]:
        """
        get all records
        """
        coll = get_db()[cls.COLLECTION]
        docs = []
        _fieldlist = options.pop('_fieldlist', cls.SIMPLEFIELDS)
        projfields = {k:1 for k in _fieldlist} if _fieldlist else {
            k:0 for k in cls.HIDDENFIELDS} or None
        async for doc in coll.find(options, projection=projfields):
            doc['id'] = doc.pop('_id')
            docs.append(doc)
        return docs

    @classmethod
    async def find_single(cls, options: dict) -> dict:
        """
        find an doc, 
        raises NotFound if nothing is found
        """
        coll = get_db()[cls.COLLECTION]
        if 'id' in options:
            options['_id'] = options.pop('id')
        fieldlist = options.pop('_fieldlist', None)
        projfields = {k:1 for k in fieldlist} if fieldlist else {
            k:0 for k in cls.HIDDENFIELDS} or None
        doc = await coll.find_one(options, projection=projfields)
        if not doc:
            raise RdNotFound(description=f"CannotFindSingle{cls.COLLECTION}")
        doc['id'] = doc.pop('_id')
        return doc

    @classmethod
    async def update(cls, id: str, docupdate: Dict[str, Any], 
            options: dict = {}) -> dict:
        """
        update an doc
        raises NotFound if event is not found
        """
        coll = get_db()[cls.COLLECTION]
        docupdate['modificationtime'] = datetime.now(timezone.utc)
        doc = await coll.find_one_and_update(
            {'_id': id},
            dict(**{'$set': docupdate}, **options),
            projection={k:0 for k in cls.HIDDENFIELDS},
            return_document=ReturnDocument.AFTER)
        if not doc:
            raise RdNotFound(description=f"CannotFind{cls.COLLECTION}")
        doc['id'] = doc.pop('_id')
        return doc

    @classmethod
    async def delete(cls, id: str) -> None:
        """
        delete an doc
        """
        coll = get_db()[cls.COLLECTION]
        rs = await coll.delete_one({'_id': id})
        if rs.deleted_count != 1:
            raise RdNotFound(description=f"CannotFind{cls.COLLECTION}")

    @classmethod
    async def upgrade(cls, version: int) -> None:
        """
        upgrade the document to version 
        """
        pass
