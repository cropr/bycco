# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

from __future__ import annotations

import logging

from dataclasses import dataclass, field, asdict
from typing import Dict, Any, TYPE_CHECKING
from datetime import datetime, timedelta
from pymongo import ReturnDocument
from bson import ObjectId
from . import MongoModel, dbconfig

log = logging.getLogger('bycco')

if TYPE_CHECKING:
    from .md_article import ArticleModel, ArticleLocalizedModel


@dataclass
class ArticleLocalizedModel:
    """
    A Localized readonly view on a ArticleModel
    """
    creationtime: datetime
    i18n_content: str
    i18n_intro: str
    i18n_title: str
    id: str 
    languages: List[str]
    metatitle: str
    modificationtime: datetime
    owner: str
    slug: str


@dataclass
class ArticleModel(MongoModel):
    """
    An Article in the database
    """
    metatitle: str
    owner: str 
    slug: str

    content: Dict[str,str] = None
    creationtime: datetime = None    
    enddate: datetime = None
    intro: Dict[str,str] = None
    languages: List[str] = None
    modificationtime: datetime = None
    startdate: datetime = None
    title: Dict[str,str] = None

    id: str = field(init=False, default=None)    
    _id: ObjectId = field(default_factory=ObjectId)

    _collection = 'article'

    # attribute id is created automatically as stringified version of _id
    def __post_init__(self):
        self.id = str(self._id)
        if not self.languages:
            self.languages = ['nl', 'fr']
        if not self.title:
            self.title = { self.languages[0]: self.metatitle}
        if not self.content: 
            self.content = { self.languages[0]: "#NA"}
        if not self.intro: 
            self.intro = { self.languages[0]: "#NA"}

    @classmethod
    def find_by_slug(cls, slug: str, lang: str) -> ArticleModel:
        """
        find an article by slug
        returns None if nothing is found
        """
        coll = dbconfig['db'][cls._collection]
        pagedoc = coll.find_one({
            'slug': slug,
        })
        if not artdoc:
            return None
        try:
            art = ArticleModel(**artdoc)
            return art
        except:
            log.exception('error encoding artdoc')
            return None

    @classmethod
    def find_by_slug_locale(cls, slug:str, lang: str) -> ArticleLocalizedModel:        
        """
        find an article by slug and locale.  Filters out the correct language
        of title and content
        returns None if nothing is found
        """
        coll = dbconfig['db'][cls._collection]
        artdoc = coll.find_one({'slug': slug})
        if not artdoc:
            return None
        try:
            artdoc['i18n_title'] = artdoc.pop('title', {}).get(lang, '')
            artdoc['i18n_content'] = artdoc.pop('content', {}).get(lang, '')
            artdoc['i18n_intro'] = artdoc.pop('intro', {}).get(lang, '')
            artdoc['id'] = str(artdoc.pop('_id'))
            art = ArticleLocalizedModel(**artdoc)
            return art
        except:
            log.exception('error encoding artdoc')
            return None

    @classmethod
    def create_article(cls, artdict: Dict[str, Any]) -> ArticleModel:
        """
        create a new articel
        """
        coll = dbconfig['db'][cls._collection]
        artdict['_id'] = artdict.get('_id', ObjectId())
        artdict['creationtime'] = datetime.utcnow()
        artdict['modificationtime'] = datetime.utcnow()
        try:
            coll.insert_one(artdict)
            art = cls(**artdict)
            return art
        except:
            log.exception('error encoding artdict')
            return None

