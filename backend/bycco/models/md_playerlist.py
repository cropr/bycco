# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

from datetime import datetime
from typing import Dict, Any, List, Optional, Type
from enum import Enum
from pydantic import BaseModel


class Belplayer(BaseModel):
    """
    A player in the Belgian playerlist
    """
    affiliated: Optional[bool] = True
    birthdate: str       # YYYY-MM-DD format
    federation: str
    first_name: str
    gender: str 
    id: str              
    idclub: str
    idfide: str
    last_name: str
    nationality: str
    ratingbel: int

class Fideplayer(BaseModel):
    birthyear: str
    chesstitle: str
    first_name: str
    gender: str
    last_name: str
    nationality: str
    ratingfide: int