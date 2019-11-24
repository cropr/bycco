# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

from __future__ import annotations

import logging

from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional, Type
from datetime import datetime, timedelta
from pymongo import ReturnDocument
from bson import ObjectId
from . import MongoModel, dbconfig

log = logging.getLogger('bycco')

@dataclass
class I18nPageFields:
    """
    subdocument, contain the localized fields of a page
    """
    content: str = ""
    intro: str = ""
    title: str = ""

@dataclass
class BasicPage:
    """
    A readonly view used in overview of all pages
    """
    name: str
    slug: str
    id: str
    creationtime: Optional[datetime] = None
    modificationtime: Optional[datetime] = None

@dataclass
class LocalizedPage:
    """
    A localized readonly view of a PageModel
    """
    creationtime: datetime
    i18n_fields: I18nPageFields
    id: str
    locale: str
    name: str              
    modificationtime: datetime
    owner: str
    slug: str

@dataclass
class PageModel(MongoModel):
    """
    A Page in the database
    """
    name: str
    owner: str 
    slug: str

    creationtime: Optional[datetime] = None
    languages: List[str] = field(default_factory=list)
    i18n_fieldset: Dict[str, I18nPageFields] = field(default_factory=dict)
    modificationtime: Optional[datetime] = None
    subpages: List[str] = field(default_factory=list)
    template: Optional[str] = None

    id: str = field(init=False, default="")    
    _id: ObjectId = field(default_factory=ObjectId)

    _collection = 'page'

    # attribute id is created automatically as stringified version of _id
    def __post_init__(self):
        self.id = str(self._id)
        if not self.languages:
            self.languages = list(self.localpages.keys()) or ['en']

    @classmethod
    def find_pages( cls: Type["PageModel"] ) -> List[BasicPage]:
        """
        find all pages 
        """
        coll = dbconfig['db'][cls._collection]
        pages = []
        cursor = coll.find({}, {
            "name": 1,
            "slug": 1,
            "creationtime": 1,
            "modificationtime": 1,
        })
        for doc in cursor:
            doc['id'] = str(doc.pop('_id'))
            try:
                page = BasicPage(**doc)
                pages.append(page)
            except:
                log.exception('error encoding BasicPage')
                continue
        return pages

    @classmethod
    def find_by_slug(
            cls: Type["PageModel"], 
            slug: str, 
        ) -> Optional["PageModel"]:
        """
        find a page by slug
        returns None if nothing is found
        """
        coll = dbconfig['db'][cls._collection]
        pagedoc = coll.find_one({
            'slug': slug,
        })
        if not pagedoc:
            return None
        try:
            page = cls(**pagedoc)
            return page
        except:
            log.exception('error encoding pagedoc')
            return None

    @classmethod
    def find_by_slug_locale(
            cls: Type["PageModel"], 
            slug: str, 
            lang: str,
        ) -> Optional[LocalizedPage]:        
        """
        find a page by slug and locale.  Filters out the correct language
        returns None if nothing is found
        """
        coll = dbconfig['db'][cls._collection]
        pagedoc = coll.find_one({'slug': slug}, {'template': 0})
        if not pagedoc:
            return None
        try:
            pagedoc['id'] = str(pagedoc.pop('_id'))
            pagedoc['locale'] = lang
            pagedoc['i18n_fields'] = pagedoc.pop('i18n_fieldset', {}).get(lang, 
                I18nPageFields()) 
            page = LocalizedPage(**pagedoc)
            return page
        except:
            log.exception('error encoding pagedicr')
            return None

    @classmethod
    def create_page(
            cls: Type["PageModel"], 
            pagedict: Dict[str, Any]
        ) -> Optional["PageModel"]:
        """
        create a new page
        """
        coll = dbconfig['db'][cls._collection]
        pagedict['_id'] = pagedict.get('_id', ObjectId())
        pagedict['creationtime'] = datetime.utcnow()
        pagedict['modificationtime'] = datetime.utcnow()
        try:
            coll.insert_one(pagedict)
            page = cls(**pagedict)
            return page
        except:
            log.exception('error encoding pagedict')
            return None

    def update_page(
            self: "PageModel", 
            pagedict: Dict[str, Any]
        ) -> None:
        """
        update a page
        """
        coll = dbconfig['db'][self._collection]
        pagedict.pop('id', None)
        pagedict['modificationtime'] = datetime.utcnow()
        try:
            coll.find_one_and_update({'_id': self._id}, pagedict, 
                return_document=ReturnDocument.AFTER)
        except:
            log.exception('error encoding pagedict')
            return None

    def getSlugTemplates(self):
        """
        returns a dict of slug:template for all pages 
        """
        coll = dbconfig['db'][self._collection]
        return {a['slug']:a['template']  for a in coll.find(projection={
            'slug':1, 'template':1, '_id':0})}