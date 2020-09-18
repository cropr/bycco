# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

from datetime import datetime
from typing import Dict, Any, List, Optional, Type, Union
from enum import Enum
from pydantic import BaseModel

class SubscriptionCategory(str, Enum):
    B8 = 'B8'
    B10 = 'B10'
    B12 = 'B12'
    B14 = 'B14'
    B16 = 'B16'
    B18 = 'B18'
    B20 = 'B20'
    G8 = 'G8'
    G10 = 'G10'
    G12 = 'G12'
    G14 = 'G14'
    G16 = 'G16'
    G18 = 'G18'
    G20 = 'G20'
    ARB = 'ARB'
    ORG = 'ORG'

class Gender(str, Enum):
    M = 'M'
    F = 'F'

class Subscription(BaseModel):
    """
    the subscription model as used in the database
    is normally not exposed
    """
    birthdate: str
    category: SubscriptionCategory
    chesstitle: str
    confirmed: bool
    custom: Optional[str] 
    emailattendant: str 
    emailplayer: Optional[str] 
    federation: str
    first_name: str
    gender: Gender
    idbel: str
    idclub: str
    idfide: str 
    invoicenumber: Optional[int] 
    locale: str
    last_name: str
    mobileattendant: str 
    mobileplayer: str 
    nameattendant: str
    nationality: str 
    payamount: int 
    paydate: Optional[datetime]
    paymessage: str 
    present: Optional[datetime]
    ratingbel: int 
    ratingfide: int 
    remarks: str
    subscriptiontime: datetime
    subscriptionnumber: int
    _id: str 
    _version: int
    _documenttype: str

class SubscriptionIn(BaseModel):
    """
    the model to create a subscription
    """
    category: SubscriptionCategory 
    idbel: str
    locale: str

class SubscriptionOptional(BaseModel):
    """
    the generic model used to encode results from the DB
    Normally more fine grained models are used
    """
    birthdate: Optional[str]
    category: Optional[SubscriptionCategory]
    chesstitle: Optional[str]
    confirmed: Optional[bool]
    custom: Optional[str] 
    emailattendant: Optional[str ]
    emailplayer: Optional[str] 
    federation: Optional[str]
    first_name: Optional[str]
    gender: Optional[str]
    id: Optional[str] 
    idbel: Optional[str]
    idclub: Optional[str]
    idfide: Optional[str]
    invoicenumber: Optional[int] 
    locale: Optional[str]
    last_name: Optional[str]
    mobileattendant: Optional[str]
    mobileplayer: Optional[str]
    nameattendant: Optional[str]
    nationality: Optional[str]
    payamount: Optional[int]
    paydate: Optional[datetime]
    paymessage: Optional[str]
    present: Optional[datetime]
    ratingbel: Optional[int] 
    ratingfide: Optional[int]
    remarks: Optional[str]
    subscriptiontime: Optional[datetime]
    subscriptionnumber: Optional[int]

class SubscriptionOut(BaseModel):
    """
    A readonly view used in overview of all subscriptions
    """
    category: SubscriptionCategory
    confirmed: bool
    first_name: str
    id: str
    idbel: str
    last_name: str
    subscriptiontime: datetime
    subscriptionnumber: int

class SubscriptionList(BaseModel):
    """
    a list view of subscriptions
    """
    subscriptions: List[Any]

class SubscriptionDetailedOut(SubscriptionOptional):
    """
    a readonly view to get a detailed view on a single subscription
    """
    birthdate: str
    category: SubscriptionCategory
    chesstitle: str
    confirmed: bool
    emailattendant: str 
    federation: str
    first_name: str
    gender: str                
    id: str 
    idbel: str
    idclub: str
    idfide: str 
    locale: str
    last_name: str
    mobileattendant: str 
    mobileplayer: str 
    nameattendant: str
    nationality: str 
    payamount: int 
    ratingbel: int 
    ratingfide: int 
    remarks: str
    subscriptiontime: datetime
    subscriptionnumber: int 

class CheckIdReply(BaseModel):
    belfound: bool
    birthyear: Optional[str] = None
    first_name: Optional[str] = ''
    fidefound: bool = False
    idfide: Optional[str] = None
    gender: Optional[Gender] = None
    last_name: Optional[str] = ''
    nationality: str = 'BEL'
    ratingbel: int = 0
    ratingfide: int = 0
    subfound: bool = False
    subconfirmed: bool = False
    subid: Optional[str] = None