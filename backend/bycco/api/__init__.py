# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

from flask_restful import Resource, Api
from .. import app
apimgr = Api(app)

from .api_lang import LangResource
apimgr.add_resource(LangResource, '/api/lang/<lang>')

from .api_page import (
    PageResource, 
    PagesResource,
    SlugResource,
    SlugLocaleResource,
)
apimgr.add_resource(PagesResource, '/api/page')
apimgr.add_resource(PageResource, '/api/page/<id>')
apimgr.add_resource(SlugResource, '/api/slug/<slug>')
apimgr.add_resource(SlugLocaleResource, '/api/slug/<slug>/locale/<locale>')

from .api_document import (
    DocumentResource, 
    DocumentsResource,
)
apimgr.add_resource(DocumentsResource, '/api/document')
apimgr.add_resource(DocumentResource, '/api/document/<id>')

from .api_playerlist import (
    BelplayerResource, 
    FideplayerResource,
)
apimgr.add_resource(BelplayerResource, '/api/belplayer/<id>')
apimgr.add_resource(FideplayerResource, '/api/fideplayer/<id>')

from .api_subscription import (
    SubscriptionsResource,
    SubscriptionResource,
    SubscriptionConfirmResource,
    SubscriptionPhotoResource,
)
apimgr.add_resource(SubscriptionsResource, '/api/subscriptions')
apimgr.add_resource(SubscriptionResource, '/api/subscriptions/<id>')
apimgr.add_resource(SubscriptionConfirmResource, 
    '/api/subscriptions/<id>/confirm')
apimgr.add_resource(SubscriptionPhotoResource, 
    '/api/subscriptions/<id>/photo')

from .api_attendee import  AttendeesResource
apimgr.add_resource(AttendeesResource, '/api/attendee')


from .api_account import (
    AccountResource,
    AccountsResource,
    LoginResource
)

apimgr.add_resource(AccountsResource, '/api/account')
apimgr.add_resource(AccountResource, '/api/account/<username>')
apimgr.add_resource(LoginResource, '/api/login')

