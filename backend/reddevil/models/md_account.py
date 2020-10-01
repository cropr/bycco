# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

# all models in the service level exposed to the API
# we are using pydantic as tool

from datetime import datetime, date, timezone
from typing import Dict, Any, List, Optional, Type
from enum import Enum
from pydantic import BaseModel

class LoginType(str, Enum):
    email = 'email'
    facebook = 'facebook'
    google = 'google'

class Account(BaseModel):
    """
    contains the fields as registered in the database
    """
    domain: str
    email: str
    email_verified: bool
    enabled: bool
    first_name: str
    groups: str                 # comma separated list of groups
    last_name: str
    locale: str
    logintype: LoginType
    password_expiration_time: datetime
    scopes: str                 # comma separated list of scopes
    superuser: bool
    tokensalt: str
    xtra: Dict[str,Any]
    _id: str
    _documenttype: str
    _version: int
    _creationtime: datetime
    _modificationtime: datetime 


class AccountIn(BaseModel):
    """
    contains the minimal fields  to create a new account
    """
    enabled: bool = False
    logintype: LoginType    
    id: str

class AccountOut(BaseModel):
    """
    A readonly view used for listing pages, contains only the basic fields
    """
    id: str

class AccountDetailedIn(BaseModel):
    """
    contains the fields to update
    """
    domain: Optional[str] = None
    enabled: Optional[bool] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    locale: Optional[str] = None
    logintype: Optional[LoginType ] = None
    xtra: Optional[Dict[str,Any]] = None

class AccountListOut(BaseModel):
    accounts: List[AccountOut]

class AccountDetailedOut(BaseModel):
    """
    An detailed view of a page 
    """
    _creationtime: datetime
    domain: str = ''
    email: str
    email_verified: bool = False
    enabled: bool = False
    first_name: str
    id: str 
    last_name: str
    locale: str = ''
    logintype: LoginType 
    _modificationtime: datetime
    password_expiration_time: Optional[datetime] = None
    xtra: Dict[str,Any] = {}

class AccountOptional(BaseModel):
    """
    An detailed view of a page 
    """
    _creationtime: Optional[datetime] = None
    domain: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    enabled: Optional[bool] = None
    first_name: Optional[str] = None
    id: str 
    last_name: Optional[str] = None
    locale: Optional[str] = None
    logintype: Optional[LoginType] = None
    _modificationtime: Optional[datetime] = None
    password_expirationtime: Optional[datetime] = None
    superuser: Optional[bool] = None
    tokensalt: Optional[str] = None
    _version: Optional[int] = None
    xtra: Optional[Dict[str,Any]] = None

class LoginIn(BaseModel):
    logintype: LoginType
    password: Optional[str]
    token: Optional[str]
    username: Optional[str]

class Scope(BaseModel):
    name: str
    permission: str

class Group(BaseModel):
    name: str
    scopes: List[Scope]