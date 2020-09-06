# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging
log = logging.getLogger(__name__)

import json
import jwt
import uuid
from google.oauth2 import id_token
from google.auth.transport import requests
from datetime import datetime, timedelta
from passlib.apps import custom_app_context as pwd_context
from typing import List, Optional, Union
from ..common import (
    cfg,
    iso2date,
    resolve_method_module, 
    RdInternalServerError, 
    RdBadRequest,
    RdNotFound,
    RdNotAuthorized,
)

from .md_account import (
    AccountDetailedIn,
    AccountDetailedOut,
    AccountIn,
    AccountListOut,
    LoginIn,
    LoginType,
)

DbAccount = resolve_method_module(f'reddevil.account.{cfg.DATASTORE["prefix"]}_account', 
    'DbAccount')

def createAccount(d: AccountIn) -> str:
    """
    create a new Account 
    """
    dd = d.dict()
    dd['logintype'] = LoginType.google
    dd['tokensalt'] = str(uuid.uuid1())
    return DbAccount.create_account(dd)

def deleteAccount(id: str) -> None:
    """
    delete the zccount 
    """
    DbAccount.remove_account(id)

def getAccount(id: str) -> AccountDetailedOut:
    """
    get the account 
    """
    d = DbAccount.find_account({'id': id})
    return AccountDetailedOut(**d)

def getAccounts(options: dict = {}) -> AccountListOut:
    """
    get all account
    """
    dl = DbAccount.find_accounts(options)
    return AccountListOut(Accounts=dl)

def updateAccount(id: str, d: AccountDetailedIn) -> AccountDetailedOut:
    """
    update a Account
    """
    # import dates as isoformat string
    dd = d.dict(exclude_unset=True)
    udd = DbAccount.update_account(id, dd)
    return AccountDetailedOut(**udd)

def get_token(userdict: dict, days: int=30, invalidate: bool=True) -> str:
    """
    gets a new JWT token for a user
    :param userdict: a dict with username and tokensalt keys
    :param days: # of days the token is valid
    :param invalidate: invalidate the existing tokens by changing the salt
    :return: return the newly created token
    """
    username = userdict['username']
    if invalidate or 'tokensalt' not in userdict:
        tokensalt = str(uuid.uuid1())
        DbAccount.set_tokensalt(username, tokensalt)
    else:
        tokensalt = userdict['tokensalt']
    payload = {
        'username': username,
        'exp': datetime.utcnow() + timedelta(days=days)
    }
    return jwt.encode(payload, cfg.EXTRASALT + tokensalt, algorithm='HS256').decode('UTF-8')

def loginAccount(li: LoginIn) -> str:
    """
    login and returns a newly create JWT token
    """
    if li.logintype == LoginType.google:
        assert li.token is not None
        log.info(f'login google {li.token[0:8]}...')
        token = li.token
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), 
                cfg.GOOGLE_CLIENT_ID)
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise RdNotAuthorized(description='WrongAuthIssuer')
            if cfg.GOOGLE_LOGIN_DOMAINS and idinfo['hd'] not in cfg.GOOGLE_LOGIN_DOMAINS:
                raise RdNotAuthorized(description='WrongGoogleDomain')
            try: 
                acc = DbAccount.find_account({
                    'username': idinfo['sub'],
                    'logintype': LoginType.google,
                    '_fieldlist': ['username', 'tokensalt'],
                })
            except RdNotFound:
                log.info(f'account not found creating ...')
                acc = None
            if acc is None:
                accdict = {
                    'domain': idinfo['hd'],
                    'email': idinfo['email'],
                    'email_verified': idinfo['email_verified'],
                    'enabled': True,
                    'first_name': idinfo['given_name'],
                    'last_name': idinfo['family_name'],
                    'locale': idinfo['locale'],
                    'logintype': LoginType.google,
                    'username': idinfo['sub'],
                }
                id = DbAccount.create_account(accdict)
                acc = DbAccount.find_account({
                    'id': id,
                    '_fieldlist': ['username', 'tokensalt'] 
                })
            token = get_token(acc)
            return token    
        except ValueError:
            raise RdNotAuthorized(description='InvalidGoogleToken')
    # elif li.logintype == LoginType.email:
    #     return "a"
    else:
        raise RdBadRequest(description='InvalidLoginType')