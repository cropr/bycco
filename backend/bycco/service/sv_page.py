# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging

import json
from flask import render_template, abort
from bycco import app
from bycco.models import PageModel

log = logging.getLogger('bycco')

def renderPage(slug: str, lang: str):
    """
    renders a page 
    """
    page = PageModel.find_by_slug(slug, lang)
    if not page:
        log.info('could not find page')
        abort(404)
    slugtemplates = page.getSlugTemplates()
    stjson = json.dumps(slugtemplates)
    return render_template(page.template, configstub= f"""
        window.config.locale = '{lang}';
        window.config.slug = '{slug}';
        window.config.slugtemplates = JSON.parse('{stjson}');
      """)

def getPageContent(slug: str, lang: str):
    """
    get the content of a page 
    """
    # log.info(f'getting page {slug} {lang}')
    page = PageModel.find_by_slug_locale(slug, lang)
    return page

def getPages():
    """
    get all pages
    """
    log.info('get pages')
    pages = PageModel.find_pages()
    return page