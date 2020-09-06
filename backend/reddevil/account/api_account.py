# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2020

import logging
log = logging.getLogger('reddevil')

from fastapi import HTTPException
from pydantic import BaseModel
from typing import List
from ..common import app, url, RdException

from .sv_account import (
    createAccount,
    deleteAccount,
    getAccount,
    getAccounts,
    updateAccount,
    loginAccount,
)
from .md_account import (
    AccountIn,
    AccountListOut,
    AccountDetailedIn,
    AccountSingleOut,
    LoginIn,
)

assert app is not None

@app.get(url + '/account', response_model=AccountListOut)
def get_accounts(options:dict = {}):
    try:
        return getAccounts(options)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call get_accounts')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post(url + '/account', response_model=str)
def create_account(a: AccountIn):
    try:
        return createAccount(a)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call create_account')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get(url + '/account/{id}', response_model=AccountSingleOut)
def get_account(id: str):
    try:
        return AccountSingleOut(account=getAccount(id))
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call get_account')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.delete(url + '/account/{id}')
def delete_account(id: str):
    try:
        deleteAccount(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call delete_account')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.put(url + '/account/{id}')
def update_account(id: str, p: AccountDetailedIn):
    try:
        updateAccount(id, p)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call update_account')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post(url + '/login')
def login(li: LoginIn):
    try:
        return loginAccount(li)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call update_account')
        raise HTTPException(status_code=500, detail="Internal Server Error")

