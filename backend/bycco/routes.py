from bycco import app
from flask import redirect, url_for, render_template
from .service import renderPage

@app.route('/')
def index():
    return redirect('/page/home/nl')

@app.route('/page/<slug>/<lang>')
def page(slug, lang):
    return renderPage(slug, lang, 'page')

@app.route('/mgmt')
@app.route('/mgmt/<path:path>')
def mgmt(slug, path=''):
    return render_template('mgmt.html', configstub="")    

@app.route('/subscription')
@app.route('/subscription/<path:path>')
def subscription(slug, path=''):
    return render_template('subscription.html', configstub="")    
