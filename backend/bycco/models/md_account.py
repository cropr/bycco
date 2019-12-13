# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

from __future__ import annotations

import logging
import uuid
import jwt
import asyncio
from werkzeug.exceptions import NotFound, InternalServerError, Unauthorized
from passlib.apps import custom_app_context as pwd_context
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, Optional, Type, List
from datetime import datetime, timedelta
from pymongo import ReturnDocument
from bson import ObjectId
from . import MongoModel, dbconfig

log = logging.getLogger(__name__)
extrasalt = 'VascheVisch'

def uuidstr():
    return str(uuid.uuid1())

@dataclass
class AccountModel(MongoModel):
    """
    An Account
    """
    email: str
    first_name: str
    last_name: str
    mobilephone: str
    creationtime: Optional[datetime] = None
    accessrights: Dict[str, Any] = field(default_factory=dict)
    modificationtime: Optional[datetime] = None    
    password: str = ""
    tokensalt: str = field(default_factory=uuidstr)
    username: str = ""
    _id: ObjectId = field(default_factory=ObjectId)

    superuser: bool = False

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
    def create_account(cls, accountdict: Dict[str, Any]) -> AccountModel:
        """
        create a new account
        """
        try:
            accountdict['_id'] = accountdict.pop('username')
            n = datetime.utcnow()
            accountdict['modificationtime'] = accountdict['creationtime'] = n
            pwd = accountdict.pop('password')
            accountdict['tokensalt'] = uuidstr()
            cls.coll().insert_one(accountdict)
            acc = cls(**accountdict)
            if pwd: 
                acc.set_password(pwd)
            return acc
        except:
            log.exception('Cannot encode account')
            raise InternalServerError(description='CannotEncodeAccount')

    @classmethod
    def delete_account(cls, username: str) -> None:
        """
        delete an account
        """
        rs = cls.coll().delete_one({'_id': username})
        if rs.acknowledged and rs.deleted_count != 1:
            raise NotFound(description='AccountNotFound')

    @classmethod
    def get_account(cls, username:str) -> AccountModel:
        """
        get account
        """
        rs = cls.coll().find_one({'_id': username})
        if not rs:
            raise NotFound(description='AccountNotFound')                
        try:
            return cls(**rs)
        except Exception as e:
            log.exception('Cannot encode account')
            raise InternalServerError(description='CannotEncodeAccount')

    @classmethod
    def get_all_accounts(cls) -> List[AccountModel]:
        """
        get all accounts
        """
        try:
            return [cls(**doc) for doc in cls.coll().find({})]
        except:
            log.exception('Cannot encode account')
            raise InternalServerError(description='CannotEncodeAccount')

    @classmethod
    def update_account(cls, username: str, accountdict: Dict[str, Any]) -> AccountModel:
        """
        update a User
        """
        # do not update fields below
        accountdict.pop('username', None)
        accountdict.pop('password', None)
        accountdict.pop('tokensalt', None)
        accountdict.pop('accessrights', None)
        accountdict['modificationtime'] = datetime.utcnow()
        rs = cls.coll().find_one_and_update(
            {'_id': username},
            {'$set': accountdict},
            return_document=ReturnDocument.AFTER
        )
        if not rs:
            raise NotFound(description='AccountNotFound')                
        try:
            return cls(**rs)
        except:
            log.exception('Cannot encode account')
            raise InternalServerError(description='CannotEncodeAccount')

    @classmethod
    def check_token(cls: Type[AccountModel], token: str) -> AccountModel:
        """
        checks an authorization token and returns account
        raises NotFound or Unauthorized
        """
        try:
            payload = jwt.decode(token, verify=False)
        except:
            raise Unauthorized(description='InvalidToken')
        try:
            accdict = cls.coll().find_one({'_id': payload.get('username')})
            if not accdict:
                raise NotFound(description='AccountNotFound')
            account = cls(**accdict)
        except Exception:
            log.exception('Cannot encode account')
            raise Unauthorized(description='CannotEncodeAccount')
        try:
            jwt.decode(token,  extrasalt + account.tokensalt)
            return account
        except jwt.ExpiredSignatureError:
            raise Unauthorized(description='TokenExpired')
        except jwt.InvalidTokenError:
            raise Unauthorized(description='InvalidToken')

    def check_right(self, right: str) -> bool:
        """
        check if account has right 
        """
        if 'superuser' in self.accessrights:
            return True
        return self.accessrights.get(right, False)

    def get_token(self, days=30, refresh=False) -> bytes:
        """
        gets a new authorization token for an account
        """
        if refresh or not self.tokensalt:
            self.tokensalt = uuidstr()
            rs = self.coll().find_one_and_update(
                { '_id': self._id},
                {'$set': {'tokensalt': self.tokensalt}}
            )
            if not rs:
                raise NotFound(description='AccountNotFound')
        payload = {
            'username': self._id,
            'exp': datetime.utcnow() + timedelta(days=days)
        }
        return jwt.encode(payload, extrasalt + self.tokensalt, 
            algorithm='HS256')

    def remove_right(self, right: str) -> None:
        """
        remove right of qn account
        """
        self.coll().find_one_and_update({'_id': self._id}, {
            '$unset': { f'accessrights.{right}': ""}
        })

    def set_password(self, pwd: str) -> None:
        """
        sets and persists the password
        """
        self.coll().find_one_and_update( { '_id': self._id}, {'$set': {
            'password': pwd_context.encrypt(pwd),
            'modificationtime': datetime.utcnow()
        }})
    
    def update_right(self, right: str, value:Any = True) -> None:
        """
        update/add right of an account
        """
        self.coll().find_one_and_update({'_id': self._id}, { '$set': { 
            f'accessrights.{right}': value,
            'modificationtime': datetime.utcnow()
        } })

    def update_username(self, username: str) -> None:
        """
        updates the username of an account
        """
        self.coll().find_one_and_update({'_id': self._id}, { '$set': { 
            'username': username,
            'modificationtime': datetime.utcnow()
        } })
    