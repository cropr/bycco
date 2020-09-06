# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging
log = logging.getLogger('reddevil')

import os, os.path, json
from bson import ObjectId
from datetime import datetime, timezone, timedelta
from time import time

from . import app, settings, dbtestsetup, readyaml
from reddevil.common import register_app
from reddevil.accountright.mongo_aright import DbAccountRight
from reddevil.accountright.md_aright import (
    AccountRightIn, 
)

db = None

def setup_module(module):
    global db
    register_app(settings, app)
    db = dbtestsetup()
    coll = db[DbAccountRight.COLLECTION]
    for item in readyaml('aright.yaml'):
        item['_id'] = ObjectId()
        coll.insert_one(item)    

def teardown_module(module):
    pass

def test_create_aright():
    from reddevil.accountright.sv_aright import createARight
    d = AccountRightIn(name='zakkenvuller')
    rc = createARight(d)
    assert isinstance(rc, str)
    oid = ObjectId(rc)
    dd = db.rd_accountrights.find_one(oid)
    assert dd is not None
    assert dd['name'] == 'zakkenvuller'

def test_delete_aright():
    from reddevil.accountright.sv_aright import deleteARight
    dd = db.rd_accountrights.find_one({'name':'editor'})
    deleteARight(str(dd['_id']))
    dd = db.rd_accountrights.find_one({'name':'editor'})
    assert dd is None

def test_get_aright():
    from reddevil.accountright.sv_aright import getARight
    dd = db.rd_accountrights.find_one({'name':'reader'})
    dd2 = getARight(str(dd['_id']))
    assert dd2 is not None
    assert dd2.name == 'reader'

def test_get_arights():
    from reddevil.accountright.sv_aright import getARights
    dd = getARights()
    assert dd is not None
    assert isinstance(dd.rights, list)
    print(f'r1: {dd.rights[0]}')


