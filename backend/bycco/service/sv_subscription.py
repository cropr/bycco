# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging

import json, os.path
from typing import List, Optional, Dict, Any, cast
from datetime import date
from flask import render_template, Response
from binascii import a2b_base64
from werkzeug.exceptions import NotFound, BadRequest
from bs4 import BeautifulSoup
from email.message import EmailMessage, Message
from email.utils import make_msgid
from bycco import app
from bycco.models import (
    SubscriptionModel, 
    BasicSubscription, 
    CounterModel,
    BelplayerModel,
    FideplayerModel,
)
from bycco.service.mail import backends

log = logging.getLogger('bycco')
mailcc = 'confirmation@bycco.be'

def getSubscriptions() -> List[BasicSubscription]:
    """
    get all subscriptions
    """
    log.info('get subsriptions')
    subs = SubscriptionModel.find_subscriptions()
    return subs

def addSubscription(ss: dict):
    """
    add a new subscription
    """
    log.info('add subscriptions')
    idbel = ss.get('idbel', '')
    idbel = idbel.lstrip('0')
    bp = BelplayerModel.find_by_id(idbel)
    if not bp:
        raise NotFound(description="BelplayerNotfound")
    idfide = bp.idfide
    if idfide:
        fp = FideplayerModel.find_by_id(idfide)
    try:
        cs = SubscriptionModel.find_by_idbel(idbel)
        # raise BadRequest(description="AlreadySubscribed")
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

def confirmSubscription(id: str) -> str:
    invoicenumber = CounterModel.nextValue('invoice')
    nr = 202010000 + invoicenumber
    rm1 = invoicenumber // 1000
    rm2 = invoicenumber % 1000
    rm3 = nr % 97 or 97
    paymessage = f"+++020/201{rm1:01d}/{rm2:03d}{rm3:02d}+++"
    log.info(f'paymessage {paymessage}')
    sub = SubscriptionModel.updateSubscription(id, {
        'confirmed': True,
        'invoicenumber': invoicenumber,
        'paymessage': paymessage,
        'payamount': 35 if date.today() <  date(2020,3,1) else 45    
    })
    sendconfirmationmail(sub)
    return paymessage

def getPhoto(id: str):
    sub = SubscriptionModel.find_by_id(id)
    return Response(sub.badgeimage, content_type=sub.badgemimetype)     

def updatePhoto(id: str, photo: str) -> None:
    try:
        header, data = photo.split(',')
        upd = {
            'badgemimetype': header.split(':')[1].split(';')[0],
            'badgeimage': a2b_base64(data)
        }
        upd['badgelength'] = len(upd['badgeimage'])
    except:
        raise BadRequest(description='BadPhotoData')
    SubscriptionModel.updateSubscription(id, upd)

def sendconfirmationmail(s: SubscriptionModel):
    """
    send confirmation email
    :param s: the Subscription object
    :return: None
    """
    sub = {
        'fullname': f"{s.first_name} {s.last_name}",
        'birthdate': s.birthdate,
        'idclub': s.idclub,
        'nationalityfide': s.nationalityfide,
        'natstatus': 'maybe',
        'ratingbel': s.ratingbel,
        'ratingfide': s.ratingfide,
        'gender': s.gender,
        'category': s.category,
        'paymessage': s.paymessage,
        'photo_cid': make_msgid(),
    }
    if s.nationalityfide == 'BEL':
        sub['natstatus'] = 'fidebelg'
    elif s.nationalityfide and len(s.nationalityfide) > 1:
        sub['natstatus'] = 'nobelg'
    tolist = []
    if s.emailplayer:
        tolist.append(s.emailplayer)
    if s.emailparent:
        tolist.append(s.emailparent)
    basepath = os.path.dirname(os.path.dirname(__file__))
    fname = os.path.join(basepath, 'static', 'lang', f'bycco_{s.locale}.json')
    log.info(f'loading locale {s.locale} fname {fname}')
    with open(fname, 'r') as f:
        locale_msg = json.load(f)
    msgcss = render_template('mailsubscription.css')        
    msghtml = render_template('mailsubscription.html', _=locale_msg).format(
        **sub)
    msgtext = BeautifulSoup(msghtml, features="html.parser").get_text()
    msg = EmailMessage()
    msg["Subject"] = locale_msg['Confirmation Subscription']
    msg["To"] = tolist
    msg["From"] = app.config['EMAIL_SENDER']
    msg['Cc'] = mailcc
    msg["Bcc"] = app.config.get('EMAIL_BCC')
    msg.set_content(msgtext)
    msg.add_alternative(msgcss+msghtml, subtype='html')
    maintype, subtype = s.badgemimetype.split('/')
    parts = cast(List[EmailMessage], msg.get_payload())
    parts[1].add_related(s.badgeimage, maintype, subtype, 
        cid=sub['photo_cid'])
    mailbackend = backends[app.config["EMAIL_BACKEND"]]()
    mailbackend.send_message(msg)

