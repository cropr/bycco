# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

# all database request come in here, but we do not use dataclasess
# if needed we define extra models an do marshalling functions at the service level
# All _id are translatesd to stringified id on output
# All functions expect stringified id as input 

import pymongo
from datetime import datetime, date, timezone
from typing import Dict, List, Any 
from bson import ObjectId
from reddevil.crud.db_base import DbBase
from reddevil.common import get_db
from bycco import settings

class DbSubscription(DbBase):
    COLLECTION = 'subscription'
    DOCUMENTTYPE = 'Subscription'
    SIMPLEFIELDS = [ 
        'category', 'confirmed', 'first_name', 'last_name', 'idbel', 
        'subscriptiontime', 'subscriptionnumber',
    ]
    VERSION = 1

    @classmethod
    async def maxSubsciptionNumber(cls) -> int :
        coll = get_db()[cls.COLLECTION]
        cursor = coll.find(
            {}, 
            {'subscriptionnumber': 1}, 
            sort=[('subscriptionnumber', pymongo.DESCENDING)],
            limit=1,
        )
        docs = await cursor.to_list(1)
        return docs[0]['subscriptionnumber'] if len(docs) == 1 else 0
        
    @classmethod
    async def maxSubsciptionNumber(cls) -> int :
        coll = get_db()[cls.COLLECTION]
        cursor = coll.find(
            {}, 
            {'subscriptionnumber': 1}, 
            sort=[('subscriptionnumber', pymongo.DESCENDING)],
            limit=1,
        )
        docs = await cursor.to_list(1)
        return docs[0]['subscriptionnumber'] if len(docs) == 1 else 0
        
    @classmethod
    async def maxInvoiceNumber(cls) -> int:
        coll = get_db()[cls.COLLECTION]
        cursor = coll.find(
            {}, 
            {'invoicenumber': 1}, 
            sort=[('invoicenumber', pymongo.DESCENDING)],
            limit=1,
        )
        docs = await cursor.to_list(1)
        maxinvoice = settings.INVOICENUMBERSTART - 1
        if len(docs):
            d = docs[0]
            nr = d.get('invoicenumber', None)
            if nr: 
                maxinvoice = nr
        return maxinvoice
