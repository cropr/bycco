# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

# all database request come in here, but we do not use dataclasess
# if needed we define extra models an do marshalling functions at the service level
# All _id are translatesd to stringified id on output
# All functions expect stringified id as input 

import logging

from datetime import datetime, date, timezone
from typing import Dict, List, Any 
from pymongo import ReturnDocument
from bson import ObjectId
from reddevil.common import RdBadRequest, RdNotFound, date2datetime
from reddevil.crud.db_base import DbBase

log = logging.getLogger('reddevil')

class DbAccount(DbBase):
    COLLECTION = 'rd_account'
    DOCUMENTTYPE = 'Account'
    SIMPLEFIELDS = [ 'email', 'enabled', 'first_name', 'last_name', 'locale', 
        'logintype']
    VERSION = 1
