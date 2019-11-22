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
class PageLocalizedModel:
    """
    A Localized readonly view on a PageModel
    """
    creationtime: datetime
    i18n_title: str
    i18n_content: str
    id: str 
    languages: List[str]
    metatitle: str
    modificationtime: datetime
    owner: str
    slug: str

@dataclass
class PageBasicModel:
    """
    view used in overview of all pages
    """
    metatitle: str
    owner: str 
    slug: str
    template: str
    id: str

    creationtime: Optional[datetime] = None
    languages: List[str] = field(default_factory=list)
    modificationtime: Optional[datetime] = None
    title: Dict[str,str] = field(default_factory=dict)


@dataclass
class PageModel(MongoModel):
    """
    A Page in the database
    """
    metatitle: str
    owner: str 
    slug: str
    template: str

    content: Dict[str,str] = field(default_factory=dict)
    creationtime: Optional[datetime] = None
    languages: List[str] = field(default_factory=list)
    modificationtime: Optional[datetime] = None
    title: Dict[str,str] = field(default_factory=dict)
    subpages: Optional[List["PageModel"]] = None

    id: str = field(init=False, default="")    
    _id: ObjectId = field(default_factory=ObjectId)

    _collection = 'page'

    # attribute id is created automatically as stringified version of _id
    def __post_init__(self):
        self.id = str(self._id)
        if not self.languages:
            self.languages = ['nl', 'fr']
        if not self.title:
            self.title = { self.languages[0]: self.metatitle}
        if not self.content: 
            self.content = { self.languages[0]: "#NA"}

    @classmethod
    def find_all( cls: Type["PageModel"] ) -> List[PageBasicModel]:
        """
        find all pages 
        """
        coll = dbconfig['db'][cls._collection]
        pages = []
        cursor = coll.find({},{
            "metatitle": 1,
            "owner": 1,
            "slug": 1,
            "template": 1,
            "creationtime": 1,
            "languages": 1,
            "modificationtime": 1,
            "title": 1,
        })
        for doc in cursor:
            doc['id'] = str(doc.pop('_id'))
            try:
                page = PageBasicModel(**doc)
                pages.append(page)
            except:
                log.exception('error encoding pagedoc')
                return None
        return pages

    @classmethod
    def find_by_slug(
            cls: Type["PageModel"], 
            slug: str, 
            lang: str
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
    def find_by_slug_locale(cls, slug:str, lang: str
            ) -> Optional[PageLocalizedModel]:        
        """
        find a page by slug and locale.  Filters out the correct language
        of title and content
        returns None if nothing is found
        """
        coll = dbconfig['db'][cls._collection]
        pagedoc = coll.find_one({'slug': slug}, {'template': 0})
        if not pagedoc:
            return None
        try:
            pagedoc['i18n_title'] = pagedoc.pop('title', {}).get(lang, '')
            pagedoc['i18n_content'] = pagedoc.pop('content', {}).get(lang, '')
            pagedoc['id'] = str(pagedoc.pop('_id'))
            page = PageLocalizedModel(**pagedoc)
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
        pagedict['modificationtime'] = datetime.utcnow()
        try:
            coll.update_one({'_id': self._id}, pagedict)
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