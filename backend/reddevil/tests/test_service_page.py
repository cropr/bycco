# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging
log = logging.getLogger('reddevil')

import os, os.path, json
from unittest.mock import Mock, patch
from bson import ObjectId
from datetime import datetime, timezone, timedelta
from time import time

from . import app, settings, dbtestsetup, readyaml

from reddevil.common import register_app
register_app(settings, app)

from reddevil.page.mongo_page import DbPage
from reddevil.page.md_page import (
    PageIn, PageDetailedIn
)
from reddevil.page.sv_page import (
    createPage,
    deletePage,
    getPage,
    getPageBySlug,
    getPages,
    updatePage
)

from reddevil.account.md_account import UserRights

db = None

def mock_token(token):
    return UserRights(username='ik', access_rights=[], id='123', groups=[])

def setup_module(module):
    global db

    db = dbtestsetup()
    coll = db[DbPage.COLLECTION]
    for item in readyaml('page.yaml'):
        n = datetime.now(tz=timezone.utc)
        item['_id'] = ObjectId()
        item['created_ts'] = n
        item['modified_ts'] = n
        ed = item.pop('expirydelta', None) 
        if ed is not None:
            item['expired_ts'] = n + timedelta(days=ed)
        pd = item.pop('publisheddelta', None) 
        if pd is not None:
            item['published_ts'] = n + timedelta(days=pd)
        coll.insert_one(item)

def teardown_module(module):
    pass

@patch('reddevil.page.sv_page.check_token', new=mock_token)
def test_create_page():
    d = PageIn(doctype='page', name='page1')
    rc = createPage(d, "Jimi")
    assert isinstance(rc, str)
    oid = ObjectId(rc)
    dd = db.rd_page.find_one(oid)
    assert dd is not None
    assert dd['name'] == 'page1'

@patch('reddevil.page.sv_page.check_token', new=mock_token)
def test_delete_page():
    dd = db.rd_page.find_one({'slug':'Een-eerste-titel'})
    deletePage(str(dd['_id']), "Jimi")
    dd = db.rd_page.find_one({'slug':'Een-eerste-titel'})
    assert dd is None

@patch('reddevil.page.sv_page.check_token', new=mock_token)
def test_get_page():
    dd = db.rd_page.find_one({'slug':'titel2'})
    dd2 = getPage(str(dd['_id']), "Jimi")
    assert dd2 is not None
    assert dd2.slug == 'titel2'

def test_get_pagebyslug():
    dd2 = getPageBySlug('titel2')
    assert dd2 is not None
    assert dd2.name == 'doc2'

@patch('reddevil.page.sv_page.check_token', new=mock_token)
def test_get_updatepage():
    dd = db.rd_page.find_one({'slug':'titel3'})
    id = str(dd['_id'])
    ddi = PageDetailedIn(name='changedname', languages=['nl', 'fr'])
    dd2 = updatePage(id, ddi, "Jimi")
    assert dd2.name == 'changedname'
