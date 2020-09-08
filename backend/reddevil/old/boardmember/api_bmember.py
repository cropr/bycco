import logging
log = logging.getLogger('reddevil')

from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional
from ..common import app, url, RdException, bearer_schema

from .sv_bmember import (
    createBMember,
    deleteBMember,
    getBMembers,
    getBMember,
    updateBMember,
    getPicture,
)
from .md_bmember import (
    BoardMemberIn,
    BoardMemberSingleOut,
    BoardMemberDetailedIn,
    BoardMemberDetailedOut,
    BoardMemberListOut
)

assert app is not None

@app.get(url + '/bmember', response_model=BoardMemberListOut)
def get_board_members(options:dict = {}, 
        auth: HTTPAuthorizationCredentials=Depends(bearer_schema)):
    token = auth.credentials if auth else None
    try:
        return getBMembers(options or {})
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call get_board_members')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post(url + '/bmember', response_model=str)
def create_board_member(bm: BoardMemberIn,  
        auth: HTTPAuthorizationCredentials=Depends(bearer_schema)):
    if not auth:
        raise HTTPException(status_code=401, detail='MissingToken')
    try:
        return createBMember(bm)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call create_board_member')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get(url + '/bmember/{id}', response_model=BoardMemberSingleOut)
def get_board_member(id: str, 
        auth: HTTPAuthorizationCredentials=Depends(bearer_schema)):
    token = auth.credentials if auth else None
    try:
        return BoardMemberSingleOut(member=getBMember(id))
    except RdException as e:
        log.info('RdException')
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.info('Other Exception')
        log.exception('failed api call get_board_member')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.delete(url + '/bmember/{id}')
def delete_board_member(id: str, 
        auth: HTTPAuthorizationCredentials=Depends(bearer_schema)):
    if not auth:
        raise HTTPException(status_code=401, detail='MissingToken')
    try:
        deleteBMember(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call delete_board_member')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.put(url + '/bmember/{id}')
def update_board_member(id: str, bm: BoardMemberDetailedIn, 
        auth: HTTPAuthorizationCredentials=Depends(bearer_schema)):
    if not auth:
        raise HTTPException(status_code=401, detail='MissingToken')
    try:
        updateBMember(id, bm)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call update_board_member')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get(url + '/picture/{id}')
def get_picture(id: str, 
        auth: HTTPAuthorizationCredentials=Depends(bearer_schema)):
    log.info('getting picture member')
    token = auth.credentials if auth else None
    try:
        return getPicture(id, token)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call get_filecontent')
        raise HTTPException(status_code=500, detail="Internal Server Error!") 