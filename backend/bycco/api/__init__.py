# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

from flask_restful import Resource, Api
from .. import app
from .api_lang import LangResource
from .api_page import PageResource, PagesResource

apimgr = Api(app)
apimgr.add_resource(LangResource, '/api/lang/<lang>')
apimgr.add_resource(PageResource, '/api/page/<slug>/<lang>')
apimgr.add_resource(PagesResource, '/api/pages')