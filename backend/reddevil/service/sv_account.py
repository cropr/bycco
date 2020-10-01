# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging
import json
import uuid
import asyncio
from jose import jwt, JWTError, ExpiredSignatureError
from passlib.context import CryptContext
from fastapi.security import HTTPBearer
from google.oauth2 import id_token
from google.auth.transport import requests
from datetime import datetime, timedelta
from typing import List, Optional, Union

from reddevil.common import (
    cfg,
    RdInternalServerError, 
    RdBadRequest,
    RdNotAuthorized,
    RdNotFound,
)

from reddevil.models.md_account import (
    AccountDetailedOut,
    AccountDetailedIn,
    AccountIn,
    AccountListOut,
    AccountOut,
    AccountOptional,
    LoginType,
    LoginIn,
)

from reddevil.crud.db_account import DbAccount

log = logging.getLogger("reddevil")

bearer_schema = HTTPBearer(auto_error=False)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    """
    return the password hashed
    """
    return pwd_context.hash(password)

def verify_password(plain:str, hash: str):
    """
    verify hash is the plain password hashed
    """
    return pwd_context.verify(plain, hash)

async def get_token(acc: AccountOptional, duration: timedelta, 
    invalidate: bool=True
) -> str:
    """
    gets a new JWT token for a user
    :param acc: an AccountOptional
    :param invalidate: invalidate the existing tokens by changing the salt
    :return: return the newly created token
    """
    id = acc.id
    if invalidate or acc.tokensalt is None:
        tokensalt = str(uuid.uuid1())
        await DbAccount.update(acc.id, {'tokensalt': tokensalt})
    else:
        tokensalt = acc.tokensalt
        await asyncio.sleep(0)   # a noop await
    payload = {
        'username': acc.id,
        'exp': datetime.utcnow() + duration
    }
    return jwt.encode(payload, cfg.TOKEN["secret"] + tokensalt, 
        algorithm=cfg.TOKEN["algorithm"])

async def validate_token(
    token: Optional[str], raises: bool = True
) -> AccountOptional:
    """
    checks a JWT token for validity
    return an AccountRights if the token is correctly validated
    if token is not valid the function :
        - either returns None  
        - either raise RdNotAuthorized if raising is set
    """
    if cfg.TOKEN.get('nocheck'):
        return None
    if not token:
        if raises:
            raise RdNotAuthorized(description='MissingToken')
        return None
    try:
        payload = jwt.decode(token, verify=False)
    except:
        log.debug('invalid token without verification')
        if raises:
            raise RdNotAuthorized(description='BadToken')
        return None
    try:
        username = payload.get('sub')
        acc = await DbAccount.find_single({'id': username},{
            '_class': AccountOptional,
            '_fieldlist': ['tokensalt', 'scopes', 'groups', 'superuser'],
        })
        tokensalt = acc.pop('tokensalt')
    except RdNotFound:
        log.debug(f'account {username} not found')
        if raises:
            raise RdNotAuthorized(description='BadToken')
        return None
    try:
        jwt.decode(token, cfg.TOKEN["secret"] + tokensalt)
    except JWTError:
        if raises:
            log.debug('JWT Error')
            raise RdNotAuthorized(description='BadToken')
        return None
    except ExpiredSignatureError:
        if raises:
            log.debug('JWT Error')
            raise RdNotAuthorized(description='TokenExpired')
        return None
    try:
        return acc
    except Exception as e:
        log.exception('cannot encode account rights')
        raise RdInternalServerError(description='CannotEncodeAccountRights')

def encode_account(e: dict, _class=AccountDetailedOut):
    try:
        eo = _class(**e)
    except Exception:
        log.exception('cannot encode Account')
        raise RdInternalServerError(description='CannotEncodeAccount')
    return eo

async def createAccount(d: AccountIn) -> str:
    """
    create a new Account 
    """
    dd = d.dict()
    dd['logintype'] = LoginType.google
    dd['tokensalt'] = str(uuid.uuid1())
    return await DbAccount.add(dd)

async def deleteAccount(id: str) -> None:
    """
    delete the zccount 
    """
    await DbAccount.delete(id)

async def getAccount(id: str, options: dict= {}) -> AccountDetailedOut:
    """
    get the account 
    """
    _class = options.pop('_class', AccountDetailedOut)
    filter = dict(id=id, **options)
    adict = await DbAccount.find_single(filter)
    return encode_account(adict, _class)

async def getAccounts(options: dict = {}) -> AccountListOut:
    """
    get all account
    """
    _class = options.pop('_class', AccountOut)
    accs = await DbAccount.find_multiple(options)
    accounts = [encode_account(a, _class) for a in accs]
    return AccountListOut(accounts=accounts)  

async def updateAccount(id: str, d: AccountDetailedIn) -> AccountDetailedOut:
    """
    update a Account
    """
    # import dates as isoformat string
    dd = d.dict(exclude_unset=True)
    udd = await DbAccount.update_account(id, dd)
    return encode_account(udd)

async def login_account(li: LoginIn) -> str:
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
                acc = await getAccount(idinfo['sub'],{
                    '_class': AccountOptional,
                    '_fieldlist': ['id', 'tokensalt'],
                })
            except RdNotFound:
                log.info(f'account not found creating ...')
                accdict = {
                    'domain': idinfo['hd'],
                    'email': idinfo['email'],
                    'email_verified': idinfo['email_verified'],
                    'enabled': True,
                    'first_name': idinfo['given_name'],
                    'id': idinfo['sub'],
                    'last_name': idinfo['family_name'],
                    'locale': idinfo['locale'],
                    'logintype': LoginType.google,
                }
                id = await DbAccount.add(accdict)
                acc = DbAccount.find_single(idinfo['sub'],{
                    '_class': AccountOptional,
                    '_fieldlist': ['id', 'tokensalt'],
                })
            token = await get_token(acc, timedelta(minutes=cfg.TOKEN['timeout']))
            return token    
        except ValueError:
            raise RdNotAuthorized(description='InvalidGoogleToken')
    # elif li.logintype == LoginType.email:
    #     return "a"
    else:
        raise RdBadRequest(description='InvalidLoginType')

