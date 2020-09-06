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

class AccountIn(BaseModel):
    """
    contains the minimal fields  to create a new account
    """
    enabled: bool = False
    logintype: LoginType    
    username: str

class AccountOut(BaseModel):
    """
    A readonly view used for listing pages, contains only the basic fields
    """
    username: str

class AccountDetailedIn(BaseModel):
    """
    contains the fields to update
    """
    domain: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    enabled: Optional[bool] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    locale: Optional[str] = None
    logintype: Optional[LoginType ] = None
    username: Optional[str] = None
    xtra: Optional[Dict[str,Any]] = None

class AccountListOut(BaseModel):
    accounts: List[AccountOut]

class AccountDetailedOut(BaseModel):
    """
    An detailed view of a page 
    """
    created_ts: datetime
    domain: str = ''
    email: str
    email_verified: bool = False
    enabled: bool = False
    first_name: str 
    last_name: str
    locale: str = ''
    logintype: LoginType 
    modified_ts: datetime
    password_expires_ts: Optional[datetime] = None
    username: str
    xtra: Dict[str,Any] = {}

class AccountSingleOut(BaseModel):
    account: AccountDetailedOut

class LoginIn(BaseModel):
    logintype: LoginType
    password: Optional[str]
    token: Optional[str]
    username: Optional[str]

class UserRights(BaseModel):
    access_rights: List[str] = []
    groups: List[str] = []
    id: str
    username: str
