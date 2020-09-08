# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging
log = logging.getLogger('reddevil')

import json
from datetime import datetime
from slugify import slugify
from base64 import b64decode
from fastapi.responses import Response
from mimetypes import guess_type
from typing import List, Optional, Union
from ..common import (
    cfg,
    iso2date,
    resolve_method_module, 
    RdInternalServerError, 
    RdBadRequest,
)

from .md_bmember import (
    BoardMemberDetailedIn,
    BoardMemberDetailedOut,
    BoardMemberIn,
    BoardMemberListOut,
    BoardMemberOut,    
)

DbBoardMember = resolve_method_module(
    f'reddevil.boardmember.{cfg.DATASTORE["prefix"]}_bmember', 'DbBoardMember')

def createBMember(d: BoardMemberIn) -> str:
    """
    create a new BoardMember returning its id
    """
    dd = d.dict()
    dd['picture'] = b''
    dd['picturemimetype'] = ''
    return DbBoardMember.create_bmember(dd)

def deleteBMember(id: str) -> None:
    DbBoardMember.remove_bmember(id)

def getBMember(id: str) -> BoardMemberDetailedOut:
    """
    get a member
    """
    d = DbBoardMember.find_bmember({'id': id})
    return BoardMemberDetailedOut(**d)

def getBMembers(options: dict) -> BoardMemberListOut:
    """
    get all members
    """
    ml = DbBoardMember.find_bmembers(options)
    return BoardMemberListOut(**{'members': ml})


def updateBMember(id: str, d: BoardMemberDetailedIn) -> BoardMemberDetailedOut:
    """
    update a member
    """
    # import dates as isoformat string
    dd = d.dict(exclude_unset=True)
    log.info(f'dd {dd}')
    picture = dd.pop('picture', None)
    name = dd.pop('picturename', 'fake.png')
    if picture:
        dd['picture'] = b64decode(picture)
        dd['picturemimetype'] = guess_type(name)[0] or ''
    ubm = DbBoardMember.update_bmember(id, dd)
    return BoardMemberDetailedOut(**ubm)

def getPicture(id: str, token: Optional[str]) -> Response:
    """
    get the picture 
    """
    log.info(f'getPicture {id}')
    d = DbBoardMember.find_bmember({
        'id': id,
        '_fieldlist': ['picture','picturemimetype']
    })
    return Response(content=d['picture'], 
                    media_type=d['picturemimetype'])
