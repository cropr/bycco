import asyncio

from datetime import date, datetime, timedelta, timezone
from bycco import settings
from bycco.crud import get_db

from bycco.service.sv_subscription import (
    addSubscription,
    confirmSubscription,
    deleteSubscription,
    getSubscription,
    getSubscriptions,
    updateSubscription,
    checkId,
)
from bycco.models.md_subscription import (
    SubscriptionIn,
    SubscriptionCategory,
    SubscriptionList,
    SubscriptionDetailedOut,
    SubscriptionOut,
    SubscriptionOptional,
)


async def main():

    # drop database
    print('dropping database')
    db = get_db()
    cl = db.client
    await cl.drop_database('bycco')

    r = await checkId('45608')
    print('checkid', r)
    # add a subscription
    id1 = await addSubscription(SubscriptionIn(
        locale='nl',
        category=SubscriptionCategory.B8,
        idbel='45608',
    ))
    r = await checkId('45608')
    print('checkid', r)
    id2 = await addSubscription(SubscriptionIn(
        locale='nl',
        category=SubscriptionCategory.G12,
        idbel='28436',
    ))
    # s = await getSubscription(id1)
    # ss = await getSubscriptions()
    ss = await updateSubscription(id1, SubscriptionOptional(
        emailplayer='ruben@decrop.net'
    ))
    ss = await confirmSubscription(id1)
    r = await checkId('45608')
    print('checkid', r)
    

if __name__ == '__main__':
    asyncio.run(main())
