# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging

import json
from datetime import datetime

from passlib.apps import custom_app_context as pwd_context
from flask import render_template, abort, request
from werkzeug.exceptions import NotFound, Forbidden, BadRequest, Unauthorized
from typing import List, Optional, Union
from bycco import app
from bycco.models import AccountModel

log = logging.getLogger('bycco')

def getAccounts() -> List[AccountModel]:
    """
    get all accounts
    """
    return AccountModel.get_all_accounts()

def createAccount(accountdict: dict) -> AccountModel:
    """
    add an account
    """    
    if not accountdict:
        raise BadRequest(description='MissingAccountParameter')
    return AccountModel.create_account(accountdict)

def getAccount(username: str) -> AccountModel:
    """
    get details of a user
    """
    return AccountModel.get_account(username)

def updateAccount(username: str, accountdict: dict) -> AccountModel:
    """
    update an account 
    """
    return AccountModel.update_account(username, accountdict)

def deleteAccount(username) -> None:
    """
    delete an account
    """
    return AccountModel.delete_account(username)

def loginAccount(body:  dict) -> str:
    """
    gets a JWT Token for the user, providing username and password
    """
    username = body.get('username')
    password = body.get('password')
    if not username or not password:
        raise BadRequest(description='MissingParameters')
    account = AccountModel.get_account(username)
    if not pwd_context.verify(password, account.password):
        raise Unauthorized(description='WrongUsernamePassword')
    log.info(f'user {username} logged in')
    return account.get_token().decode('utf-8')
    
def request2account() -> AccountModel:
    """
    return the associated account of the request
    """
    authheader = request.headers.get('Authorization')
    if not authheader:
        raise Unauthorized(description='MissingToken')
    auth = authheader.split()
    if auth[0] != 'Bearer' or len(auth) != 2:
        raise Unauthorized(description='InvalidToken')
    return AccountModel.check_token(auth[1])

def resetPassword():
    pass

def setPassword():
    pass
   
def updatePassword():
    pass
