# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

from flask import Flask
app = Flask(__name__)


# enable CORS
from flask_cors import CORS
CORS(app)

# load configuration
app.config.from_object('bycco.settings')
app.config.from_object('local_settings')

# set logging config
import logging, logging.config
logging.config.dictConfig(app.config['LOG_CONFIG'])
log = logging.getLogger('bycco')
log.info(f'Starting bycco')

# set up db
from bycco.models import setup_db_connection
db = setup_db_connection(app.config['MONGODB'])

# load api definitions
import bycco.api
import bycco.routes

