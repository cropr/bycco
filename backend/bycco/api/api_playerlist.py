# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging

from flask import request
from werkzeug.exceptions import BadRequest
from flask_restful import Resource
from bycco.service import (
    getBelplayer,
    getFideplayer,
)

log = logging.getLogger('bycco')

class BelplayerResource(Resource):
    def get(self, id):
        return {'belplayer': getBelplayer(id)}

class FideplayerResource(Resource):
    def get(self, id):
        return {'fideplayer': getFideplayer(id)}
