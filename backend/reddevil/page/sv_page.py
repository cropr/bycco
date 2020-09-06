# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging
log = logging.getLogger(__name__)

import json

from datetime import datetime
from slugify import slugify
from typing import List, Optional, Union
from ..common import (
    cfg,
    iso2date,
    check_token,
    RdInternalServerError, 
    RdBadRequest,
)

from .md_page import (
    ArticleListOut,
    PageDetailedIn,
    PageDetailedOut,
    PageIn,
    PageI18nOut,
    PageListOut,
    RoutingTableListOut,
)
from .helpers import isactive

from .mongo_page import DbPage

def createPage(d: PageIn, token: str) -> str:
    """
    create a new Page returning its id
    """
    ur = check_token(token)    
    dd = d.dict()
    dd['slug'] = slugify(d.name)
    return DbPage.create_page(dd)

def deletePage(id: str, token: str) -> None:
    ur = check_token(token)
    DbPage.remove_page(id)

def getPage(id: str, token: str) -> PageDetailedOut:
    """
    get the page 
    """
    d = DbPage.find_page({'id': id})
    d['active'] = isactive(d)
    log.debug(f'getPage {d}')
    return PageDetailedOut(**d)

def getPageBySlug(slug: str):
    """
    get the page by slug 
    """
    d = DbPage.find_page({'slug': slug})
    d['active'] = isactive(d)
    return PageDetailedOut(**d)

def getPages(options: dict, token: str) -> PageListOut:
    """
    get all the pages
    """
    ur = check_token(token)
    dl = DbPage.find_pages(options)
    for d in dl:
        d['active'] = isactive(d)
    return PageListOut(pages=dl)

def getLocalizedPage(slug: str, locale: str) -> PageI18nOut:
    """
    get the localized content of a page
    """
    d = DbPage.find_page({'slug': slug, 'locale': locale})
    d['active'] = isactive(d)
    return PageI18nOut(**d)

def updatePage(id: str, d: PageDetailedIn, token: str) -> PageDetailedOut:
    """
    update a page
    """
    # import dates as isoformat string
    ur = check_token(token)
    dd = d.dict(exclude_unset=True)
    udd = DbPage.update_page(id, dd)
    udd['active'] = isactive(udd)
    return PageDetailedOut(**udd)

def getRoutingTable():
    dl = DbPage.find_pages({
        '_fieldlist': ['slug', 'component']
    })
    return RoutingTableListOut(routes=dl)

def getActiveArticles(token: str=None) -> ArticleListOut:
    """
    get all the pages
    """
    dl = DbPage.find_pages({
        'doctype': 'article',
        'enabled': True,
        '_fieldlist': ["created_ts", "enabled", "expired_ts", "page_i18n_fields",
            "languages", "name", "modified_ts", "published_ts", 'slug'],
        '_order': [('published_ts', -1)],
        '_exists': ['published_ts'],
    })
    # ap = [x for x in dl if isactive(x)]
    ap = [x for x in dl]
    return ArticleListOut(articles=ap)