from bycco import app
from flask import redirect, url_for
from .service import renderPage

@app.route('/')
def index():
    return redirect('/page/home/en')

@app.route('/page/<slug>/<lang>')
def page(slug, lang):
    return renderPage(slug, lang, 'page')
