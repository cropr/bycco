import logging
log = logging.getLogger('reddevil')

from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List
from ..common import (
    app, 
    url, 
    RdException, 
    oauth2_scheme, oauth2_optional,
    bearer_schema,
)

from .sv_file import (
    createFile,
    deleteFile,
    getFile,
    getFileContent,
    getFiles,
    updateFile,
)
from .md_file import (
    FileIn,
    FileListOut,
    FileDetailedIn,
    FileSingleOut,
)

assert app is not None


@app.get(url + '/file', response_model=FileListOut)
def get_files(reports: int=0, auth: HTTPAuthorizationCredentials=Depends(bearer_schema)):
    token = auth.credentials if auth else None
    try:
        options = {}
        if reports:
            options['reports'] = True
        return getFiles(options, token)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call get_files')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post(url + '/file', response_model=str)
def create_file(p: FileIn, auth: HTTPAuthorizationCredentials=Depends(bearer_schema)):
    if not auth:
        raise HTTPException(status_code=401, detail='MissingToken')
    try:
        return createFile(p, auth.credentials)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call create_file')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get(url + '/file/{id}', response_model=FileSingleOut)
def get_file(id: str, auth: HTTPAuthorizationCredentials=Depends(bearer_schema)):
    log.info('getting file')
    if not auth:
        raise HTTPException(status_code=401, detail='MissingToken')
    try:
        file = getFile(id, auth.credentials)
        return FileSingleOut(file=file)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call get_file')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.delete(url + '/file/{id}')
def delete_file(id: str, auth: HTTPAuthorizationCredentials=Depends(bearer_schema)):
    log.info('deleting file')
    if not auth:
        raise HTTPException(status_code=401, detail='MissingToken')
    try:
        deleteFile(id, auth.credentials)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call delete_file')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.put(url + '/file/{id}')
def update_file(id: str, p: FileDetailedIn, 
        auth: HTTPAuthorizationCredentials=Depends(bearer_schema)):
    log.info('updating file')
    if not auth:
        raise HTTPException(status_code=401, detail='MissingToken')
    try:
        updateFile(id, p, auth.credentials)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call update_file')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get(url + '/filecontent/{url}')
def get_filecontent(url: str, 
        auth: HTTPAuthorizationCredentials=Depends(bearer_schema)):
    log.info('getting file content')
    token = auth.credentials if auth else None
    try:
        return getFileContent(url, token)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call get_filecontent')
        raise HTTPException(status_code=500, detail="Internal Server Error!") 