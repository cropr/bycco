# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging
log = logging.getLogger('reddevil')

import json
from datetime import datetime
from slugify import slugify
from typing import List, Optional, Union
from ..common import (
    cfg,
    iso2date,
    resolve_method_module, 
    RdInternalServerError, 
    RdBadRequest,
)

from .md_brole import (
    BoardRoleDetailedIn,
    BoardRoleIn,
    BoardRoleListOut,
    BoardRoleOut,
)

DbBoardRole = resolve_method_module(
    f'reddevil.boardrole.{cfg.DATASTORE["prefix"]}_brole', 'DbBoardRole')

def createBRole(d: BoardRoleIn) -> str:
    """
    create a new BoardRole returning its id
    """
    dd = d.dict()
    return DbBoardRole.create_brole(dd)

def deleteBRole(id: str) -> None:
    DbBoardRole.remove_brole(id)

def getBRole(id: str) -> BoardRoleOut:
    """
    get a Role
    """
    d = DbBoardRole.find_brole({'id': id})
    return BoardRoleOut(**d)

def getBRoles(options: Optional[dict] = {}) -> BoardRoleListOut:
    """
    get all Roles
    """
    ml = DbBoardRole.find_broles(options)
    return BoardRoleListOut(**{'roles': ml})


def updateBRole(id: str, d: BoardRoleDetailedIn) -> BoardRoleOut:
    """
    update a Role
    """
    # import dates as isoformat string
    dd = d.dict(exclude_unset=True)
    ubm = DbBoardRole.update_brole(id, dd)
    return BoardRoleOut(**ubm)
