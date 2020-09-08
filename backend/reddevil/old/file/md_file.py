# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

# all models in the service level exposed to the API
# we are using pydantic as tool

import logging

from datetime import datetime, date, timezone
from typing import Dict, Any, List, Optional, Type
from pydantic import BaseModel

class FileIn(BaseModel):
    """
    contains the minimal fields (doctype and name) to create a new page
    """
    content: bytes           # base64 encoded content of file
    name: str

class FileOut(BaseModel):
    """
    A readonly view used for listing files
    """
    archived: bool = False
    created_by: str = 'webmaster'
    created_ts: datetime
    filelength: int
    id: str
    locale: str = ''
    mimetype: str
    modified_ts: datetime
    name: str
    topic: str = 'Unknown'    # report BM, report GA, ....
    topic_ts: date = None
    url: str

class FileListOut(BaseModel):
    files: List[FileOut]


class FileDetailedIn(BaseModel):
    """
    An update to a file: all fields are optional
    """
    archived: Optional[bool] = None
    created_by: Optional[str] = None
    content: Optional[bytes] = None
    locale: Optional[str] = None
    name: Optional[str] = None
    topic: Optional[str] = None
    topic_ts: Optional[date] = None

class FileSingleOut(BaseModel):
    file: FileOut
