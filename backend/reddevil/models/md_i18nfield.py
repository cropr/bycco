# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

# all models in the service level exposed to the API
# we are using pydantic as tool

from pydantic import BaseModel
from typing import Optional
    
class I18nField(BaseModel):
    """
    a subobject: contains a localised version of a field
    """
    id: str             # the id of the object the field belong to
    name: str
    value: str