# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

# all models in the service level exposed to the API
# we are using pydantic as tool

import logging

from typing import Dict, Any, List, Optional, Type
from pydantic import BaseModel

class AccountGroupIn(BaseModel):
    """
    contains the minimal fields to create a new account group
    """
    name: str


class AccountGroupOut(BaseModel):
    """
    A readonly view used for listing account groups
    """
    i18n: Dict[str,str]
    id: str
    name: str
    rights: List[str]
    

class AccountGroupSingleOut(BaseModel):
    group: AccountGroupOut 


class AccountGroupListOut(BaseModel):
    groups: List[AccountGroupOut]


class AccountGroupDetailedIn(BaseModel):
    """
    An update to a account group: all fields are optional
    """
    i18n: Optional[Dict[str,str]] = None
    name: Optional[str] = None
    rights: Optional[List[str]] = None
    

