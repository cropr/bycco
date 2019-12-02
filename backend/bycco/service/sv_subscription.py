# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging

from typing import List, Optional, Dict, Any
import json
from datetime import date
from flask import render_template, abort, Response
from werkzeug.exceptions import NotFound
from bycco import app
from bycco.models import (
    SubscriptionModel, 
    BasicSubscription, 
    CounterModel,
    BelplayerModel,
    FideplayerModel,
)
from .mail import sendconfirmationmail

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
    bp = BelplayerModel.find_by_id(idbel)
    idfide = bp.idfide
    if idfide:
        fp = FideplayerModel.find_by_id(idfide)
    try:
        cs = SubscriptionModel.find_by_idbel(idbel)
    except NotFound:
        cs = SubscriptionModel.blank()
    cs.birthdate = bp.birthdate
    cs.category = ss.get('category') or '#NA'
    cs.chesstitle = fp.chesstitle if idfide else ''
    cs.emailparent = ss.get('emailparent') or ''
    cs.emailplayer = ss.get('emailplayer') or ''
    cs.federation = bp.federation
    cs.nationalityfide = fp.nationalityfide if idfide else ''
    cs.first_name = bp.first_name
    cs.fullnameattendant = ss.get('fullnameattendant') or ''
    cs.fullnameparent = ss.get('fullnameparent') or ''
    cs.gender = bp.gender
    cs.idclub = bp.idclub
    cs.idfide = idfide
    cs.idbel = idbel
    cs.last_name = bp.last_name
    cs.locale = ss.get('locale') or 'nl'
    cs.mobileattendant = ss.get('mobileattendant') or ''
    cs.mobileparent = ss.get('mobileparent') or ''
    cs.mobileplayer = ss.get('mobileplayer') or ''
    cs.ratingbel = bp.currentrating()
    cs.ratingfide = fp.currentrating() if idfide else 0
    cs.rating = max(cs.ratingbel, cs.ratingfide)
    cs.nationalitybel = bp.nationalitybel
    cs.payamount = 0
    cs.save()
    return {'id': cs.id}

def confirmSubscription(id: str) -> None:
    invoicenumber = CounterModel.nextValue('invoice')
    nr = 2020010000 + invoicenumber
    rm1 = invoicenumber // 1000
    rm2 = invoicenumber % 1000
    rm3 = nr % 97 or 97
    paymessage = f"+++202/001{rm1:01d}/{rm2:03d}{rm3:02d}+++"
    sub = SubscriptionModel.updateSubscription(id, {
        'confirmed': True,
        'invoicenumber': invoicenumber,
        'paymessage': paymessage,
        'payamount': 35 if date.today() <  date(2020,3,1) else 45    
    })
    sendconfirmationmail(sub)

def getPhoto(id: str):
    sub = SubscriptionModel.find_by_id(id)
    return Response(sub.badgeimage, content_type=sub.badgemimetype)     

def sendconfirmationmail(sub):
    pass    