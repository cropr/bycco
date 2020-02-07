# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

from flask_restful import Resource, request
from werkzeug.exceptions import BadRequest
from bycco.service import (
    addSubscription, 
    confirmSubscription,
    csvSubscriptions,
    deleteSubscription,
    getSubscriptions,
    getSubscription,
    getSubscriptionByIdbel, 
    updatePhoto,
    updateSubscription,
)

class SubscriptionsResource(Resource):
    
    def get(self) -> dict:
        format = request.args.get('format', 'json')
        if format == 'csv':
            return {'subscriptions': csvSubscriptions()}
        else:
            return {'subscriptions': getSubscriptions()}

    def post(self) -> dict:
        data = request.get_json(silent=True)
        if not data:
            raise BadRequest(description='JsonDecodingError')
        subdict = data.get('subscription')
        if not subdict:
            raise BadRequest(description='MissingSubscriptionParameter')
        return addSubscription(subdict)

class SubscriptionResource(Resource):
    
    def get(self, id:str) -> dict:
        idtype = request.args.get('idtype', 'db')
        if idtype == 'db':
            s = {'subscription': getSubscription(id)}
        if idtype == 'bel':
            s = {'subscription': getSubscriptionByIdbel(id)}
        return s

    def put(self, id:str) -> dict:
        data = request.get_json(silent=True)
        if not data:
            raise BadRequest(description='JsonDecodingError')
        subdict = data.get('subscription')
        if not subdict:
            raise BadRequest(description='MissingSubscriptionParameter')
        return {'subscription': updateSubscription(id, subdict)}

    def delete(self, id:str) -> tuple:
        deleteSubscription(id)
        return '', 204


class SubscriptionConfirmResource(Resource):

    def post(self, id:str) -> dict:
        pm = confirmSubscription(id)
        return {'paymessage': pm}


class SubscriptionPhotoResource(Resource):

    def get(self, id:str) -> dict:
        pass

    def post(self, id:str) -> tuple:
        data = request.get_json(silent=True)
        if not data:
            raise BadRequest(description='JsonDecodingError')
        photo = data.get('photo')
        if not photo:
            raise BadRequest(description='MissingPhotoParameter')
        updatePhoto(id, photo)
        return '', 204