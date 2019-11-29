# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

from pymongo import MongoClient

dbconfig:dict = dict()

class MongoModel:
    _collection = ""

    @classmethod
    def coll(cls):
        return dbconfig['db'][cls._collection]

from .md_counters import CounterModel
from .md_page import PageModel, BasicPage, LocalizedPage
from .md_account import AccountModel
from .md_subscription import SubscriptionModel, BasicSubscription

def setup_db_connection(config):
    """
    create a mongo connection 
    @param(config): the mongo db config
    """
    dbconfig['host'] = config.get('host') or 'localhost'
    dbconfig['port'] = config.get('port') or 27017
    dbconfig['dbname'] = config.get('database')
    dbconfig['client'] = MongoClient(
        f'mongodb://{dbconfig["host"]}:{dbconfig["port"]}')
    dbconfig['db'] = dbconfig['client'][dbconfig['dbname']] 
    return dbconfig['db']