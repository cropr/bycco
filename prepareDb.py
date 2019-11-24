
import bycco 

from bycco.models import PageModel
from bycco import db

db.drop_collection('page')

PageModel.create_page({
    'metatitle': 'Home Page',
    'slug': 'home',
    'languages': ['en', 'nl', 'fr', 'de'],
    'template': 'landingspage.html',
    'owner': 'ikke',
    'title': {
        'nl': 'Home',
        'fr': 'Accueil',
        'en': 'Home',
        'de': 'Startseite',
    },
    'content': {
        'nl': 'Het Belgisch jeugdkampioenschap Schaken 2020',
        'fr': 'Le championnat de Belgiue de la jeunesse 2020',
        'en': 'The Belgian Youth Chess Championship 2020',
        'de': 'Die belgischer Jugend-Meisterschaften Schah 2020',
    }
})