# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

from datetime import datetime
from typing import Dict, Any, List, Optional, Type
from enum import Enum
from pydantic import BaseModel
from .md_subscription import Gender


class Player(BaseModel):
    """
    submodel of SwarTrn
    """
    birthdate: str
    chesstitle: str
    clubname: str
    federation: str
    fiderating: int
    first_name: str
    gender: Gender
    idbel: str
    idclub: str
    idfide: str
    last_name: str
    nationality: str
    ratingbel: int
    rating: int

class RoundPublication(str, Enum):
    Active = 'ACT'
    Outdated = 'OUT'
    Unpublished = 'UNP'

class SwarJson(BaseModel):
    """
    submodel of SwarTrn, containing the json file from swar
    and the processed  
    """
    id: str
    jsontext: str
    pairings: Dict[int, str]
    standings: Dict[int, str]
    status: RoundPublication
    uploaddate:  datetime

class SwarTrn(BaseModel):
    """
    as written to the database
    """
    name: str
    players: List[Player]
    rounds: int
    shortname: str
    swarjsons: Dict[int, SwarJson]
    _id: str 
    _version: int
    _documenttype: str
    _creationtime: datetime
    _modificationtime: datetime

class SwarTrnOut(BaseModel):
    name: str
    id: str 
    rounds: int
    shortname: str
    swarname: str

class SwarTrnList(BaseModel):
    trns: List[SwarTrnOut]

class SwarTrnIn(BaseModel):
    name: str
    shortname: str
    rounds: int

class SwarJsonIn(BaseModel):
    idswar: str
    jsontext: str
    swarname: str
    round: int