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

from .md_aright import (
    AccountRightDetailedIn,
    AccountRightIn,
    AccountRightListOut,
    AccountRightOut,
)

DbAccountRight = resolve_method_module(
    f'reddevil.accountright.{cfg.DATASTORE["prefix"]}_aright', 'DbAccountRight')

def createARight(d: AccountRightIn) -> str:
    """
    create a new AccountRight returning its id
    """
    dd = d.dict()
    return DbAccountRight.create_aright(dd)

def deleteARight(id: str) -> None:
    DbAccountRight.remove_aright(id)

def getARight(id: str) -> AccountRightOut:
    """
    get a Role
    """
    d = DbAccountRight.find_aright({'id': id})
    return AccountRightOut(**d)

def getARights(options: Optional[dict] = {}) -> AccountRightListOut:
    """
    get all Roles
    """
    ml = DbAccountRight.find_arights(options)
    return AccountRightListOut(**{'rights': ml})


def updateARight(id: str, d: AccountRightDetailedIn) -> AccountRightOut:
    """
    update a Role
    """
    # import dates as isoformat string
    dd = d.dict(exclude_unset=True)
    ubm = DbAccountRight.update_aright(id, dd)
    return AccountRightOut(**ubm)
