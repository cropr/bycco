# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

from dataclasses import dataclass
from pymongo import MongoClient

@dataclass
class MongoModel:
    _collection = ""

dbconfig = {}

from .md_page import PageModel
from .md_account import AccountModel

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