# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging

import json
from flask import render_template, abort
from typing import List, Optional
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

def addSubscription() -> List[BasicSubscription]:
    """
    get all subscriptions
    """
    log.info('get subsriptions')
    subs = SubscriptionModel.find_subscriptions()
    return subs