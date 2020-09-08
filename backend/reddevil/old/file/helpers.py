# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging
from datetime import datetime, timezone

log = logging.getLogger('reddevil')

def isactive(dd: dict) -> bool:
    """
    checks whether a page is active
    """
    if not dd.get('enabled'):
        return False
    p = dd.get('publishedtime', None)
    e = dd.get('expirytime', None)
    published = p and (p < datetime.now(timezone.utc))
    expired = e and (e < datetime.now(timezone.utc))
    return bool( published and not expired)
