# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging

import os.path
import json
from bycco import app

_langdir = os.path.join(app.root_path, 'static', 'lang')

def getLanguageFile(lang: str) -> str:
    """
    returns translation file for {lang}
    """
    messages = {}
    with open(os.path.join(_langdir, f'bycco_{lang}.json')) as f:
        messages = f.read()
    return json.loads(messages)