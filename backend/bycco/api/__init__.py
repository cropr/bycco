# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import reddevil.api.api_page
import reddevil.api.api_account
# import reddevil.file.api_file

import bycco.api.api_subscription
import bycco.api.api_swar

from bycco import app

@app.get('/api')
def api_root():
    return {'hello': 'world'}
