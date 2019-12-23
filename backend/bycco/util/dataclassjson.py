#    Copyright 2019 Chessdevil Consulting

import logging, logging.config
log = logging.getLogger('bycco')

import json
import datetime
import dataclasses
from bson import ObjectId

class DataclassEncoder(json.JSONEncoder):
    """
    JSON encoder which handles dataclasses, datetime and ObjectId types
    removes all _hidden  attributes from dataclasses 
    """
    
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, ObjectId):
            return str(obj)
        elif dataclasses.is_dataclass(obj):
            objd = dataclasses.asdict(obj)
            if hasattr(obj, '_hidden'):
                for h in obj._hidden:
                    objd.pop(h, None)
            return objd
        return super(DataclassEncoder, self).default(obj)

