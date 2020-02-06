# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

from pymongo import MongoClient
from typing import Dict, Any

dbconfig:dict = dict()

class MongoModel:
    _collection = ""

    @classmethod
    def coll(cls):
        return dbconfig['db'][cls._collection]

from .md_counters import CounterModel
from .md_page import PageModel, BasicPage, LocalizedPage
from .md_document import DocumentModel, BasicDocument, I18nView
from .md_account import AccountModel
from .md_subscription import SubscriptionModel, BasicSubscription, Attendee
from .md_playerlist import BelplayerModel, FideplayerModel
from .md_account import AccountModel

def setup_indexes():
    DocumentModel.coll().create_index('slug', unique=True)    

def setup_db_connection(config: Dict[str, Any]):
    """
    create a mongo connection and returns the database object
    """
    dbconfig['host'] = config.get('host') or 'localhost'
    dbconfig['port'] = config.get('port') or 27017
    dbconfig['dbname'] = config.get('database')
    dbconfig['client'] = MongoClient(
        f'mongodb://{dbconfig["host"]}:{dbconfig["port"]}')
    dbconfig['db'] = dbconfig['client'][dbconfig['dbname']]
    setup_indexes()
    return dbconfig['db']