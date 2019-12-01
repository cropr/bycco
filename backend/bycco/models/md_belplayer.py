# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

from __future__ import annotations

import logging

from datetime import datetime
from werkzeug.exceptions import BadRequest, NotFound, InternalServerError
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional, Type
from pymongo import ReturnDocument
from bson import ObjectId
from . import MongoModel, dbconfig

log = logging.getLogger('bycco')


@dataclass
class BelplayerModel(MongoModel):
    """
    A player in the Belgian playerlist
    """
    _id: str            # Belgian id number
    birthdate: datetime
    federation: str
    first_name: str
    gender: str 
    idclub: str
    last_name: str
    nationalitybel: str

    idfide: str = ''
    ratingsbel: list = field(default_factory=list)
    _class: str = "Belplayer"

    _collection = 'belranking'


    @classmethod
    def find_by_id(
            cls: Type["BelplayerModel"], 
            id: str, 
        ) -> "BelplayerModel":
        """
        find a player by his Beligan id
        returns None if nothing is found
        """
        beldoc = cls.coll().find_one({'_id':id})
        if not beldoc:
            raise NotFound(description="BelplayerNotFound")
        try:
            return cls(**beldoc)
        except:
            log.exception('error encoding belplayer')
            raise InternalServerError(description="ErrorEncodingBelplayer")

    @classmethod
    def blank(
            cls: Type["BelplayerModel"], 
            id: str, 
        ) -> "BelplayerModel":
        """
        cretae a blank Belplyaer with a given id
        """
        beldict = {
            '_id': id,
            'birthdate': datetime(1900,1,1),
            'federation': '#NA',
            'first_name': '#NA',
            'gender': '#NA',
            'last_name': '#NA',
            'idclub': '#NA',
            'nationalitybel': 'BEL'
        }
        try:
            cls.coll().insert_one(beldict)
        except:
            raise BadRequest(description="CannotCreateBelplayer(duplicate?)")
        return cls.find_by_id(id)

    def save(self: "BelplayerModel") -> None:
        """
        save changes of Belplayer instance
        """
        beldict = asdict(self)
        self.coll().find_one_and_replace({'_id': self._id}, beldict)

@dataclass
class FideplayerModel(MongoModel):
    """
    A player in the Fide playerlist
    """
    _id: str            # Belgian id number
    birthyear: str
    first_name: str
    gender: str 
    last_name: str
    nationalityfide: str

    chesstitle: str = ''
    ratingsfide: list = field(default_factory=list)
    _class: str = "Fideplayer"

    _collection = 'fideranking'

    @classmethod
    def find_by_id(
            cls: Type["FideplayerModel"], 
            id: str, 
        ) -> "FideplayerModel":
        """
        find a player by his Beligan id
        returns None if nothing is found
        """
        fidedoc = cls.coll().find_one({'_id':id})
        if not fidedoc:
            raise NotFound(description="FideplayerNotFound")
        try:
            return cls(**fidedoc)
        except:
            log.exception('error encoding fideplayer')
            raise InternalServerError(description="ErrorEncodingFideplayer")

    @classmethod
    def blank(
            cls: Type["FideplayerModel"], 
            id: str, 
        ) -> "FideplayerModel":
        """
        cretae a blank Fideplayer with a given id
        """
        fidedict = {
            '_id': id,
            'birthyear': '1900',
            'first_name': '#NA',
            'gender': '#NA',
            'last_name': '#NA',
            'nationalityfide': '#NA'
        }
        try:
            cls.coll().insert_one(fidedict)
        except:
            raise BadRequest(description="CannotCreateFideplayer(duplicate?)")
        return cls.find_by_id(id)

    def save(self: "FideplayerModel") -> None:
        """
        save changes of Fideplayer instance
        """
        fidedict = asdict(self)
        self.coll().find_one_and_replace({'_id': self._id}, fidedict)