#    Copyright 2019 Chessdevil Consulting

from typing import Any, Optional
from datetime import datetime, timezone
from dateutil import parser
import pytz

def iso2date(d: Any) -> Optional[datetime]:
    """
    parse an input paramater as a datetime
    input can either be an str (in isoformat), a datetime or None
    str without timezone are expetecd to be utc
    raises ValueError in case of failure
    """
    if isinstance(d, str):
        return parser.isoparse(d).replace(tzinfo=timezone.utc)
    if isinstance(d, datetime):
        return d
    if not d:
        return None
    raise ValueError