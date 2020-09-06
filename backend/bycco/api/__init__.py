# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import reddevil.page.api_page
import reddevil.file.api_file

from bycco import app

@app.get('/api')
def api_root():
    return {'hello': 'world'}

