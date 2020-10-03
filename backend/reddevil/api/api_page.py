import logging
log = logging.getLogger('reddevil')

from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List
from reddevil.common import app, url, RdException, bearer_schema

from reddevil.service.sv_page import (
    createPage,
    deletePage,
    getPage,
    getPages,
    getPageBySlug,
    getRoutingTable,
    updatePage,
    getActiveArticles,
    backupPages,
)
from reddevil.service.sv_account import validate_token
from reddevil.models.md_page import (
    ArticleListOut,
    PageIn,
    PageListOut,
    PageOptional,
    PageUpdate,
    PageSingleOut,
    RoutingTableListOut,
)

assert app is not None

@app.get(url + '/pages', response_model=PageListOut)
async def api_get_pages( 
        auth: HTTPAuthorizationCredentials=Depends(bearer_schema)):
    token = auth.credentials if auth else None
    if not token:
        raise HTTPException(status_code=401, detail='MissingToken')
    await validate_token(token)
    try:
        return await getPages()
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call get_pages')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get(url + '/a/pages', response_model=PageListOut)
async def api_anon_get_pages():
    log.info(f'options {options}')
    try:
        return await getPages()
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call get_pages')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post(url + '/pages/backup', response_model=List[PageOptional])
async def api_backup_pages( 
        auth: HTTPAuthorizationCredentials=Depends(bearer_schema)):
    token = auth.credentials if auth else None
    if not token:
        raise HTTPException(status_code=401, detail='MissingToken')
    await validate_token(token)
    try:
        return await backupPages()
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call get_pages')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post(url + '/pages/restore', response_model=PageListOut)
async def api_restore_pages( 
        auth: HTTPAuthorizationCredentials=Depends(bearer_schema)):
    token = auth.credentials if auth else None
    if not token:
        raise HTTPException(status_code=401, detail='MissingToken')
    await validate_token(token)
    try:
        return await getPages()
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call get_pages')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post(url + '/page', response_model=str)
async def api_add_page(p: PageIn, 
        auth: HTTPAuthorizationCredentials=Depends(bearer_schema)):
    token = auth.credentials if auth else None
    if not token:
        raise HTTPException(status_code=401, detail='MissingToken')
    await validate_token(token)
    try:
        return await createPage(p)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call create_page')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get(url + '/page/{id}')
async def api_get_page(id: str, 
             auth: HTTPAuthorizationCredentials=Depends(bearer_schema)):
    token = auth.credentials if auth else None
    if not token:
        raise HTTPException(status_code=401, detail='MissingToken')
    await validate_token(token)
    try:
        return await getPage(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call get_page')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get(url + '/a/page/{id}')
async def api_anon_get_page(id: str):
    try:
        return await getPage(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call get_page')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.delete(url + '/page/{id}')
async def api_delete_page(id: str,  
        auth: HTTPAuthorizationCredentials=Depends(bearer_schema)):
    token = auth.credentials if auth else None
    if not token:
        raise HTTPException(status_code=401, detail='MissingToken')
    await validate_token(token)
    try:
        await deletePage(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call delete_page')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.put(url + '/page/{id}')
async def api_update_page(id: str, p: PageUpdate,  
                auth: HTTPAuthorizationCredentials=Depends(bearer_schema)):
    token = auth.credentials if auth else None
    if not token:
        raise HTTPException(status_code=401, detail='MissingToken')
    await validate_token(token)
    try:
        await updatePage(id, p)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call update_page')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get(url + '/a/routingtable', response_model=RoutingTableListOut)
async def api_anon_routingtable():
    try:
        return await getRoutingTable()
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call get_routingtable')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get(url + '/a/slug/{slug}')
async def api_anon_slug_page(slug: str):
    try:
        return await getPageBySlug(slug)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call get_localized_page')
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get(url + '/a/articles')
async def api_anon_get_articles():
    try:
        return await getActiveArticles()
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call get_activearticles')
        raise HTTPException(status_code=500, detail="Internal Server Error") 
