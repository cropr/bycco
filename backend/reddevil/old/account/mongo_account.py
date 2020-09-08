# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

# all database request come in here, but we do not use dataclasess
# if needed we define extra models an do marshalling functions at the service level
# All _id are translatesd to stringified id on output
# All functions expect stringified id as input 

import logging

from datetime import datetime, date, timezone
from typing import Dict, List, Any 
from pymongo import ReturnDocument
from pymongo.errors import DuplicateKeyError
from bson import ObjectId
from ..common import RdBadRequest, RdNotFound
from .md_account import LoginType

log = logging.getLogger('reddevil')

class DbAccount:
    COLLECTION = 'rd_account'
    DOCUMENTTYPE = 'Account'
    SIMPLEFIELDS = [ 'username']
    HIDDENFIELDS = ['password', 'tokensalt']  
    

    # the fields for this class are for documentation purposes
    # they are not used in the code

    access_rights: List[str]
    created_ts: datetime
    domain: str
    email: str
    email_verified: bool
    enabled: bool
    first_name: str
    groups: List[str]
    last_name: str
    logintype: LoginType
    locale: str 
    modified_ts: datetime
    name: str
    password = str
    password_expires_ts: datetime
    tokensalt = str    
    username: str

    @classmethod
    def create_account(cls, account_in: dict ) -> str:
        """
        create a account
        """
        from ..common import conn
        account_in['_id'] = account_in.get('_id', ObjectId())
        account_in['_documenttype'] = cls.DOCUMENTTYPE
        account_in['created_ts'] = account_in['modified_ts'] = datetime.now(timezone.utc)
        try:
            conn[1][DbAccount.COLLECTION].insert_one(account_in)
        except DuplicateKeyError:
            log.exception('account with duplicate username')
            raise RdBadRequest(description="DuplicateKeyError")
        except:
            log.exception('error inserting pagedict')
            raise RdBadRequest(description="CannotInsertPage")
        return str(account_in['_id'])

    @classmethod
    def find_accounts(cls, options: dict = {}) -> List[dict]:
        """
        find all accounts, 
        filtering on certain fields is enabled.
        """
        from ..common import conn
        accounts = []
        filter: Dict[str, Any] = {}
        if options.get('enabled'):
            filter['enabled'] = True
        _fieldlist = options.pop('_fieldlist', cls.SIMPLEFIELDS)
        if _fieldlist:
            projfields = {k:1 for k in _fieldlist}
        else:
            projfields.update({k:0 for k in cls.HIDDENFIELDS})
        cursor = conn[1][cls.COLLECTION].find(filter, projection=projfields)
        for doc in cursor:
            doc['id'] = str(doc.pop('_id'))
            accounts.append(doc)
        return accounts

    @classmethod
    def find_account(cls, options: dict) -> dict:
        """
        find an account, 
        raises NotFound if nothing is found
        """
        from ..common import conn
        if 'id' in options:
            try:
                options['_id'] = ObjectId(options.pop('id'))
            except:
                raise RdBadRequest(description='InvalidPageId')
        _fieldlist = options.pop('_fieldlist', None)
        if _fieldlist:
            projfields = {k:1 for k in _fieldlist}
        else:
            projfields = ({k:0 for k in cls.HIDDENFIELDS})
        account = conn[1][cls.COLLECTION].find_one(options, 
            projection=projfields)
        if not account:
            raise RdNotFound(description="AccountNotFound")
        account['id'] = str(account.pop('_id'))
        return account

    @classmethod
    def update_account(cls, id: str, accountupdate: Dict[str, Any] ) -> dict:
        """
        update an account
        raises NotFound if page is not found
        """
        from ..common import conn
        try:
            oid = ObjectId(id)
        except:
            raise RdBadRequest(description="InvalidAccountId")
        accountupdate['modified_ts'] = datetime.now(timezone.utc)
        account = conn[1][cls.COLLECTION].find_one_and_update({'_id': oid}, 
            {'$set': accountupdate}, projection={k:0 for k in cls.HIDDENFIELDS}, 
            return_document=ReturnDocument.AFTER)
        if not account:
            raise RdNotFound(description="AccountNotFound")
        account['id'] = str(account.pop('_id'))
        return account

    @classmethod
    def remove_account(cls, id: str) -> None:
        """
        delete an account
        """
        from ..common import conn
        try:
            oid = ObjectId(id)
        except:
            raise RdBadRequest(description="InvalidAccountId")
        rs = conn[1][cls.COLLECTION].delete_one({'_id': oid})
        if rs.deleted_count != 1:
            raise RdNotFound(description="AccountNotFound")

    @classmethod
    def set_password(cls, id: str, hashed_pwd: str) -> int:
        """
        update the password of an account
        returns 1 if successful
        """
        from ..common import conn
        try:
            oid = ObjectId(id)
        except:
            raise RdBadRequest(description="InvalidAccountId")
        rs = conn[1][cls.COLLECTION].update_one({'_id': oid}, {'$set':{
            'password': hashed_pwd
        }})
        return rs.modified_count

    @classmethod
    def set_tokensalt(cls, username: str, tokensalt: str) -> int:
        """
        update the tokensalt of an account
        returns 1 if successful
        """
        from ..common import conn
        rs = conn[1][cls.COLLECTION].update_one({'username': username}, {'$set':{
            'tokensalt': tokensalt
        }})
        return rs.modified_count

