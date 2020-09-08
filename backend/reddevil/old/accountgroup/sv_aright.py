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

from .md_agroup import (
    AccountGroupDetailedIn,
    AccountGroupIn,
    AccountGroupListOut,
    AccountGroupOut,
)

DbAccountGroup = resolve_method_module(
    f'reddevil.accountgroup.{cfg.DATASTORE["prefix"]}_agroup', 'DbAccountGroup')

def createAGroup(d: AccountGroupIn) -> str:
    """
    create a new AccountGroup returning its id
    """
    dd = d.dict()
    return DbAccountGroup.create_agroup(dd)

def deleteAGroup(id: str) -> None:
    DbAccountGroup.remove_agroup(id)

def getAGroup(id: str) -> AccountGroupOut:
    """
    get a Group
    """
    d = DbAccountGroup.find_agroup({'id': id})
    return AccountGroupOut(**d)

def getAGroups(options: Optional[dict] = {}) -> AccountGroupListOut:
    """
    get all Groups
    """
    ml = DbAccountGroup.find_agroups(options)
    return AccountGroupListOut(**{'groups': ml})


def updateAGroup(id: str, d: AccountGroupDetailedIn) -> AccountGroupOut:
    """
    update a Group
    """
    # import dates as isoformat string
    dd = d.dict(exclude_unset=True)
    ubm = DbAccountGroup.update_agroup(id, dd)
    return AccountGroupOut(**ubm)
