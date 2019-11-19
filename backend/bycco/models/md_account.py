# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

from __future__ import annotations

import logging
import uuid
import jwt
import asyncio
from passlib.apps import custom_app_context as pwd_context
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, TYPE_CHECKING
from datetime import datetime, timedelta
from pymongo import ReturnDocument
from bson import ObjectId
from . import MongoModel, dbconfig

log = logging.getLogger(__name__)

if TYPE_CHECKING:
    from .md_account import AccountModel

extrasalt = 'LailijkeBaiste'

def uuidstr():
    return str(uuid.uuid1())

@dataclass
class AccountModel(MongoModel):
    """
    An Account
    """
    first_name: str
    last_name: str
    email: str
    mobilephone: str
    password: str = ""
    username: str = ""
    creationtime: datetime = None
    modificationtime: datetime = None    
    tokensalt: str = field(default_factory=uuidstr)
    _id: ObjectId = field(default_factory=ObjectId)

    _collection = 'account'
    # never disclose password and tokensalt 
    _hidden = ['_id', 'password', 'tokensalt'] 
    
    # attribute username is created automatically as alias of _id
    def __post_init__(self):
        self.username = self.username or self._id
        if not self.creationtime:
            self.creationtime = datetime.utcnow()
        if not self.modificationtime:
            self.modificationtime = datetime.utcnow()

    @classmethod
    def get_user(cls, username:str) -> AccountModel:
        """
        get User
        #param: evdict: as defined in ElectionEventNewSchema
        """
        coll = dbconfig['db'][cls._collection]
        rs = coll.find_one({'_id': username})
        if not rs:
            raise ApiException(status_code=404, reason='UserNotFound')                
        try:
            return  cls(**rs)
        except Exception as e:
            log.execption('Cannot get account')
            raise e

    @classmethod
    def get_all_users(cls) -> AccountModel:
        """
        get all users
        """
        coll = dbconfig['db'][cls._collection]
        users = [AccountModel(**doc) for doc in coll.find({})]
        return users

    @classmethod
    def update_user(cls, 
                username: str, 
                userdict: Dict[str, Any],
            ) -> AccountModel:
        """
        update a User
        #param: username: the username
        #param: userdict: updated fields
        """
        coll = dbconfig['db'][cls._collection]
        # do not update fields below
        userdict.pop('username', None)
        userdict.pop('password', None)
        userdict.pop('tokensalt', None)
        rs = coll.find_one_and_update(
            {'_id': username},
            {'$set': userdict},
            return_document=ReturnDocument.AFTER
        )
        if not rs:
            raise ApiException(status_code=404, reason='UserNotFound')                
        try:
            return  cls(**rs)
        except Exception as e:
            log.execption('Cannot update account')
            raise e

    @classmethod
    def delete_user(cls, username: str) -> None:
        """
        delete a user
        #param username: 
        """
        coll = dbconfig['db'][cls._collection]
        rs = coll.delete_one({'_id': username})
        if rs.acknowledged and rs.deleted_count != 1:
            raise ApiException(status_code=404, reason='AccountNotFound')

    @classmethod
    def create(cls, accountdict: Dict[str, Any]) -> AccountModel:
        """
        add a new account
        #param: accountdict as in schema UserNew
        """
        coll = dbconfig['db'][cls._collection]
        try:
            accountdict['_id'] = accountdict.pop('username')
            pwd = accountdict.pop('password')
            accountdict['tokensalt'] = uuidstr()
            coll.insert_one(accountdict)
            acc = cls(**accountdict)
            if pwd: 
                acc.set_password(pwd)
            return acc
        except Exception as e:
            log.exception('Cannot create account')
            raise e

    def get_token(self, days=30, refresh=False):
        """
        gets a new token
        :param days: # of days the token is valid
        :param refresh: create a new token, invalidating the existing tokens
        :return: return the newly created token
        """
        coll = dbconfig['db'][self._collection]
        if refresh or not self.tokensalt:
            self.tokensalt = uuidstr()
            rs = coll.find_one_and_update(
                { '_id': self._id},
                {'$set': {'tokensalt': self.tokensalt}}
            )
            if not rs:
                raise ApiException(status_code=404, reason='CannotUpdateAccount')
        else:
            asyncio.sleep(0)
        payload = {
            'username': self._id,
            'exp': datetime.utcnow() + timedelta(days=days)
        }
        return jwt.encode(payload, extrasalt + self.tokensalt, 
            algorithm='HS256')

    @classmethod
    def check_token(cls, token):
        """
        checks an authorization token
        :param token:
        :return: the accountModel or raises exception
        """
        coll = dbconfig['db'][cls._collection]
        try:
            payload = jwt.decode(token, verify=False)
        except:
            raise ApiException(status_code=401, reason='InvalidToken')
        try:
            accdict = coll.find_one({'_id': payload.get('username')})
            if not accdict:
                raise ApiException(status_code=401, reason='AccountNotFound')
            account = cls(**accdict)
            jwt.decode(token,  extrasalt + account.tokensalt)
        except jwt.ExpiredSignatureError:
            raise ApiException(status_code=401, reason='TokenExpired')
        except jwt.InvalidTokenError:
            raise ApiException(status_code=401, reason='InvalidToken')
        except Exception:
            log.exception('Cannot get account from token')
            raise ApiException(status_code=401, reason='InvalidToken')
        return account

    def set_password(self, pwd):
        """
        sets and persists the password
        :param pwd:
        :return: None
        """
        coll = dbconfig['db'][self._collection]
        coll.find_one_and_update(
            { '_id': self._id},
            {'$set': {'password': pwd_context.encrypt(pwd)}}
        )