import logging
log = logging.getLogger('reddevil')

from fastapi import HTTPException
from pydantic import BaseModel
from typing import List, Optional
from ..common import app, url, RdException

from .sv_aright import (
    createARight,
    deleteARight,
    getARights,
    getARight,
    updateARight,
)
from .md_aright import (
    AccountRightDetailedIn,
    AccountRightIn,
    AccountRightListOut,
    AccountRightSingleOut,
)

assert app is not None

@app.get(url + '/aright', response_model=AccountRightListOut)
def get_account_rights(options: Optional[dict] = None):
    try:
        return getARights(options)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call get_account_rights')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post(url + '/aright', response_model=str)
def create_account_right(br: AccountRightIn):
    try:
        return createARight(br)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call create_account_right')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get(url + '/aright/{id}', response_model=AccountRightSingleOut)
def get_account_right(id: str):
    try:
        return AccountRightSingleOut(right=getARight(id))
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call get_account_right')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.delete(url + '/aright/{id}')
def delete_account_right(id: str):
    try:
        deleteARight(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call delete_account_right')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.put(url + '/aright/{id}')
def update_account_right(id: str, bm: AccountRightDetailedIn):
    try:
        updateARight(id, bm)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call update_account_right')
        raise HTTPException(status_code=500, detail="Internal Server Error")

