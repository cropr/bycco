# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import os.path
import yaml
from fastapi import FastAPI
from bson import ObjectId


class Settings:

    DATASTORE = {
        'database': 'test_reddevil',
        'host': 'localhost',
        'module': 'reddevil.common.db_mongo',
        'port': 27017,
        'prefix': 'mongo'    
    }

    LOG_CONFIG = {
        'version': 1,
        'formatters': {
            'simple': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'simple',
                'stream': 'ext://sys.stderr'
            }
        },
        'loggers': {
            'reddevil': {
                'handlers': ['console'],
                'level': 'INFO'
            }
        }
    }

settings = Settings()
app = FastAPI(
    title="Test Reddevil",
    version='0.0.1',    
)

def readyaml(name):
    with open(os.path.join(os.path.dirname(__file__), "data", name)) as f:
        return iter(yaml.load(f, Loader=yaml.FullLoader))


def dbtestsetup():
   
    from reddevil.common import conn
    db = conn[1]
    db.command('dropDatabase')
    return db


