# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

from __future__ import annotations

import logging

from typing import Type
from pymongo import ReturnDocument
from . import MongoModel, dbconfig

log = logging.getLogger(__name__)

class CounterModel(MongoModel):
    """
    A simple Counter collection storing autoincrement sequences 
    two fields: _id and value
    """

    _collection = 'counters'

    @classmethod
    def nextValue(cls: Type["CounterModel"], name: str) -> int:
        coll = dbconfig['db'][cls._collection]
        next = coll.find_one_and_update({'_id': name}, {'$inc': {'value': 1}}, 
            upsert=True, return_document=ReturnDocument.AFTER)
        return next['value']
