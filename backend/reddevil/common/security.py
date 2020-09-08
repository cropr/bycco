# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging
log = logging.getLogger(__name__)

from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from jose import jwt

from .errors import (
    RdBadRequest,
    RdException,
    RdInternalServerError,
    RdNotFound,
    RdNotAuthorized,
)

# from ..account.md_account import UserRights

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/mgmt/login")
oauth2_optional = OAuth2PasswordBearer(tokenUrl="/mgmt/login", auto_error=False)

bearer_schema = HTTPBearer(auto_error=False)

def check_token(token: str):
    pass

# def check_token(token: str) -> UserRights:
#     """
#     checks a JWT token for validity
#     return a UserRights or riase an RdNotAuthorized exception
#     """
#     from reddevil.account.sv_account import DbAccount
#     from reddevil.account.md_account import UserRights
#     from reddevil.common import cfg
#     if not token:
#         raise RdNotAuthorized(description='MissingToken')
#     log.debug(f'token {token}')
#     try:
#         payload = jwt.decode(token, verify=False)
#     except:
#         log.info('Could not decode token')
#         raise RdNotAuthorized(description='BadToken')
#     try:
#         username = payload.get('username')
#         acc = DbAccount.find_account({
#             'username': username,
#             '_fieldlist': ['tokensalt', 'username', 'access_rights', 'groups', 'email'],
#         })
#         log.debug(f'user {acc["email"]} {username} logged in')
#     except RdNotFound:
#         log.info('could not find username to authorize')
#         raise RdNotAuthorized(description='BadToken')
#     tokensalt = acc.pop('tokensalt')
#     try:
#         jwt.decode(token, cfg.EXTRASALT + tokensalt)
#     except jwt.ExpiredSignatureError:
#         raise RdNotAuthorized(description='TokenExpired')
#     except jwt.InvalidTokenError:
#         raise RdNotAuthorized(description='BadToken')
#     return UserRights(**acc)

