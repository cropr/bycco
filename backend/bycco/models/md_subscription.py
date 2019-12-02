# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

from __future__ import annotations

import logging

from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional, Type
from datetime import datetime, timedelta, date
from pymongo import ReturnDocument
from bson import ObjectId
from werkzeug.exceptions import BadRequest, NotFound, InternalServerError
from . import MongoModel, dbconfig, CounterModel

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

    birthdate: str
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
    invoicenumber: int = 0
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
    subscriptionnumber: int = 0

    _collection = 'subscription'

    @classmethod
    def find_subscriptions( 
        cls: Type["SubscriptionModel"] 
    ) -> List[BasicSubscription]:
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

    @classmethod
    def find_by_idbel( 
        cls: Type["SubscriptionModel"],
        idbel: str, 
    ) -> "SubscriptionModel":
        """
        find a subscription by idbel
        """
        subdoc = cls.coll().find_one({'idbel': idbel})
        if not subdoc:
            return None
        try:
            return cls(**subdoc)
        except:
            log.exception('Cannot encode Subscription')
            raise InternalServerError(description="CannotEncodeSubscription")

    @classmethod
    def find_by_id( 
        cls: Type["SubscriptionModel"],
        idbel: str, 
    ) -> "SubscriptionModel":
        """
        find a subscription by idbel
        """
        try:
            oid = ObjectId(id)
        except:
            raise BadRequest(description="InvalidSubscriptionId")
        subdoc = cls.coll().find_one(oid)
        if not subdoc:
            raise NotFound(description="SubscriptionNotFound")
        try:
            return cls(**subdoc)
        except:
            log.exception('Cannot encode Subscription')
            raise InternalServerError(description="CannotEncodeSubscription")


    @classmethod
    def add_subscription( 
        cls: Type["SubscriptionModel"],
        subdict: Dict, 
    ) -> "SubscriptionModel":
        """
        find all subscription
        """

    @classmethod
    def blank( 
        cls: Type["SubscriptionModel"],
    ) -> "SubscriptionModel":
        """
        find all subscription
        """
        coll = dbconfig['db'][cls._collection]
        id = ObjectId()
        coll.insert_one({
            '_id': id,
            'birthdate': "1900-01-01",
            'category': '#NA',               # ARB, ORG, Bxx, Gxx, BGxx, SPO, EAT
            'confirmed': False,
            'chesstitle': '',
            'federation': '#NA',
            'first_name': '#NA',
            'gender': '#NA',                 # M, F
            'idclub': '#NA',
            'idbel': '#NA',
            'locale': '#NA',
            'last_name': '#NA',
            'nationalitybel': '#NA',
            'registrationdate': datetime.utcnow(),
            'subscriotionnumber': CounterModel.nextValue('subscription')
        })
        subdict = coll.find_one(id)
        try:
            sub = cls(**subdict)
            return sub
        except:
            log.exception('Cannot encode Subscription')
            raise InternalServerError(description="CannotEncodeSubscription")

    @classmethod
    def updateSubscription(
        cls: Type["SubscriptionModel"],
        id: str,
        subdict: Dict[str, Any]
    ) -> "SubscriptionModel":
        """
        update subscription 
        """
        try:
            oid = ObjectId(id)
        except:
            raise BadRequest(description="InvalidSubscriptionId")
        subdoc = cls.coll().find_one_and_update({'_id': oid}, 
            {'$set': subdict}, return_document=ReturnDocument.AFTER)
        if not subdoc:
            raise NotFound(description="SubscriptionNotFound")
        try:
            sub = cls(**subdoc)
            return sub
        except:
            log.exception('error encoding subdict')
            raise InternalServerError(description="ErrorEncodingSubscription")

    def save(self: "SubscriptionModel") -> None:
        """
        save changes of Subscription instance
        """
        subdict = asdict(self)
        self.coll().find_one_and_replace({'_id': self._id}, subdict)

