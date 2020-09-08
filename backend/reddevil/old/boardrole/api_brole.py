import logging
log = logging.getLogger('reddevil')

from fastapi import HTTPException
from pydantic import BaseModel
from typing import List, Optional
from ..common import app, url, RdException

from .sv_brole import (
    createBRole,
    deleteBRole,
    getBRoles,
    getBRole,
    updateBRole,
)
from .md_brole import (
    BoardRoleDetailedIn,
    BoardRoleIn,
    BoardRoleListOut,
    BoardRoleSingleOut,
)

assert app is not None

@app.get(url + '/brole', response_model=BoardRoleListOut)
def get_board_roles(options: Optional[dict] = None):
    try:
        return getBRoles(options)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call get_board_roles')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post(url + '/brole', response_model=str)
def create_board_role(br: BoardRoleIn):
    try:
        return createBRole(br)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call create_board_role')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get(url + '/brole/{id}', response_model=BoardRoleSingleOut)
def get_board_role(id: str):
    try:
        return BoardRoleSingleOut(role=getBRole(id))
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call get_board_role')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.delete(url + '/brole/{id}')
def delete_board_role(id: str):
    try:
        deleteBRole(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call delete_board_role')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.put(url + '/brole/{id}')
def update_board_role(id: str, bm: BoardRoleDetailedIn):
    try:
        updateBRole(id, bm)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call update_board_role')
        raise HTTPException(status_code=500, detail="Internal Server Error")

