# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

from __future__ import annotations

import logging

from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional, Type
from datetime import datetime, timedelta
from pymongo import ReturnDocument
from bson import ObjectId
from . import MongoModel, dbconfig

log = logging.getLogger('bycco')

@dataclass
class BasicSubscription:
    """
    A readonly view used in overview of all subscriptions
    """
    category: str
    first_name: str
    id: str
    last_name: str
    registrationdate: datetime

@dataclass
class SubscriptionModel(MongoModel):

    birthdate: datetime
    category: str               # ARB, ORG, Bxx, Gxx, BGxx, SPO, EAT
    confirmed: bool
    chesstitle: str
    federation: str
    first_name: str
    gender: str                 # M, F
    idclub: str
    idbel: str
    locale: str
    last_name: str
    nationalitybel: str
    registrationdate: datetime

    badgeimage: Optional[bytes] = None
    badgelength: int = 0
    badgemimetype: str = 'image/jpeg'
    catering: Optional[str] = None
    custom: Optional[str] = None
    emailparent: Optional[str] = None
    emailplayer: Optional[str] = None
    fullnameattendant: Optional[str] = None
    fullnameparent: Optional[str] = None
    id: str = field(init=False, default="")    
    _id: ObjectId = field(default_factory=ObjectId)
    idfide: Optional[str] = None
    mobileattendant: Optional[str] = None
    mobileparent: Optional[str] = None
    mobileplayer: Optional[str] = None
    nationalityfide: Optional[str] = None
    payamount: int = 0
    paydate: Optional[datetime] = None
    paymessage: Optional[str] = None
    present: Optional[datetime] = None
    rating: int = 0
    ratingbel: int = 0
    ratingfide: int = 0
    remarks: Optional[str] = None

    _collection = 'subscription'

    @classmethod
    def find_subscriptions( cls: Type["SubscriptionModel"] ) -> List[BasicSubscription]:
        """
        find all subscription
        """
        coll = dbconfig['db'][cls._collection]
        subs = []
        cursor = coll.find({}, {
            "first_name": 1,
            "last_name": 1,
            "registratiotndate": 1,
            "modificationtime": 1,
        })
        for doc in cursor:
            doc['id'] = str(doc.pop('_id'))
            try:
                sub = BasicSubscription(**doc)
                subs.append(sub)
            except:
                log.exception('error encoding BasicSubscription')
                continue
        return subs