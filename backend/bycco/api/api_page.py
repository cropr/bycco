# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging

from flask import request
from werkzeug.exceptions import BadRequest
from flask_restful import Resource
from bycco.service import (
    getPage, 
    getPages, 
    getPageBySlug, 
    getPageBySlugLocale,
    updatePage,
)

log = logging.getLogger('bycco')

class PagesResource(Resource):
    def get(self):
        return {'pages': getPages()}

class PageResource(Resource):
    def get(self, id: str):
        return {'page': getPage(id)}

    def put(self, id:str):
        data = request.get_json(silent=True)
        if not data:
            raise BadRequest(description='JsonDecodingError')
        pagedict = data.get('page')
        if not pagedict:
            raise BadRequest(description='MissingPageParameters')
        return {'page': updatePage(id, pagedict)}

class SlugResource(Resource):
    def get(self, slug: str):
        return {'page': getPageBySlug(slug)}

class SlugLocaleResource(Resource):
    def get(self, slug: str, locale: str):
        return {'page': getPageBySlugLocale(slug, locale)}
