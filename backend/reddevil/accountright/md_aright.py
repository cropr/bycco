# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

# all models in the service level exposed to the API
# we are using pydantic as tool

import logging

from typing import Dict, Any, List, Optional, Type
from pydantic import BaseModel

class AccountRightIn(BaseModel):
    """
    contains the minimal fields to create a new account right
    """
    name: str


class AccountRightOut(BaseModel):
    """
    A readonly view used for listing account rights
    """
    i18n: Dict[str,str]
    id: str
    name: str

class AccountRightSingleOut(BaseModel):
    right: AccountRightOut 

class AccountRightListOut(BaseModel):
    rights: List[AccountRightOut]

class AccountRightDetailedIn(BaseModel):
    """
    An update to a account right: all fields are optional
    """
    i18n: Optional[Dict[str,str]] = None
    name: Optional[str] = None

