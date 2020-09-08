# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging
log = logging.getLogger(__name__)

import json, os, os.path
from datetime import datetime

from base64 import b64encode, b64decode
from fastapi.responses import FileResponse
from mimetypes import guess_type
from random import randrange
from slugify import slugify
from typing import List, Optional, Union
from ..common import (
    cfg,
    iso2date,
    check_token,
    RdInternalServerError, 
    RdBadRequest,
)

from .md_file import (
    FileIn,
    FileOut,
    FileListOut,
    FileDetailedIn,
    FileSingleOut,
)
from .mongo_file import DbFile

def createFile(d: FileIn, token: str) -> str:
    """
    create a new File returning its id
    """
    ur = check_token(token)    
    dd = d.dict()
    ns = dd["name"].split('.')
    dd['url'] = f'{".".join(ns[0:-1])}__{randrange(1000000):06d}.{ns[-1]}'
    dd['path'] = os.path.join(cfg.FILESTORE, dd['url'])
    dd['mimetype'] = guess_type(dd['name'])[0]
    content = b64decode(dd.pop("content"))
    dd['filelength'] = len(content)
    rf = DbFile.create_file(dd)
    with open(dd["path"], 'wb') as f:
        f.write(content)
    return rf

def deleteFile(id: str, token: str) -> None:
    """
    delete a file, first update the database, then remove the fiel from fielsystem
    """
    ur = check_token(token)
    d = DbFile.find_file({'id': id})
    DbFile.remove_file(id)
    try:
        os.unlink(d["path"])
    except:
        pass

def getFile(id: str, token: str) -> FileOut:
    """
    get the file 
    """
    ur = check_token(token)
    d = DbFile.find_file({'id': id})
    return FileOut(**d)

def getFileContent(url: str, token: Optional[str]) -> FileResponse:
    """
    get the file 
    """
    log.info(f'getFile {url}')
    d = DbFile.find_file({'url': url})
    log.info(f' found file {d}')
    return FileResponse(path=d['path'], media_type=d['mimetype'])
    # return FileResponse(path=d['path'], media_type=d['mimetype'], 
    #     filename=d['name'])

def getFiles(options: dict, token: str) -> FileListOut:
    """
    get all the files
    """
    # ur = check_token(token)
    if 'reports' in options:
        options['_in'] = [('topic', ['Report Board Meeting', 'Report General Assembly'])]
    dl = DbFile.find_files(options)
    return FileListOut(files=dl)

def updateFile(id: str, d: FileDetailedIn, token: str) -> FileOut:
    """
    update a file ans it contents
    """
    # import dates as isoformat string
    log.info('trying to update file', d)
    ur = check_token(token)
    dd = d.dict(exclude_unset=True)
    content = None
    if 'name' in dd:
        name = f'{dd["name"]}__{randrange(1000000):06d}'
        dd['mimetype'] = guess_type(dd['name'])[0]
    if 'content' in dd:
        content = b64decode(dd.pop("content"))
        dd['filelength'] = len(content)
    udd = DbFile.update_file(id, dd)
    if content:
        with open(udd['path'], 'wb') as f:
            f.write(content)    
    return FileOut(**udd)

