# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging

from flask import request
from werkzeug.exceptions import BadRequest
from flask_restful import Resource
from bycco.service import (
    getDocs,
    getDoc,
    createDoc,
    updateDoc,
)

log = logging.getLogger('bycco')

class DocumentsResource(Resource):
    def get(self):
        options = request.args.to_dict()
        return {'documents': getDocs(options)}

    def post(self):
        data = request.get_json(silent=True)
        if not data:
            raise BadRequest(description='JsonDecodingError')
        docdict = data.get('document')
        if not docdict:
            raise BadRequest(description='MissingDocParameter')
        return {'id': createDoc(docdict)}

class DocumentResource(Resource):
    def get(self, id: str):
        return {'document': getDoc(id)}

    def put(self, id:str):
        data = request.get_json(silent=True)
        if not data:
            raise BadRequest(description='JsonDecodingError')
        docdict = data.get('document')
        if not docdict:
            raise BadRequest(description='MissingDocParameters')
        return {'document': updateDoc(id, docdict)}
