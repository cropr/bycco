# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

from flask_restful import Resource
from bycco.service import getSubscriptions, addSubscription, getSubscription

class SubscriptionsResource(Resource):
    def get(self) -> dict:
        return {'subscriptions': getSubscriptions()}
    def post(self, subscription: dict) -> dict:
        return {'subscription': addSubscription(subscription)}

class SubscriptionResource(Resource):
    def get(self, id:str) -> dict:
        return {'subscription': getSubscription(id)}