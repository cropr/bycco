# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

from typing import Optional, Any
from datetime import datetime, timezone
from dateutil import parser

def iso2date(d: Any) -> Optional[datetime]:
    """
    parse an input paramater as a datetime
    input can either be an str (in isoformat), a datetime instance or None
    str without timezone are expected to be utc
    raises ValueError in case of failure
    """
    if isinstance(d, str):
        return parser.isoparse(d).replace(tzinfo=timezone.utc)
    if isinstance(d, datetime):
        return d
    if not d:
        return None
    raise ValueError

def date2datetime(d, f):
    """
    converts field f of input mongo document d from date to datetime
    as mongo does not supports dates
    """
    if f in d and isinstance(d[f], date):
        t = datetime.min.time()
        d[f] = datetime.combine(d[f], t)       