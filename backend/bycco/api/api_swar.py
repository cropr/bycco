# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2020

import logging
from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List
from reddevil.common import RdException, bearer_schema
from bycco import app
from bycco.service.sv_swar import (
    addSwarTrn,
    getSwarTrn,
    getSwarTrns,
)
from bycco.models.md_swar import (
    SwarTrnIn,
    SwarTrnList,
    SwarTrnOut,
)
from reddevil.service.sv_account import validate_token

log = logging.getLogger('bycco')

@app.get('/api/swar', response_model=SwarTrnList)
async def api_getSwarTrns( 
        auth: HTTPAuthorizationCredentials=Depends(bearer_schema)):
    token = auth.credentials if auth else None
    if not token:
        raise HTTPException(status_code=401, detail='MissingToken')
    await validate_token(token)
    try:
        return await getSwarTrns()
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call get_subscriptions')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post('/api/swar', response_model=str)
async def api_addSwarTrn(sti: SwarTrnIn, 
        auth: HTTPAuthorizationCredentials=Depends(bearer_schema)):
    token = auth.credentials if auth else None
    if not token:
        raise HTTPException(status_code=401, detail='MissingToken')
    await validate_token(token)
    try:
        return await addSwarTrn(sti)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call get_subscriptions')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get('/api/swar/{id}', response_model=SwarTrnOut)
async def api_getSwarTrn(id: str,
        auth: HTTPAuthorizationCredentials=Depends(bearer_schema)):
    token = auth.credentials if auth else None
    if not token:
        raise HTTPException(status_code=401, detail='MissingToken')
    await validate_token(token)
    try:
        return await getSwarTrn(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call get_subscriptions')
        raise HTTPException(status_code=500, detail="Internal Server Error")
