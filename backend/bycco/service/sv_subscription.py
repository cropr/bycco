# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging

import json, os.path
from typing import List, Optional, Dict, Any, cast
from datetime import date, datetime, timezone
from flask import render_template, Response
from binascii import a2b_base64
from werkzeug.exceptions import NotFound, BadRequest
from bs4 import BeautifulSoup
from email.message import EmailMessage, Message
from email.utils import make_msgid
from bycco import app
from bycco.util.dates import iso2date
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
    cs.locale = ss.get('locale') or 'en'
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
    log.info(f'confirm sub {id}')
    try:
        sub = SubscriptionModel.find_by_id(id)
        invoicenumber = sub.invoicenumber if sub.invoicenumber else \
            CounterModel.nextValue('invoice')
    except:
        log.info('Cannot find sub')
        invoicenumber = CounterModel.nextValue('invoice')
    nr = int(2020010000 + invoicenumber)
    rm1 = invoicenumber // 1000
    rm2 = invoicenumber % 1000
    rm3 = nr % 97 or 97
    paymessage = f"+++202/001{rm1:01d}/{rm2:03d}{rm3:02d}+++"
    sub = SubscriptionModel.updateSubscription(id, {
        'confirmed': True,
        'invoicenumber': invoicenumber,
        'paymessage': paymessage,
        'payamount': 35 if date.today() < date(2020,3,1) else 45    
    })
    sendconfirmationmail(sub)
    return paymessage

def csvSubscriptions() -> List[dict]:
    """
    get all subscriptions in csv format
    """
    return SubscriptionModel.csv_subscriptions()

def deleteSubscription(id: str) -> None:
    SubscriptionModel.removeSubscription(id)

def getPhoto(id: str):
    sub = SubscriptionModel.find_by_id(id)
    return Response(sub.badgeimage, content_type=sub.badgemimetype)     

def getSubscriptions() -> List[BasicSubscription]:
    """
    get all subscriptions
    """
    log.info('get subsriptions')
    subs = SubscriptionModel.find_subscriptions()
    return subs

def getSubscription(id: str) -> SubscriptionModel:
    """
    get one subscription
    """
    log.info('get subsription')
    s = SubscriptionModel.find_by_id(id)
    return s

def getSubscriptionByIdbel(idbel: str) -> SubscriptionModel:
    """
    get one subscription
    """
    log.info('get subsription by idbel')
    return SubscriptionModel.find_by_idbel(idbel)

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
        'ratingbel': s.ratingbel,
        'ratingfide': s.ratingfide,
        'gender': s.gender,
        'category': s.category,
        'paymessage': s.paymessage,
    }
    tolist = []
    if s.emailplayer:
        tolist.append(s.emailplayer)
    if s.emailparent:
        tolist.append(s.emailparent)
    basepath = os.path.dirname(os.path.dirname(__file__))
    fname = os.path.join(basepath, 'static', 'lang', f'bycco_{s.locale}.json')
    with open(fname, 'r') as f:
        locale_msg = json.load(f)
    sub['champ'] = locale_msg['To be confirmed']
    if s.nationalityfide == 'BEL':
        sub['champ'] = locale_msg['Yes']
    elif s.nationalityfide and len(s.nationalityfide) > 1:
        sub['champ'] = locale_msg['No']
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
    if s.badgeimage:
        parts[1].add_related(s.badgeimage, maintype, subtype, cid='1')
    mailbackend = backends[app.config["EMAIL_BACKEND"]]()
    mailbackend.send_message(msg)

def updatePhoto(id: str, photo: str) -> None:
    try:
        header, data = photo.split(',')
        upd = {
            'badgemimetype': header.split(':')[1].split(';')[0],
            'badgeimage': a2b_base64(data)
        }
        upd['badgelength'] = len(cast(str, upd['badgeimage']))
    except:
        raise BadRequest(description='BadPhotoData')
    SubscriptionModel.updateSubscription(id, upd)

def updateSubscription(id: str, updatedict: dict) -> SubscriptionModel:
    updatedict.pop('_id', None)
    updatedict.pop('id', None)
    try:
        updatedict['registrationdate'] = iso2date(updatedict.get(
            'registrationdate', None))
    except ValueError:
        log.exception('invalid registrationdate')
        raise BadRequest(description='InvalidRegistrationdate')
    try:
        updatedict['paydate'] = iso2date(updatedict.get('paydate', None))
    except ValueError:
        log.exception('invalid paydate')
        raise BadRequest(description='InvalidPaydate')
    try:
        updatedict['present'] = iso2date(updatedict.get('present', None))
    except ValueError:
        log.exception('invalid present')
        raise BadRequest(description='InvalidPresent')
    if 'rating' in updatedict and not isinstance(updatedict['rating'], int):
        log.exception('rating not a number')
        raise BadRequest(description='RatingNotNumber')
    if 'ratingbel' in updatedict and not isinstance(updatedict['ratingbel'], int):
        log.exception('rating not a number')
        raise BadRequest(description='RatingBelNotNumber')
    if 'ratingfide' in updatedict and not isinstance(updatedict['ratingfide'], int):
        log.exception('rating not a number')
        raise BadRequest(description='RatingFideNotNumber')
    if 'payamount' in updatedict and not isinstance(updatedict['payamount'], int):
        log.exception('rating not a number')
        raise BadRequest(description='PayamountNotNumber')
    return SubscriptionModel.updateSubscription(id, updatedict)
