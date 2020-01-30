# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging

import json, os.path, io, csv
from typing import List, Optional, Dict, Any, cast
import dataclasses
from datetime import date
from flask import render_template, Response
from binascii import a2b_base64
from werkzeug.exceptions import NotFound, BadRequest
from bs4 import BeautifulSoup
from email.message import EmailMessage, Message
from email.utils import make_msgid
from bycco import app
from bycco.models import (
    Attendee,
    BasicSubscription, 
    BelplayerModel,
    FideplayerModel,
    SubscriptionModel, 
)
from bycco.service.mail import backends

log = logging.getLogger('bycco')

def addAttendee(ss: dict) -> str:
    """
    add a new subscription
    """
    log.info('add attendees')
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
    return cs.id

def deleteAttendee(id: str) -> None:
    pass

def getAttendees(options: dict) ->  List[Attendee]:
    """
    get all attendees
    """
    return SubscriptionModel.get_attendees(options)

def getAttendeesCsv() ->  str:
    """
    get all attendees
    """
    fieldnames = [f.name for f in dataclasses.fields(SubscriptionModel)]
    csvstr = io.StringIO()
    csvf = csv.DictWriter(csvstr, fieldnames)
    csvf.writeheader()
    for sub in SubscriptionModel.csv_subscriptions():
        csvf.writerow(sub)
    return csvstr.getvalue()

def getAttendee(id: str) -> SubscriptionModel:
    """
    get one subscription
    """
    log.info('get subsription')
    return SubscriptionModel.find_by_id(id)

def updateAttendee(id: str) -> None:
    pass
    # try:
    #     header, data = photo.split(',')
    #     upd = {
    #         'badgemimetype': header.split(':')[1].split(';')[0],
    #         'badgeimage': a2b_base64(data)
    #     }
    #     upd['badgelength'] = len(upd['badgeimage'])
    # except:
    #     raise BadRequest(description='BadPhotoData')
    # SubscriptionModel.updateSubscription(id, upd)

