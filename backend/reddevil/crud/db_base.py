# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging
import uuid
import asyncio
from datetime import datetime, date, timezone
from typing import List, Dict, Any, Optional
from bson.objectid import ObjectId
from pymongo import ReturnDocument
from pymongo.errors import DuplicateKeyError

from ..common import RdNotFound, RdBadRequest
from reddevil.common import get_db

log = logging.getLogger('reddevil')

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
    IDGENERATOR = 'uuid'
    FORCEUPGRADE = False

    @classmethod
    def idgenerator(cls):
        if cls.IDGENERATOR == 'uuid':
            return str(uuid.uuid4())
        if cls.IDGENERATOR == 'objectid':
            return ObjectId()
    
    @classmethod
    def id_to_native(cls, id):
        if cls.IDGENERATOR == 'uuid':
            return id
        if cls.IDGENERATOR == 'objectid':
            return ObjectId(id)

    @classmethod
    def id_from_native(cls, _id):
        if cls.IDGENERATOR == 'uuid':
            return _id
        if cls.IDGENERATOR == 'objectid':
            return str(_id)

    @classmethod
    async def add(cls, doc_in: dict ) -> str:
        """
        create a new record, starting form doc_in, return the id 
        """
        coll = get_db()[cls.COLLECTION]
        if 'id' in doc_in:
            doc_in['_id'] = cls.id_to_native(doc_in.pop('id'))
        else:
            doc_in['_id'] = cls.idgenerator()
        doc_in['_documenttype'] = cls.DOCUMENTTYPE
        doc_in['_version'] = cls.VERSION
        doc_in['_creationtime'] = datetime.now(timezone.utc)
        doc_in['_modificationtime'] = datetime.now(timezone.utc)
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
        if 'id' in options:
            options['_id'] = cls.id_to_native(options.pop('id'))
        _fieldlist = options.pop('_fieldlist', cls.SIMPLEFIELDS)
        projfields = {k:1 for k in _fieldlist} if _fieldlist else {
            k:0 for k in cls.HIDDENFIELDS} or None
        # if FORCEUPGRADE inject _version in projfields
        if cls.FORCEUPGRADE and projfields and ('_version' not in projfields):
            projfields['_version'] = 2
        async for doc in coll.find(options, projection=projfields):
            if cls.FORCEUPGRADE:
                oldversion = doc.get('_version', 1)
                if projfields and projfields['_version'] == 2:
                    # remove _version after injection
                    doc.pop('_version', None)
                if oldversion != cls.VERSION:
                    doc = await cls.upgrade(doc, projfields, oldversion)
            doc['id'] = cls.id_from_native(doc.pop('_id'))
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
            options['_id'] = cls.id_to_native(options.pop('id'))
        fieldlist = options.pop('_fieldlist', None)
        projfields = {k:1 for k in fieldlist} if fieldlist else {
            k:0 for k in cls.HIDDENFIELDS} or None
        # if FORCEUPGRADE inject _version in projfields
        if cls.FORCEUPGRADE and projfields and ('_version' not in projfields):
            projfields['_version'] = 2
        doc = await coll.find_one(options, projection=projfields)
        if not doc:
            raise RdNotFound(description=f"CannotFindSingle{cls.COLLECTION}")
        if cls.FORCEUPGRADE:
            oldversion = doc.get('_version', 1)
            if projfields and projfields['_version'] == 2:
                # remove _version after injection
                doc.pop('_version', None)
            if oldversion != cls.VERSION:
                doc = await cls.upgrade(doc, projfields, oldversion)
        doc['id'] = cls.id_from_native(doc.pop('_id'))
        return doc

    @classmethod
    async def update(cls, id: str, docupdate: Dict[str, Any], 
            options: dict = {}) -> dict:
        """
        update an doc
        raises NotFound if event is not found
        """
        coll = get_db()[cls.COLLECTION]
        idn = cls.id_to_native(id)
        vu = options.pop('_versionupgrade', None)
        if vu:
            doc = await coll.find_one({'_id': idn}, projection={'_version':1})
            doc = await cls.upgrade(doc, None, doc.get('_version', 1))
        docupdate['_modificationtime'] = datetime.now(timezone.utc)
        doc = await coll.find_one_and_update(
            {'_id': idn},
            dict(**{'$set': docupdate}, **options),
            projection={k:0 for k in cls.HIDDENFIELDS},
            return_document=ReturnDocument.AFTER)
        if not doc:
            raise RdNotFound(description=f"CannotFind{cls.COLLECTION}")
        doc['id'] =  cls.id_from_native(doc.pop('_id'))
        return doc

    @classmethod
    async def delete(cls, id: str) -> None:
        """
        delete an doc
        """
        coll = get_db()[cls.COLLECTION]
        rs = await coll.delete_one({'_id': cls.id_to_native(id)})
        if rs.deleted_count != 1:
            raise RdNotFound(description=f"CannotFind{cls.COLLECTION}")

    @classmethod
    async def upgrade(cls, doc: dict, projfields: Optional[dict],  
        from_version: int = 1
    ) -> dict:
        """
        upgrade the document to version 
        """
        return doc
                
    @classmethod
    async def restore(cls, docs: List[dict]) -> None:
        """
        delete an doc
        """
        coll = get_db()[cls.COLLECTION]
        await coll.delete_many({})
        await coll.insert_may(docs)
