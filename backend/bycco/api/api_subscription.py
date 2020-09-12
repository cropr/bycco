# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2020

from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List
from reddevil.common import RdException, bearer_schema
from bycco import app
from bycco.service.sv_subscription import (
    addSubscription,
    confirmSubscription,
    deleteSubscription,
    getSubscription,
    getSubscriptions,
    updateSubscription,
    checkId,
)
from bycco.models.md_subscription import (
    SubscriptionIn,
    SubscriptionCategory,
    SubscriptionList,
    SubscriptionDetailedOut,
    SubscriptionOut,
    SubscriptionOptional,
)

@app.get('/api/subscription', response_model=SubscriptionList)
async def api_get_subscriptions( 
        auth: HTTPAuthorizationCredentials=Depends(bearer_schema)):
    token = auth.credentials if auth else None
    try:
        return await getSubscriptions()
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call get_subscriptions')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get('/api/a/subscription', response_model=SubscriptionList)
async def api_anon_get_subscriptions():
    try:
        return await getSubscriptions()
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call get_subscriptions')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post('/api/a/subscription', response_model=str)
async def api_add_subscriptiob(s: SubscriptionIn):
    try:
        return await addSubscription(s)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call create_subscription')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get('/api/subscription/{id}')
async def api_get_subscription(id: str, 
             auth: HTTPAuthorizationCredentials=Depends(bearer_schema)):
    token = auth.credentials if auth else None
    try:
        return await getSubscription(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call get_subscription')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get('/api/a/subscription/{id}')
async def api_anon_get_subscription(id: str):
    try:
        return await getSubscription(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call get_subscription')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.delete('/api/subscription/{id}')
async def api_delete_subscription(id: str,  
        auth: HTTPAuthorizationCredentials=Depends(bearer_schema)):
    token = auth.credentials if auth else None
    try:
        await deleteSubscription(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call delete_subscription')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.put('/api/subscrconfirmSubscription
        log.exception('failed api call update_subscription')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get('/api/a/subscription/{id}/confirm')
async def api_anon_confirm_subscription(id: str):
    try:
        return await confirmSubscription(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call get_subscription')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get('/api/a/subscription/{idbel}/check')
async def api_anon_confirm_subscription(idbel: str):
    try:
        return await checkId(idbel)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call get_subscription')
        raise HTTPException(status_code=500, detail="Internal Server Error")
