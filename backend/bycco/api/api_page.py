# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

from flask_restful import Resource
from bycco.service import getPageContent, getPages


class PagesResource(Resource):
    def get(self):
        return getPages()


class PageResource(Resource):
    def get(self, slug:str, lang:str):
        return getPageContent(slug, lang)

