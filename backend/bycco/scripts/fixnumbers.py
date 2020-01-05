# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

from bycco.models import dbconfig, SubscriptionModel

def fixnumbers():
    coll = dbconfig['db'][SubscriptionModel._collection]
    fields = {
        "subscriptionnumber": 1,
        "invoicenumber": 1,
    }
    for s in coll.find({}, fields):
        if s.get('subscriptionnumber'):
            coll.update_one({'_id': s['_id']}, {'$set': {
                'subscriptionnumber': int(s['subscriptionnumber'])
            }})
        if s.get('invoicenumber'):
            coll.update_one({'_id': s['_id']}, {'$set': {
                'invoicenumber': int(s['invoicenumber'])
            }})

if __name__ == '__main__':
    fixnumbers()
    print('numbers fixed')