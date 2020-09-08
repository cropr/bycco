
# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

from flask import Flask
app = Flask(__name__)

import bycco

# load configuratio 
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

import csv
from bycco.models.md_page import PageModel

with open('itl/pages.csv') as f:
    reader =  csv.DictReader(f)
    for page in reader:
        languages = []
        i18n_fieldset = {}
        for l in ['nl', 'fr', 'en', 'de']:
            if page[l] == '1':
                languages.append(l)
                with open(f'itl/{page["name"]}_{l}.md') as c:
                    i18n_fieldset[l] = {
                      'content': c.read(),
                      'title': page[f"title_{l}"],
                      'intro': "",
                    }
        p = {
            'name': page["name"],
            'owner': 'ruben',
            'slug': page["name"],
            'active': True,
            'i18n_fieldset': i18n_fieldset,
            'languages': languages,
            'template': page['template'],
        }
        success = PageModel.create_page(p)
        if success:
            print(f'page {page["name"]} created')
        else:
            print(f'page {page["name"]} failed')
