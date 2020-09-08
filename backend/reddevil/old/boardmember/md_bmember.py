# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

# all models in the service level exposed to the API
# we are using pydantic as tool

import logging

from typing import Dict, Any, List, Optional, Type
from pydantic import BaseModel

class BoardMemberIn(BaseModel):
    """
    contains the required fields to create a new boardmember
    """
    boardroles: List[str] = []
    first_name: str
    last_name: str
    enabled: bool = True
    email: str
    membertype: str = 'board'  # mandated or board, 
    mobile: str
    priority: int = 0
    showemail: bool = True
    showmobile: bool = True


class BoardMemberOut(BaseModel):
    """
    A readonly view used for listing boardmembers
    """
    boardroles: List[str]
    email: str
    enabled: bool
    first_name: str
    id: str
    last_name: str
    membertype: str
    mobile: str
    priority: int
    showemail: bool
    showmobile: bool

class BoardMemberSingleOut(BaseModel):
    member: BoardMemberOut 

class BoardMemberListOut(BaseModel):
    members: List[BoardMemberOut]

class BoardMemberDetailedIn(BaseModel):
    """
    An update to a boardmember: all fields are optional
    """
    boardroles: Optional[List[str]] = None
    email: Optional[str] = None
    enabled: Optional[bool] = None
    first_name: Optional[str] = None
    id: Optional[str] = None
    last_name: Optional[str] = None
    membertype: Optional[str] = None
    mobile: Optional[str] = None
    picture: Optional[bytes] = None
    picturename: Optional[str] = None
    picturemimetype: Optional[str] = None
    priority: Optional[int] = None
    showemail: Optional[bool] = True
    showmobile: Optional[bool] = True    

class BoardMemberDetailedOut(BaseModel):
    """
    An detailed view of a boardmember, including picture 
    """
    boardroles: List[str]
    email: str
    enabled: bool
    first_name: str
    id: str
    last_name: str
    membertype: str
    mobile: str = ''
    picture: bytes 
    picturemimetype: str 
    priority: int
    showemail: bool 
    showmobile: bool 
