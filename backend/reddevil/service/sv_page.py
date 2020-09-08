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
    PageI18nOut,
    PageListOut,
    PageUpdate,
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
    tsnow = datetime.now(tz=timezone.utc)
    dd = d.dict()
    dd['id'] = str(uuid.uuid4())
    dd['body'] = {}
    dd['component'] = ''
    dd['creationtime'] = tsnow
    dd['enabled'] = False
    dd['expirationdate'] = ''
    dd['intro'] = {}
    dd['languages'] = [d.locale]
    dd['modificationtime'] = tsnow
    dd['owner'] = ''
    dd['publicationdate'] = ''
    dd['slug'] = slugify(d.name)
    dd['title'] = {}
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
    log.info(f'pdict {pdict}')
    return encode_page(pdict, _class)

async def getPages(options: dict) -> PageListOut:
    """
    get all the pages
    """
    _class = options.pop('_class', PageOut)
    docs = await DbPage.find_multiple(options)
    for d in docs:
        d['active'] = isactive(d)
    pages = [encode_page(e, _class) for e in evs]
    return PageListOut(pages=pages)    

async def getLocalizedPage(slug: str, locale: str) -> PageI18nOut:
    """
    get the localized content of a page
    """
    _class = options.pop('_class', PageI18nOut)
    filter = dict(slug=slug, locale=locale, **options)
    pdict = await DbPage.find_single(filter)
    return encode_page(pdict, _class)

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
