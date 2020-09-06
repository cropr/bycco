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
from reddevil.boardmember.mongo_bmember import DbBoardMember
from reddevil.boardmember.md_bmember import (
    BoardMemberIn, 
)

db = None

def setup_module(module):
    global db
    register_app(settings, app)
    db = dbtestsetup()
    coll = db[DbBoardMember.COLLECTION]
    for item in readyaml('bmember.yaml'):
        item['_id'] = ObjectId()
        coll.insert_one(item)    

def teardown_module(module):
    pass

def test_create_bmember():
    from reddevil.boardmember.sv_bmember import createBMember
    d = BoardMemberIn(first_name='Jimi', last_name='Hendrix')
    rc = createBMember(d)
    assert isinstance(rc, str)
    oid = ObjectId(rc)
    dd = db.rd_boardmembers.find_one(oid)
    assert dd is not None
    assert dd['first_name'] == 'Jimi'

def test_delete_bmember():
    from reddevil.boardmember.sv_bmember import deleteBMember
    dd = db.rd_boardmembers.find_one({'first_name':'Ruben'})
    print('dd', dd)
    deleteBMember(str(dd['_id']))
    dd = db.rd_boardmembers.find_one({'first_name':'Ruben'})
    assert dd is None

def test_get_bmember():
    from reddevil.boardmember.sv_bmember import getBMember
    dd = db.rd_boardmembers.find_one({'first_name':'Martin'})
    dd2 = getBMember(str(dd['_id']))
    assert dd2 is not None
    assert dd2.first_name == 'Martin'

def test_get_bmembers():
    from reddevil.boardmember.sv_bmember import getBMembers
    dd = getBMembers({})
    assert dd is not None
    assert isinstance(dd.members, list)


