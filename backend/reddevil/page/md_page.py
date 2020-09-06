# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

# all models in the service level exposed to the API
# we are using pydantic as tool

import logging

from datetime import datetime, date, timezone
from typing import Dict, Any, List, Optional, Type
from pydantic import BaseModel

class PageIn(BaseModel):
    """
    contains the minimal fields (doctype and name) to create a new page
    """
    doctype: str        # 'normal-page', 'article', 'app-page' 
    name: str

class PageOut(BaseModel):
    """
    A readonly view used for listing pages, contains only the basic fields
    """
    active: bool
    created_ts: datetime
    doctype: str
    enabled: Optional[bool] = False
    expired_ts: Optional[date]
    id: str
    name: str
    modified_ts: datetime
    published_ts: Optional[date]

class PageListOut(BaseModel):
    pages: List[PageOut]


class I18nFields(BaseModel):
    """
    contains the localized fields of a page
    """
    body: str
    intro: str 
    title: str

class PageI18nOut(BaseModel):
    """
    A localized readonly view of a page
    """
    active: bool
    body: str = ''
    component: str
    created_by: str = ' webmaster'
    created_ts: datetime
    id: str
    intro: str = ''
    locale: str
    name: str         
    modified_ts: datetime
    slug: str
    title: str = ''


class ArticleOut(BaseModel):
    """
    A readonly view used for getting the article title and intros
    """
    created_ts: datetime
    enabled: Optional[bool] = False
    expired_ts: Optional[date]
    page_i18n_fields: Dict[str, I18nFields] = {}
    id: str   
    languages: List[str]= ['en']
    name: str
    modified_ts: datetime
    published_ts: Optional[date]
    slug: str

class ArticleListOut(BaseModel):
    articles: List[ArticleOut]

class PageDetailedIn(BaseModel):
    """
    An update to a page: all fields are optional
    """
    component: Optional[str] = None
    created_by: Optional[str] = None
    doctype: Optional[str] = None 
    enabled: Optional[bool] = None
    expired_ts: Optional[date] = None
    page_i18n_fields: Optional[Dict[str, I18nFields]] = None
    id: Optional[str] = None
    languages: Optional[List[str]]
    name: Optional[str] = None
    published_ts: Optional[date] = None
    slug: Optional[str] = None

class PageDetailedOut(BaseModel):
    """
    An detailed view of a page 
    """
    active: bool
    component: str = 'CmsSimplePage'
    created_by: str = ' webmaster'
    created_ts: datetime
    doctype: str 
    enabled: bool = False
    expired_ts: Optional[date] = None
    page_i18n_fields: Dict[str, I18nFields] = {}
    id: str   
    languages: List[str]= ['en']
    name: str
    modified_ts: datetime
    published_ts: Optional[date] = None
    slug: str

class PageSingleOut(BaseModel):
    page: PageDetailedOut

class PageI18nSingleOut(BaseModel):
    page: PageI18nOut

class RoutingTableItem(BaseModel):
    component: str
    id: str
    slug: str

class RoutingTableListOut(BaseModel):
    routes: List[RoutingTableItem] 