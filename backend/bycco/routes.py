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
def mgmt(path=''):
    return render_template('mgmt.html', configstub="")    

@app.route('/subscription')
@app.route('/subscription/<path:path>')
def subscription(path=''):
    return render_template('subscription.html', configstub="")    


@app.route('/vertaal')
def vertaal(path=''):
    return render_template('testmail.html', _={
        "Vertaal": "Translate",
        "Tekst <b>met</b> {a} vertaald": "Text <b>with</b> {a} translated"
    }).format(**{'a':'aa'})    
