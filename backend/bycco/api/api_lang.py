# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

from flask_restful import Resource
from bycco.service import getLanguageFile

class LangResource(Resource):
    def get(self, lang):
        return getLanguageFile(lang)

