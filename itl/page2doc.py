
# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

from flask import Flask
app = Flask(__name__)

import bycco

# load configuration 
app.config.from_object('bycco.settings')
app.config.from_pyfile('../local_settings.py', silent=True)

# set logging config
import logging, logging.config
logging.config.dictConfig(app.config['LOG_CONFIG'])
log = logging.getLogger('bycco')
log.info(f'Starting bycco')

# set up db
from bycco.models import setup_db_connection
db = setup_db_connection(app.config['MONGODB'])

# now import the data 

from datetime import datetime
from bycco.models.md_page import PageModel
from bycco.models.md_document import DocumentModel

def readPages():
    cursor = PageModel.coll().find()
    for p in cursor:
        ct = p['creationtime']
        if isinstance(ct, str):
            ct = datetime.fromisoformat(ct)
        doc = {
            'creationtime': ct,
            'doctype': 'page',
            'i18n_fields': p['i18n_fieldset'],
            'languages': p['languages'],
            'modificationtime': p['modificationtime'],
            'name': p['name'],
            'owner': 'me',
            'slug': p['slug'],
        }
        DocumentModel.create_doc(doc)

if __name__ == '__main__':
    readPages()
    print('done')

