# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

from __future__ import annotations

import logging

from dataclasses import dataclass, field, asdict
from dacite import from_dict
from typing import Dict, Any, List, Optional, Type, Union
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
class Attendee:
    """
    A readonly view used in overview of all attendees
    """
    category: str
    confirmed: bool
    first_name: str
    gender: str                 # M, F
    id: str
    idbel: str
    idclub: str
    last_name: str
    registrationdate: datetime
    subscriptionnumber: int

    nationalityfide: str = ''
    meals: str = ''
    present: Optional[datetime] = None
    payamount: int = 0 
    rating: int = 0
    ratingbel: int = 0
    ratingfide: int = 0

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
    id: str = ""    
    _id: ObjectId = field(default_factory=ObjectId)
    idfide: str = ''
    invoicenumber: int = 0
    meals: str = ''
    mobileattendant: str = ''
    mobileparent: str = ''
    mobileplayer: str = ''
    nationalityfide: str = ''
    payamount: int = 0
    paydate: Optional[datetime] = None
    paymessage: str = ''
    present: Optional[datetime] = None
    rating: int = 0
    ratingbel: int = 0
    ratingfide: int = 0
    remarks: str = ''
    subscriptionnumber: int = 0

    _collection = 'subscription'

    # attribute id is created automatically as stringified version of _id
    def __post_init__(self):
        self.id = str(self._id)

    @classmethod
    def csv_subscriptions(cls) -> List[dict]:
        """
        find all subscription for csv output
        """
        coll = dbconfig['db'][cls._collection]
        subs = []
        cursor = coll.find({}, {'badgeimage': 0})
        for doc in cursor:
            doc['id'] = str(doc.pop('_id'))
            doc['badgeimage'] = ''
            subs.append(doc)
        return subs
    
    @classmethod
    def find_subscriptions(cls, format=None) -> List[BasicSubscription]:
        """
        find all subscription
        """
        coll = dbconfig['db'][cls._collection]
        subs = []
        fields = {
            "category": 1,
            "first_name": 1,
            "last_name": 1,
            "registrationdate": 1,
        }
        cursor = coll.find({}, fields)
        for doc in cursor:
            doc['id'] = str(doc.pop('_id'))
            try:
                subs.append(BasicSubscription(**doc))
            except:
                raise InternalServerError(description="CannotEncodeBasicSubscription")
        return subs

    @classmethod
    def find_by_idbel(cls, idbel: str, withimage=False) -> "SubscriptionModel":
        """
        find a subscription by idbel
        """
        if withimage:
            subdoc = cls.coll().find_one({'idbel': idbel})
        else:
            subdoc = cls.coll().find_one({'idbel': idbel}, {'badgeimage':0})
        if not subdoc:
            raise NotFound(description="SubscriptionNotFound")
        try:
            return cls(**subdoc)
        except:
            log.exception('Cannot encode Subscription')
            raise InternalServerError(description="CannotEncodeSubscription")

    @classmethod
    def find_by_id(cls, id: str, withimage=False) -> "SubscriptionModel":
        """
        find a subscription by id
        """
        try:
            oid = ObjectId(id)
        except:
            raise BadRequest(description="InvalidSubscriptionId")
        if withimage:
            subdoc = cls.coll().find_one(oid)
        else:
            subdoc = cls.coll().find_one(oid, {'badgeimage':0})
        if not subdoc:
            raise NotFound(description="SubscriptionNotFound")
        try:
            return from_dict(data_class=SubscriptionModel, data=subdoc)
        except:
            log.exception('Cannot encode Subscription')
            raise InternalServerError(description="CannotEncodeSubscription")

    @classmethod
    def get_attendees(cls, options: dict) -> List[Attendee]:
        """
        find all subscriptions for attendee
        """
        coll = dbconfig['db'][cls._collection]
        subs = []
        fields = {
            'category': 1,
            'confirmed': 1,
            'first_name': 1,
            'gender': 1,
            'idbel': 1,
            'idclub': 1,
            'last_name': 1,
            'nationalityfide': 1,
            'meals': 1,
            'present': 1,
            'payamount': 1,
            'rating': 1,
            'ratingbel': 1,
            'ratingfide': 1,
            'registrationdate': 1,
            'subscriptionnumber': 1,
        }
        filter = {}
        if options['cat']:
            filter['category'] = options['cat']
        if options['ss']:
            filter['last_name'] = { '$regex': options['ss'], '$options': 'i' } 
        if options['confirmed']:
            filter['confirmed'] = True
        cursor = coll.find(filter, fields)
        for doc in cursor:
            doc['id'] = str(doc.pop('_id'))
            try:
                subs.append(from_dict(data_class=Attendee, data=doc))
            except:
                raise InternalServerError(description="CannotEncodeAttendee")
        return subs

    @classmethod
    def blank(cls) -> SubscriptionModel:
        """
        create a blank subscription
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
            'subscriptionnumber': CounterModel.nextValue('subscription')
        })
        subdict = coll.find_one(id)
        try:
            sub = cls(**subdict)
            return sub
        except:
            log.exception('Cannot encode Subscription')
            raise InternalServerError(description="CannotEncodeSubscription")

    @classmethod
    def updateSubscription(cls, id: str, subdict: Dict[str, Any]) -> SubscriptionModel:
        """
        update a subscription 
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
            return from_dict(data_class=SubscriptionModel, data=subdoc)
        except:
            log.exception('error encoding subdict')
            raise InternalServerError(description="ErrorEncodingSubscription")

    def save(self) -> None:
        """
        save changes of Subscription instance
        """
        subdict = asdict(self)
        subdict.pop('id', None)
        self.coll().find_one_and_replace({'_id': self._id}, subdict)

    @classmethod
    def removeSubscription(cls, id: str) -> None:
        """
        delete a subscription 
        """
        try:
            oid = ObjectId(id)
        except:
            raise BadRequest(description="InvalidSubscriptionId")
        rs = cls.coll().delete_one({'_id': oid})
        if rs.deleted_count != 1:
            raise NotFound(description="SubscriptionNotFound")


