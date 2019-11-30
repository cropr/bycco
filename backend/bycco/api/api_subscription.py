# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

from flask_restful import Resource, request, BadRequest
from bycco.service import (
    getSubscriptions, 
    addSubscription, 
    confirmSubscription,
)

class SubscriptionsResource(Resource):
    def get(self) -> dict:
        return {'subscriptions': getSubscriptions()}
    def post(self) -> dict:
        data = request.get_json(silent=True)
        if not data:
            raise BadRequest(description='JsonDecodingError')
        subdict = data.get('subscription')
        if not subdict:
            raise BadRequest(description='MissingSubscriptionParameter')
        return {'subscription': addSubscription(subdict)}

    def put(self) -> dict:
        data = request.get_json(silent=True)
        if not data:
            raise BadRequest(description='JsonDecodingError')
        subdict = data.get('subscription')
        if not subdict:
            raise BadRequest(description='MissingSubscriptionParameter')
        # return {'subscription': updateSubscription(subdict)}
        return {}


class SubscriptionConfirmResource(Resource):
    def post(self, id:str) -> tuple:
        return '', 204

class SubscriptionPhotoResource(Resource):
    def get(self, id:str) -> dict:
        pass
    def post(self, id:str) -> dict:
        data = request.get_json(silent=True)
        if not data:
            raise BadRequest(description='JsonDecodingError')
        photo = data.get('subscription')
        if not photo:
            raise BadRequest(description='MissingPhotoParameter')
        return {}