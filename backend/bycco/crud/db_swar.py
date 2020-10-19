# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

# all database request come in here, but we do not use dataclasess
# if needed we define extra models an do marshalling functions at the service level
# All _id are translatesd to stringified id on output
# All functions expect stringified id as input 

import pymongo
from datetime import datetime, date, timezone
from typing import Dict, List, Any 
from bson import ObjectId
from reddevil.crud.db_base import DbBase
from reddevil.common import get_db
from bycco import settings

class DbSwar(DbBase):
    COLLECTION = 'swar'
    DOCUMENTTYPE = 'Swar'
    SIMPLEFIELDS = [ 
        'name', 'rounds', 'shortname', 'swarname'
    ]
    VERSION = 1

