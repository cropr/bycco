# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging

import json
import requests
from flask import render_template, abort, Response
from typing import List, Optional, Dict, Any
from bycco import app
from bycco.models import SubscriptionModel, BasicSubscription

log = logging.getLogger('bycco')

def getSubscriptions() -> List[BasicSubscription]:
    """
    get all subscriptions
    """
    log.info('get subsriptions')
    subs = SubscriptionModel.find_subscriptions()
    return subs

def addSubscription(ss: dict):
    """
    get all subscriptions
    """
    log.info('add subscriptions')
    idbel = ss.get('idbel', '')
    idbel = idbel.lstrip('0')
    ca_url = f"{app.config['CHESSAPI_URL']}ranking/bel/{idbel}"
    resp = requests.get(ca_url)
    if resp.status_code == 404:
        abort(Response("PlayerNotFound", status=404))
    if resp.status_code != 200:
        log.error(f'chessapi returned {resp.status_code}')
        abort(Response("ChessApiError", status=500))
    bp = resp.json()
    idfide = bp.get('idfide', '')
    fp: Dict[str, Any] = dict()
    if idfide:
        ca_url = f"{app.config['CHESSAPI_URL']}ranking/fide/{idfide}"
        resp = requests.get(ca_url)
        if resp.status_code == 200:
            fp = resp.json()
    cs = SubscriptionModel.find_by_idbel(idbel)
    if not cs:
        cs = SubscriptionModel.blank()
    cs.birthdate = bp.get('birthdate').split('T')[0]
    cs.category = ss.get('category') or '#NA'
    cs.chesstitle = bp.get('chesstitle') or ''
    cs.emailparent = ss.get('emailparent') or ''
    cs.emailplayer = ss.get('emailplayer') or ''
    cs.federation = bp.get('federation')
    cs.nationalityfide = fp.get('nationalityfide', '')
    cs.first_name = bp.get('first_name')
    cs.fullnameattendant = ss.get('fullnameattendant') or ''
    cs.fullnameparent = ss.get('fullnameparent') or ''
    cs.gender = bp.get('gender')
    cs.idclub = bp.get('idclub')
    cs.idfide = idfide
    cs.idbel = idbel
    cs.last_name = bp.get('last_name')
    cs.locale = ss.get('locale') or 'nl'
    cs.mobileattendant = ss.get('mobileattendant') or ''
    cs.mobileparent = ss.get('mobileparent') or ''
    cs.mobileplayer = ss.get('mobileplayer') or ''
    cs.ratingbel = bp.get('currentrating')
    cs.ratingfide = fp.get('currentrating', 0)
    cs.rating = max(cs.ratingbel, cs.ratingfide)
    cs.nationalitybel = bp.get('nationalitybel')
    cs.payamount = 0
    paymessage = cs.save()
    return {'paymessage': msg, 'id': cs.id}

def getSubscription(id: str) -> dict:
    """
    get a Subscription
    """
    return {}