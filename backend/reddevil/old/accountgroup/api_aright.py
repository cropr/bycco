# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2020

import logging
log = logging.getLogger('reddevil')

from fastapi import HTTPException
from pydantic import BaseModel
from typing import List, Optional
from ..common import app, url, RdException

from .sv_agroup import (
    createAGroup,
    deleteAGroup,
    getAGroups,
    getAGroup,
    updateAGroup,
)
from .md_agroup import (
    AccountGroupDetailedIn,
    AccountGroupIn,
    AccountGroupListOut,
    AccountGroupSingleOut,
)

assert app is not None

@app.get(url + '/agroup', response_model=AccountGroupListOut)
def get_account_groups(options: Optional[dict] = None):
    try:
        return getAGroups(options)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call get_account_groups')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post(url + '/agroup', response_model=str)
def create_account_group(br: AccountGroupIn):
    try:
        return createAGroup(br)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call create_account_group')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get(url + '/agroup/{id}', response_model=AccountGroupSingleOut)
def get_account_group(id: str):
    try:
        return AccountGroupSingleOut(group=getAGroup(id))
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call get_account_group')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.delete(url + '/agroup/{id}')
def delete_account_group(id: str):
    try:
        deleteAGroup(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call delete_account_group')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.put(url + '/agroup/{id}')
def update_account_group(id: str, bm: AccountGroupDetailedIn):
    try:
        updateAGroup(id, bm)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call update_account_group')
        raise HTTPException(status_code=500, detail="Internal Server Error")

