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
from reddevil.boardrole.mongo_brole import DbBoardRole
from reddevil.boardrole.md_brole import (
    BoardRoleIn, 
)

db = None

def setup_module(module):
    global db
    register_app(settings, app)
    db = dbtestsetup()
    coll = db[DbBoardRole.COLLECTION]
    for item in readyaml('brole.yaml'):
        item['_id'] = ObjectId()
        coll.insert_one(item)    

def teardown_module(module):
    pass

def test_create_brole():
    from reddevil.boardrole.sv_brole import createBRole
    d = BoardRoleIn(name='zakkenvuller')
    rc = createBRole(d)
    assert isinstance(rc, str)
    oid = ObjectId(rc)
    dd = db.rd_boardroles.find_one(oid)
    assert dd is not None
    assert dd['name'] == 'zakkenvuller'

def test_delete_brole():
    from reddevil.boardrole.sv_brole import deleteBRole
    dd = db.rd_boardroles.find_one({'name':'president'})
    deleteBRole(str(dd['_id']))
    dd = db.rd_boardroles.find_one({'name':'president'})
    assert dd is None

def test_get_brole():
    from reddevil.boardrole.sv_brole import getBRole
    dd = db.rd_boardroles.find_one({'name':'webmaster'})
    dd2 = getBRole(str(dd['_id']))
    assert dd2 is not None
    assert dd2.name == 'webmaster'

def test_get_broles():
    from reddevil.boardrole.sv_brole import getBRoles
    dd = getBRoles()
    assert dd is not None
    assert isinstance(dd.roles, list)
    print(f'r1: {dd.roles[0]}')


