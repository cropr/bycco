# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

# all models in the service level exposed to the API
# we are using pydantic as tool

import logging

from typing import Dict, Any, List, Optional, Type
from pydantic import BaseModel

class BoardRoleIn(BaseModel):
    """
    contains the minimal fields to create a new boardrole
    """
    name: str


class BoardRoleOut(BaseModel):
    """
    A readonly view used for listing boardroles
    """
    i18n: Dict[str,str]
    id: str
    name: str

class BoardRoleSingleOut(BaseModel):
    role: BoardRoleOut 

class BoardRoleListOut(BaseModel):
    roles: List[BoardRoleOut]

class BoardRoleDetailedIn(BaseModel):
    """
    An update to a boardrole: all fields are optional
    """
    i18n: Optional[Dict[str,str]] = None
    name: Optional[str] = None

