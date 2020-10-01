# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2020

import logging
log = logging.getLogger('reddevil')

from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List
from reddevil.common import app, url, RdException

from reddevil.service.sv_account import (
    createAccount,
    deleteAccount,
    getAccount,
    getAccounts,
    updateAccount,
    login_account,
    bearer_schema,
)
from reddevil.models.md_account import (
    AccountIn,
    AccountListOut,
    AccountDetailedIn,
    AccountDetailedOut,
    LoginIn,
)

assert app is not None

@app.get(url + '/account', response_model=AccountListOut)
async def api_get_accounts(options:dict = {}, 
        auth: HTTPAuthorizationCredentials=Depends(bearer_schema)):
    token = auth.credentials if auth else None
    try:
        return await getAccounts(options)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call get_accounts')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post(url + '/account', response_model=str)
async def api_add_account(a: AccountIn,  
        auth: HTTPAuthorizationCredentials=Depends(bearer_schema)):
    token = auth.credentials if auth else None
    try:
        return await createAccount(a)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call create_account')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get(url + '/account/{id}', response_model=AccountDetailedOut)
async def api_get_account(id: str,  
        auth: HTTPAuthorizationCredentials=Depends(bearer_schema)):
    token = auth.credentials if auth else None
    try:
        return await getAccount(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call get_account')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.delete(url + '/account/{id}')
async def api_delete_account(id: str,  
        auth: HTTPAuthorizationCredentials=Depends(bearer_schema)):
    token = auth.credentials if auth else None
    try:
        await deleteAccount(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call delete_account')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.put(url + '/account/{id}')
async def api_update_account(id: str, p: AccountDetailedIn,  
        auth: HTTPAuthorizationCredentials=Depends(bearer_schema)):
    token = auth.credentials if auth else None
    try:
        await updateAccount(id, p)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call update_account')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post(url + '/login', response_model=str)
async def api_login(li: LoginIn):
    try:
        return await login_account(li)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call login')
        raise HTTPException(status_code=500, detail="Internal Server Error")

