# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import os.path

# load settings
from reddevil.common.configreader import SettingsProxy
settings = SettingsProxy('bycco.bycco_settings')

import logging, logging.config
logging.config.dictConfig(settings.LOG_CONFIG)

version = '0.0.1'
# read VERSION file if it exist in backend or in root directory
backenddir = os.path.dirname(os.path.dirname(__file__))
rootdir = os.path.dirname(backenddir)
try:
    with open(os.path.join(backenddir, 'VERSION')) as fv:
        version = fv.read()
except:
    pass
try:
    with open(os.path.join(rootdir, 'VERSION')) as fv:
        version = fv.read()
except:
    pass     

log = logging.getLogger('bycco')
log.info(f'Starting website Bycco v{version} ...')

from fastapi import FastAPI
from fastapi.routing import APIRoute

app = FastAPI(
    title="Bycco",
    description="Belgisch jeugd",
    version=version,
)

from bycco.crud import get_db
from reddevil.common import register_app
register_app(settings, app, get_db(), '/api')

# import service layer 
import bycco.service
log.info(f'Service layer loaded')

# import api endpoints
import bycco.api
log.info(f'Api layer loaded')

#    Simplify operation IDs so that generated API clients have simpler function
#    names.

for route in app.routes:
    if isinstance(route, APIRoute):
        route.operation_id = route.name 

# import static html endpoints
import bycco.static
log.info(f'static html endpoints loaded')

