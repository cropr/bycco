import logging
log = logging.getLogger('reddevil')

from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List
from ..common import app, url, RdException, bearer_schema

from .sv_page import (
    createPage,
    deletePage,
    getLocalizedPage,
    getPage,
    getPages,
    getPageBySlug,
    getRoutingTable,
    updatePage,
    getActiveArticles,
)
from .md_page import (
    ArticleListOut,
    PageIn,
    PageListOut,
    PageDetailedIn,
    PageSingleOut,
    PageI18nSingleOut,
    RoutingTableListOut,
)

assert app is not None


@app.get(url + '/page', response_model=PageListOut)
def get_pages(options:dict = {}, 
              auth: HTTPAuthorizationCredentials=Depends(bearer_schema)):
    if not auth:
        raise HTTPException(status_code=401, detail='MissingToken')
    try:
        return getPages(options, auth.credentials)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call get_pages')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post(url + '/page', response_model=str)
def create_page(p: PageIn, 
                auth: HTTPAuthorizationCredentials=Depends(bearer_schema)):
    if not auth:
        raise HTTPException(status_code=401, detail='MissingToken')
    try:
        return createPage(p, auth.credentials)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call create_page')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get(url + '/page/{id}', response_model=PageSingleOut)
def get_page(id: str, 
             auth: HTTPAuthorizationCredentials=Depends(bearer_schema)):
    if not auth:
        raise HTTPException(status_code=401, detail='MissingToken')
    try:
        page = getPage(id, auth.credentials)
        return PageSingleOut(page=page)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call get_page')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.delete(url + '/page/{id}')
def delete_page(id: str,  
                auth: HTTPAuthorizationCredentials=Depends(bearer_schema)):
    if not auth:
        raise HTTPException(status_code=401, detail='MissingToken')
    try:
        deletePage(id, auth.credentials)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call delete_page')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.put(url + '/page/{id}')
def update_page(id: str, p: PageDetailedIn,  
                auth: HTTPAuthorizationCredentials=Depends(bearer_schema)):
    if not auth:
        raise HTTPException(status_code=401, detail='MissingToken')
    try:
        updatePage(id, p, auth.credentials)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call update_page')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get(url + '/routingtable', response_model=RoutingTableListOut)
def get_routingtable():
    try:
        return getRoutingTable()
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call get_routingtable')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get(url + '/slug/{slug}/locale/{locale}', 
    response_model=PageI18nSingleOut)
def get_localized_page(slug: str, locale: str,  
                       auth: HTTPAuthorizationCredentials=Depends(bearer_schema)):
    try:
        page = getLocalizedPage(slug, locale)
        return PageI18nSingleOut(page=page)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call get_localized_page')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get(url + '/slug/{slug}', 
    response_model=PageSingleOut)
def get_page_by_slug(slug: str,   
                    auth: HTTPAuthorizationCredentials=Depends(bearer_schema)):
    try:
        page = getPageBySlug(slug)
        return PageSingleOut(page=page)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call get_localized_page')
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get(url + '/active-articles', response_model=ArticleListOut)
def get_activearticles(auth: HTTPAuthorizationCredentials=Depends(bearer_schema)):
    token = auth.credentials if auth else None
    try:
        return getActiveArticles(token)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        log.exception('failed api call get_activearticles')
        raise HTTPException(status_code=500, detail="Internal Server Error") 