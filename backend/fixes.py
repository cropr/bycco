
import bycco 

from bycco.models import SubscriptionModel
from bycco import db


def fix_remarks():
    cursor = SubscriptionModel.coll().find({}, {"remarks": 1})
    for s in cursor:
        if s.get('remarks', None) is None:
            SubscriptionModel.coll().update_one({'_id': s['_id']} , {
                '$set': {'remarks': ''}
            })

def fix_ints_subsubscription():
    cursor = SubscriptionModel.coll().find({}, {
        "rating": 1,
        "ratingbel": 1,
        "ratingfide": 1,
        "payamount": 1,
    })
    for s in cursor:
        if s.get('remarks', None) is None:
            SubscriptionModel.coll().update_one({'_id': s['_id']} , { '$set': {
                'rating': int(s.get('rating', 0)),
                'ratingbel': int(s.get('ratingbel', 0)),
                'ratingfide': int(s.get('ratingfide', 0)),
                'payamount': int(s.get('payamount', 0)),
            }})
    
if __name__ == '__main__':
    # fix_remarks()
    fix_ints_subsubscription()