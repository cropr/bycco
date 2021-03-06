# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2020

# all models in the service level exposed to the API
# we are using pydantic as tool

import logging

from datetime import datetime
from typing import Dict, Any, List, Optional, Type
from enum import Enum
from pydantic import BaseModel
from .md_i18nfield import I18nField

class PageComponent(str, Enum):
    CmsSimplePage = 'CmsSimplePage'
    LandingPage = 'LandingPage'
    MulitLocalePage = 'MultiLocalePage'
    Agenda = 'Agenda'
    Subscription = 'Subscription'
    Participants = 'Participants'


class Page(BaseModel):
    """
    a Page as written in database
    """
    body: Dict[str, I18nField]
    component: PageComponent
    doctype: str
    enabled: bool
    expirationdate: str             # format yyyy-mm-dd
    intro: Dict[str, I18nField]
    name: str
    owner: str 
    publicationdate: str            # format yyyy-mm-dd
    slug: str
    title: Dict[str, I18nField]  
    _id: str
    _version: int
    _documenttype: str
    _creationtime: datetime
    _modificationtime: datetime

    # deprecated fields bo longer in use since version 2
    creationtime: datetime
    modificationtime: datetime


class PageOptional(BaseModel):
    """
    a Page with all fields Optional so we can work on raw database documents
    id and _id are boith provided for maximum flexibility
    """
    body: Optional[Dict[str, I18nField]] = None
    component: Optional[PageComponent] = None
    doctype: Optional[str] = None
    enabled: Optional[bool] = None
    expirationdate: Optional[str] = None          # format yyyy-mm-dd
    intro: Optional[Dict[str, I18nField]] = None
    name: Optional[str] = None
    owner: Optional[str] = None 
    publicationdate: Optional[str] = None         # format yyyy-mm-dd
    slug: Optional[str] = None
    title: Optional[Dict[str, I18nField]] = None
    _id: Optional[str] = None
    _version: Optional[int] = None
    _documenttype: Optional[str] = None
    _creationtime: Optional[datetime] = None
    _modificationtime: Optional[datetime] = None

    # fields not in the database but used at service level
    creationtime: Optional[datetime] = None
    id : Optional[str] = None
    modificationtime: Optional[datetime] = None


class PageIn(BaseModel):
    """
    contains the minimal fields (doctype and name) to create a new page
    """
    doctype: str        # 'normal-page', 'article', 'app-page' 
    locale: str
    name: str

class PageOut(BaseModel):
    """
    A readonly view used for listing pages, contains only the basic fields
    """
    active: bool
    creationtime: datetime
    doctype: str
    enabled: bool
    expirationdate: Optional[str]
    id: str
    intro: Dict[str, I18nField]
    name: str
    modificationtime: datetime
    publicationdate: Optional[str]
    slug: str

class PageDetailedOut(BaseModel):
    """
    An detailed view of a page 
    """
    active: bool
    body: Dict[str, I18nField]  
    component: PageComponent
    creationtime: datetime
    doctype: str 
    enabled: bool
    expirationdate: str
    id: str   
    intro: Dict[str, I18nField]  
    languages: List[str]
    name: str
    modificationtime: datetime
    owner: str 
    publicationdate: str
    slug: str
    title: Dict[str, I18nField]  

class PageListOut(BaseModel):
    pages: List[PageOut]

class PageUpdate(BaseModel):
    """
    a Page
    """
    body: Optional[Dict[str, I18nField]]
    component: Optional[PageComponent]
    doctype: Optional[str]
    enabled: Optional[bool]
    expirationdate: Optional[str]             # format yyyy-mm-dd
    intro: Optional[Dict[str, I18nField]]
    languages: Optional[List[str]]
    name: Optional[str]
    owner: Optional[str] 
    publicationdate: Optional[str]            # format yyyy-mm-dd
    slug: Optional[str]
    title: Optional[Dict[str, I18nField]]


class ArticleOut(BaseModel):
    """
    A readonly view used for getting the article title and intros
    """
    body: Dict[str, I18nField]  
    creationtime: datetime
    enabled: Optional[bool] = False
    expirationdate: str
    id: str   
    intro: Dict[str, I18nField]  
    languages: List[str]
    name: str
    modificationtime: datetime
    publicationdate: str
    slug: str
    title: Dict[str, I18nField]  

class ArticleListOut(BaseModel):
    articles: List[ArticleOut]

class PageSingleOut(BaseModel):
    page: PageDetailedOut

class RoutingTableItem(BaseModel):
    component: str
    id: str
    slug: str

class RoutingTableListOut(BaseModel):
    routes: List[RoutingTableItem] 