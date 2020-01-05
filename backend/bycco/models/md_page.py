# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

from __future__ import annotations

import logging

from datetime import datetime, date
from werkzeug.exceptions import BadRequest, NotFound, InternalServerError
from dataclasses import dataclass, field, asdict
from dacite import from_dict
from typing import Dict, Any, List, Optional, Type
from pymongo import ReturnDocument
from bson import ObjectId
from . import MongoModel, dbconfig

log = logging.getLogger('bycco')

@dataclass
class BasicPage:
    """
    A readonly view used in overview of all pages
    """
    active: bool
    creationtime: datetime
    id: str
    modificationtime: datetime
    name: str
    slug: str

@dataclass
class I18nPageFields:
    """
    subdocument, contain the localized fields of a page
    """
    content: str = ""
    intro: str = ""
    title: str = ""

@dataclass
class LocalizedPage:
    """
    A localized readonly view of a PageModel
    """
    active: bool
    creationtime: datetime
    i18n_fields: I18nPageFields
    id: str
    locale: str
    name: str              
    modificationtime: datetime
    owner: str
    slug: str
    template: str

def fixcreationtime(pagedoc: dict):
    if isinstance(pagedoc.get('creationtime'), str):
        try:
            pagedoc['creationtime'] = datetime.fromisoformat(
                pagedoc['creationtime'])
        except Exception:
            pagedoc['creationtime'] = pagedoc['modificationtime']  

@dataclass
class PageModel(MongoModel):
    """
    A Page in the database
    """
    name: str
    owner: str 
    slug: str

    active: bool = False
    creationtime: Optional[datetime] = None
    i18n_fieldset: Dict[str, I18nPageFields] = field(default_factory=dict)
    languages: List[str] = field(default_factory=list)
    modificationtime: Optional[datetime] = None
    pagetype: str = "page"
    subpages: List[str] = field(default_factory=list)
    template: Optional[str] = None

    id: str = field(init=False, default="")    
    _id: ObjectId = field(default_factory=ObjectId)

    _collection = 'page'
    _hidden = ['_id']

    # attribute id is created automatically as stringified version of _id
    def __post_init__(self):
        self.id = str(self._id)
        if not self.creationtime:
            self.creationtime = datetime.utcnow()
        if not self.modificationtime:
            self.modificationtime = datetime.utcnow()
        if not self.languages:
            self.languages = list(self.localpages.keys()) or ['en']


    @classmethod
    def create_page(cls, pagedict: Dict[str, Any] ) -> PageModel:
        """
        create a new page
        """
        pagedict['_id'] = pagedict.get('_id', ObjectId())
        pagedict['creationtime'] = pagedict.get('creationtime', 
            datetime.utcnow())
        pagedict['modificationtime'] = pagedict.get('modificationtime', 
            datetime.utcnow())
        try:
            cls.coll().insert_one(pagedict)
            page = from_dict(data_class=cls, data=pagedict)
            return page
        except:
            log.exception('error encoding pagedict')
            raise BadRequest(description="CannotEncodeCreatedPage")

    @classmethod
    def find_pages(cls) -> List[BasicPage]:
        """
        find all pages 
        """
        pages = []
        cursor = cls.coll().find({}, {
            "active": 1,
            "creationtime": 1,
            "modificationtime": 1,
            "name": 1,
            "slug": 1,
        })
        for doc in cursor:
            doc['id'] = str(doc.pop('_id'))
            fixcreationtime(doc)
            try:
                page = from_dict(data_class=BasicPage, data=doc)
                pages.append(page)
            except:
                log.exception('error encoding BasicPage')
                raise InternalServerError(description="CannotEncodePage")
        return pages

    @classmethod
    def find_by_id(cls, id: str, ) -> PageModel:
        """
        find a page by slug
        returns None if nothing is found
        """
        try:
            oid = ObjectId(id)
        except:
            raise BadRequest(description="InvalidPageId")
        pagedoc = cls.coll().find_one(oid)
        if not pagedoc:
            raise NotFound(description="PageNotFound")
        fixcreationtime(pagedoc)            
        try:
            page = from_dict(data_class=cls, data=pagedoc)
            return page
        except:
            log.exception('error encoding pagedoc')
            raise InternalServerError(description="ErrorEncodingPage")

    @classmethod
    def find_by_slug(cls, slug: str) -> PageModel:
        """
        find a page by slug
        returns None if nothing is found
        """
        pagedoc = cls.coll().find_one({'slug': slug})
        if not pagedoc:
            raise NotFound(description="PageNotFound")
        fixcreationtime(pagedoc)
        try:
            page = from_dict(data_class=cls, data=pagedoc)
            return page
        except:
            log.exception('error encoding pagedoc')
            raise InternalServerError(description="ErrorEncodingPage")

    @classmethod
    def find_i18n_by_slug(cls, slug: str, lang: str) -> LocalizedPage:        
        """
        find a page by slug and locale.  Filters out the correct language
        returns None if nothing is found
        """
        pagedoc = cls.coll().find_one({'slug': slug}, 
            {'pagetype': 0, 'subpages': 0, 'languages': 0})
        if not pagedoc:
            raise NotFound(description="PageNotFound")
        fixcreationtime(pagedoc)
        try:
            pagedoc['id'] = str(pagedoc.pop('_id'))
            pagedoc['locale'] = lang
            pagedoc['i18n_fields'] = pagedoc.pop('i18n_fieldset', {}).get(lang, 
                I18nPageFields())
            page = from_dict(data_class=LocalizedPage, data=pagedoc)
            return page
        except:
            log.exception('error encoding pagedict')
            raise InternalServerError(description="ErrorEncodingPage")

    def get_slug_templates(self):
        """
        returns a dict of slug:template for all pages 
        """
        return {a['slug']:a['template']  for a in self.coll().find(
            projection={'slug':1, 'template':1, '_id':0})}

    @classmethod
    def update_page(cls, id: str, pagedict: Dict[str, Any] ) -> PageModel:
        """
        update a page
        """
        try:
            oid = ObjectId(id)
        except:
            raise BadRequest(description="InvalidPageId")
        pagedict['modificationtime'] = datetime.utcnow()
        fixcreationtime(pagedict)
        pagedoc = cls.coll().find_one_and_update({'_id': oid}, 
            {'$set': pagedict}, return_document=ReturnDocument.AFTER)
        if not pagedoc:
            raise NotFound(description="PageNotFound")
        try:
            page = from_dict(data_class=cls, data=pagedoc)
            return page
        except:
            log.exception('error encoding pagedict')
            raise InternalServerError(description="ErrorEncodingPage")
