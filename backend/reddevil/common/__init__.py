# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging
log = logging.getLogger('reddevil')

from fastapi import FastAPI
from typing import Optional, Any, Callable
from motor.motor_asyncio import AsyncIOMotorClient

# variables common for all reddevil modules

cfg: Any = None                                     # the configuration object
app: Optional[FastAPI] = None                       # the FastAPI app instance
get_db: Callable = None                             # the database connection
url: str = ''                                       # the base url for all endpoints

def register_app(my_cfg: Any, my_app: FastAPI, my_get_db: Callable, 
        my_url: str):
    global cfg, app, get_db, url
    cfg = my_cfg
    app = my_app
    get_db = my_get_db
    url = my_url

from .errors import (
    RdBadRequest,
    RdException,
    RdInternalServerError,
    RdNotFound,
    RdNotAuthorized,
)
from .util import iso2date, date2datetime
from .security import (
    check_token, 
    oauth2_scheme, 
    oauth2_optional, 
    bearer_schema
)

