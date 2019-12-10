# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging

from flask import request
from werkzeug.exceptions import BadRequest
from flask_restful import Resource
from bycco.service import (
    createAccount,
    deleteAccount,
    getAccount, 
    getAccounts, 
    loginAccount,
    resetPassword,
    setPassword,
    updateAccount,
    updatePassword,
)

log = logging.getLogger('bycco')

class AccountsResource(Resource):
    def get(self):
        return {'account': getAccounts()}

    def post(self):
        data = request.get_json(silent=True)
        if not data:
            raise BadRequest(description='JsonDecodingError')
        accountdict = data.get('account')
        if not accountdict:
            raise BadRequest(description='MissingAccountParameter')
        return {'account': createAccount(accountdict)}

class AccountResource(Resource):
    def get(self, username: str):
        return {'account': getAccount(username)}

    def put(self, username:str):
        data = request.get_json(silent=True)
        if not data:
            raise BadRequest(description='JsonDecodingError')
        accountdict = data.get('account')
        if not accountdict:
            raise BadRequest(description='MissingAccountParameters')
        return {'account': updateAccount(username, accountdict)}

    def delete(self, username:str):
        deleteAccount(username)
        return '', 204


class LoginResource(Resource):
    def post(self):
        data = request.get_json(silent=True)
        if not data:
            raise BadRequest(description='JsonDecodingError')
        command = data.get('command')
        if not command:
            raise BadRequest(description='MissingCommand')
        if command == 'login':
            return {'token': loginAccount(data)}
        elif command == 'resetPassword':
            resetPassword(data)
            return '', 204
        elif command == 'setPassword':
            setPassword(data)
            return '', 204
        elif command == 'updatePassword':
            updatePassword(data)
            return '', 204
        else:
            raise BadRequest(description='CommandNotImplemented')        


