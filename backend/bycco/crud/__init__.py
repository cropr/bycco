# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2020

from motor.motor_asyncio import AsyncIOMotorClient
from .. import settings

def date2datetime(d, f):
    """
    converts field f of input mongo document d from date to datetime
    as mongo does not supports dates
    """
    if f in d and isinstance(d[f], date):
        t = datetime.min.time()
        d[f] = datetime.combine(d[f], t)  

def get_db():
    """
    a singleton
    """
    if not hasattr(get_db, 'database'):
        client = AsyncIOMotorClient(settings.MONGO_URL)
        setattr(get_db,'database', client[settings.MONGO_DB])
    return get_db.database