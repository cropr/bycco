# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

# all database request come in here, but we do not use dataclasess
# if needed we define extra models an do marshalling functions at the service level
# All _id are translatesd to stringified id on output
# All functions expect stringified id as input 

import logging
import asyncio
from datetime import datetime, date, timezone
from typing import Dict, List, Any, Optional 
from pymongo import ReturnDocument
from pymongo.errors import DuplicateKeyError
from bson import ObjectId
from ..common import RdBadRequest, RdNotFound, date2datetime
from reddevil.crud.db_base import DbBase
from reddevil.common import get_db

log = logging.getLogger('reddevil')

class PageI18nFields:

    # the fields for this class are for documentation purposes
    # they are not used in the code

    body: str
    intro: str
    title: str

class DbPage(DbBase):
    COLLECTION = 'rd_page'
    DOCUMENTTYPE = 'Page'
    SIMPLEFIELDS = [ 'body', '_creationtime', 'doctype', 'enabled', 
        'expirationdate', 'intro', 'name',  '_modificationtime', 
        'publicationdate', 'slug', 'title', '_version']
    VERSION = 2
    FORCEUPGRADE = True

    @classmethod
    async def upgrade(
        cls, doc: dict, projfields: Optional[dict],  from_version: int = 1
    ) -> dict:
        """
        upgrade the document to the current version 
        """
        coll = get_db()[cls.COLLECTION]        
        if from_version == 1:
            # add _documenttype, _version, _modificationtime, _creationtime
            # remove creationtime, modificationtime
            docfull = await coll.find_one({'_id': doc['_id']})
            docupgrade = await coll.find_one_and_update(
                {'_id': doc['_id']},
                { '$set': {
                    '_documenttype': cls.DOCUMENTTYPE,
                    '_version': cls.VERSION,
                    '_creationtime': docfull.get('creationtime', 
                        docfull.get('_creationtime')),
                    '_modificationtime': docfull.get('modificationtime', 
                        docfull.get('_modificationtime')),
                }, '$unset': {
                    'creationtime': 1,
                    'modificationtime': 1,
                }}, return_document=ReturnDocument.AFTER 
            )
            doc = await coll.find_one({'_id': doc['_id']}, 
                projection=projfields)
            log.info(f'{cls.DOCUMENTTYPE} upgraded from {from_version} tp {cls.VERSION}')
            return doc
        else:
            asyncio.sleep(0)
            return doc
                        