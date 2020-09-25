# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging
log = logging.getLogger(__name__)

import json
import uuid
from datetime import datetime, timezone, date
from slugify import slugify
from typing import List, Optional, Union

from ..common import (
    cfg,
    iso2date,
    check_token,
    RdInternalServerError, 
    RdBadRequest,
)

from reddevil.models.md_page import (
    ArticleListOut,
    PageDetailedOut,
    PageIn,
    PageOut,
    PageListOut,
    PageUpdate,
    PageComponent,
    RoutingTableListOut,
    RoutingTableItem,
)
from reddevil.models.md_i18nfield import I18nField

from reddevil.crud.db_page import DbPage

def encode_page(e: dict, _class=PageDetailedOut):
    try:
        eo = _class(**e)
    except Exception:
        log.exception('cannot encode Page')
        raise RdInternalServerError(detail='CannotEncodePage')
    return eo

async def createPage(d: PageIn) -> str:
    """
    create a new Page returning its id
    """
    id = str(uuid.uuid4())
    title = {
        'default': I18nField(
            id=id,
            name='title',
            value=d.name,
        ).dict(),
        d.locale: I18nField(
            id=id,
            name='title',
            value=d.name,
        ).dict(),
    }
    body = {
        'default': I18nField(
            id=id,
            name='body',
            value='',
        ).dict(),
        d.locale: I18nField(
            id=id,
            name='body',
            value='',
        ).dict(),    
    }
    intro = {
        'default': I18nField(
            id=id,
            name='intro',
            value='',
        ).dict(),
        d.locale: I18nField(
            id=id,
            name='intro',
            value='',
        ).dict(),
    }
    tsnow = datetime.now(tz=timezone.utc)
    dd = d.dict()
    dd['id'] = id
    dd['body'] = body
    dd['component'] = PageComponent.CmsSimplePage
    dd['creationtime'] = tsnow
    dd['enabled'] = False
    dd['expirationdate'] = ''
    dd['intro'] = intro
    dd['languages'] = [d.locale]
    dd['modificationtime'] = tsnow
    dd['owner'] = ''
    dd['publicationdate'] = ''
    dd['slug'] = slugify(d.name)
    dd['title'] = title
    return await DbPage.add(dd)

async def deletePage(id: str) -> None:
    await DbPage.delete(id)

async def getPage(id: str, options: dict= {}) -> PageDetailedOut:
    """
    get the page 
    """
    _class = options.pop('_class', PageDetailedOut)
    filter = dict(id=id, **options)
    pdict = await DbPage.find_single(filter)
    pdict['active'] = isactive(pdict)
    return encode_page(pdict, _class)

async def getPageBySlug(slug: str, options: dict= {}):
    """
    get the page by slug 
    """
    _class = options.pop('_class', PageDetailedOut)
    filter = dict(slug=slug, **options)
    pdict = await DbPage.find_single(filter)
    pdict['active'] = isactive(pdict)
    return encode_page(pdict, _class)

async def getPages(options: dict={}) -> PageListOut:
    """
    get all the pages
    """
    _class = options.pop('_class', PageOut)
    docs = await DbPage.find_multiple(options)
    for d in docs:
        d['active'] = isactive(d)
    pages = [encode_page(d, _class) for d in docs]
    return PageListOut(pages=pages)    

async def updatePage(id: str, d: PageUpdate) -> PageDetailedOut:
    """
    update a page
    """
    dd = d.dict(exclude_unset=True)
    udd = await DbPage.update(id, dd)
    udd['active'] = isactive(udd)
    return encode_page(udd)

async def getRoutingTable() -> RoutingTableListOut:
    log.info('fetching routingtable form pages')
    docs = await DbPage.find_multiple({
        '_fieldlist': ['slug', 'component']
    })
    pages = [encode_page(d, RoutingTableItem) for d in docs]
    return RoutingTableListOut(routes=pages)

async def getActiveArticles(token: str=None) -> ArticleListOut:
    """
    get all the pages
    """
    dl = await DbPage.find_multiple({
        'doctype': 'article',
        'enabled': True,
        '_fieldlist': ["body", "creationtime", "enabled", "expirationdate", 
            "title", 
            "name", "modificationtime", "publicationdate", 'slug'],
        'publicationsdate': {'$ne': ""},
    })
    # ap = [x for x in dl if isactive(x)]
    ap = [x for x in dl]
    return ArticleListOut(articles=ap)

def isactive(dd: dict) -> bool:
    """
    checks whether a page is active
    """
    if not dd.get('enabled'):
        return False
    p = dd['publicationdate']
    e = dd['expirationdate']
    published = p and (date.fromisoformat(p) <= date.today())
    expired = e and (date.fromisoformat(e) < date.today())
    return bool( published and not expired)
