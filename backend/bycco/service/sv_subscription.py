# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging

import json, os.path, io, csv
from typing import List, Optional, Dict, Any, cast
from datetime import date, datetime, timezone
from bycco.service.sv_playerlist import getBelplayer, getFideplayer
from reddevil.common import RdInternalServerError
from bycco.service.mail import sendconfirmationmail

from bycco.models.md_subscription import (
    Subscription,
    SubscriptionDetailedOut,
    SubscriptionIn,
    SubscriptionList,
    SubscriptionOut,
    SubscriptionOptional,
    SubscriptionCategory,
    CheckIdReply
)
from bycco.crud.db_subscription import DbSubscription
from reddevil.common import RdNotFound, RdBadRequest

log = logging.getLogger('bycco')

def encode_subscription(e: dict, cls=SubscriptionDetailedOut):
    try:
        o = cls(**e)
    except Exception:
        log.exception(f'cannot encode {cls.__name__}')
        raise RdInternalServerError(description='CannotEncodeSubscription')
    return o

async def addSubscription(si: SubscriptionIn) -> str:
    """
    add a new subscription
    """
    bp = getBelplayer(si.idbel)
    log.info(f'bp.idfide {bp.idfide}')
    try:
        fp = getFideplayer(bp.idfide) if bp.idfide else None
    except Exception:
        log.warning(f'Fide id {bp.idfide} unknown in fide.sqlite')
        fp = None
    try:
        subdict = await DbSubscription.find_single({'idbel': bp.id})
        raise RdBadRequest(description="Alreadysubscribed")        
    except RdNotFound:
        pass
    maxsubnr = await DbSubscription.maxSubsciptionNumber()
    s = {
        'birthdate': bp.birthdate,
        'category': si.category,
        'chesstitle': fp.chesstitle if fp else '',
        'confirmed': False,
        'custom': '', 
        'emailattendant': '',
        'emailparent': '',
        'emailplayer': '',
        'federation': bp.federation,
        'first_name': bp.first_name,
        'fullnameattendant': '',
        'fullnameparent': '',
        'gender': bp.gender,
        'idbel': si.idbel,
        'idclub': bp.idclub,
        'idfide': bp.idfide,
        'invoicenumber': None,
        'locale': si.locale,
        'last_name': bp.last_name,
        'mobileattendant': '',
        'mobileparent': '',
        'mobileplayer': '',
        'nationality': bp.nationality,
        'payamount': 35,
        'paydate': None,
        'paymessage': None,
        'present': None,
        'ratingbel': bp.ratingbel,
        'ratingfide': fp.ratingfide if fp else 0,
        'remarks': '',
        'subscriptiontime': datetime.now(tz=timezone.utc),
        'subscriptionnumber': maxsubnr + 1,
    }
    return await DbSubscription.add(s)

async def confirmSubscription(id: str):
    s = await getSubscription(id)
    if s.confirmed:
        raise RdBadRequest(description="AlreadyConfirmed")
    invoicenumber = await DbSubscription.maxInvoiceNumber() + 1
    nr = int(2020010000 + invoicenumber)
    rm1 = invoicenumber // 1000
    rm2 = invoicenumber % 1000
    rm3 = nr % 97 or 97
    paymessage = f"+++202/001{rm1:01d}/{rm2:03d}{rm3:02d}+++"
    s = await updateSubscription(id, SubscriptionOptional(
        confirmed = True,
        invoicenumber = invoicenumber,
        paymessage = paymessage,
        payamount = 35
    ))
    sendconfirmationmail(s)
    return s

async def deleteSubscription(id: str) -> None:
    await DbSubscription.delete(id)

async def getSubscriptions(options: dict={}, cls=SubscriptionOut) -> SubscriptionList:
    """
    get all subscriptions
    """
    sdict = await DbSubscription.find_multiple(options)
    log.info(f'sdict {sdict}')
    return SubscriptionList(subscriptions=
        [encode_subscription(s, cls) for s in sdict])

async def getSubscriptionsPerCategory(cat: str) -> SubscriptionList:
    """
    get all subscriptions
    """
    options: dict = {
        'confirmed':  True,
        '_fieldlist': [
            'category', 'chesstitle', 'confirmed', 'first_name', 'gender', 
            'id', 'idbel', 'idclub', 'last_name', 'ratingbel', 'ratingfide', 
        ]
    }
    if cat != 'all':
        cats = cat.split(',')
        if len(cats) == 1:
            options['category'] = cats[0]
        else:
            options['category'] = { '$in': cats}
    return await getSubscriptions(options, cls=SubscriptionOptional) 

async def getSubscription(id: str, options: dict= {}, 
        cls=SubscriptionDetailedOut) -> SubscriptionOptional:
    """
    get one subscription,
    with options given to the DB backend
    encode the result as cls instance
    """
    filter = dict(id=id, **options)
    sdict = await DbSubscription.find_single(filter)
    return encode_subscription(sdict, cls)

async def updateSubscription(id: str, su: SubscriptionOptional):
    sd = su.dict(exclude_unset=True)
    sd.pop('id', None)
    udd = await DbSubscription.update(id, sd)
    return encode_subscription(udd, SubscriptionDetailedOut)
    
async def checkId(idbel: str) -> CheckIdReply:
    """
    fill in
    """
    try:
        bp = getBelplayer(idbel)
        if not bp:
            return CheckIdReply(belfound=False)
    except Exception:
        return CheckIdReply(belfound=False)
    try:
        fp = getFideplayer(bp.idfide) if bp.idfide else None
    except:
        log.warning(f'Fide id {bp.idfide} unknown in fide.sqlite')
        fp = None
    try:
        sdict = await DbSubscription.find_single({'idbel': idbel})
    except RdNotFound:
        sdict = {}
    return CheckIdReply(
        affiliated = bp.affiliated,
        belfound = True,
        birthyear = bp.birthdate[0:4],
        fidefound = bool(fp),
        first_name = bp.first_name,
        gender = bp.gender,
        last_name = bp.last_name,
        ratingbel = bp.ratingbel,
        ratingfide = fp.ratingfide if fp else 0,
        subconfirmed = sdict.get('confirmed', False),        
        subfound = bool(sdict),
        subid =  sdict.get('id', False),
    )

async def csvSubscriptions() -> str:
    """
    get all subscriptions in csv format
    """
    fieldnames = list(SubscriptionOptional.__fields__.keys())
    csvstr = io.StringIO()
    csvf = csv.DictWriter(csvstr, fieldnames)
    csvf.writeheader()
    subs = (await getSubscriptions({'_fieldlist': [
        'birthdate', 'category', 'chesstitle', 'confirmed', 'custom',
        'emailattendant', 'emailparent', 'emailplayer', 'federation', 
        'first_name', 'fullnameattendant', 'fullnameparent', 'gender', 
        'id', 'idbel', 'idclub', 'idfide', 'invoicenumber', 'locale',
        'last_name', 'mobileattendant', 'mobileparent', 'mobileplayer', 
        'nationality', 'payamount', 'paydate', 'paymessage', 'present',
        'ratingbel', 'ratingfide', 'remarks', 'subscriptiontime', 
        'subscriptionnumber',
    ]}, cls=SubscriptionOptional)).subscriptions
    for sub in subs:
        csvf.writerow(sub.dict())
    return csvstr.getvalue()    

