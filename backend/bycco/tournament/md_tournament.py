# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2024

from pydantic import BaseModel


class TrnUpload(BaseModel):
    name: str
    jsoncontent: str


class TrnUnofficialResult(BaseModel):
    name: str
    round: int
    boardnr: int
    unofficial_result: str
