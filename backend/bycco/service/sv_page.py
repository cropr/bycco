# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging

import json
from datetime import datetime
from flask import render_template, abort
from werkzeug.exceptions import NotFound
from typing import List, Optional, Union
from bycco import app
from bycco.models import PageModel, BasicPage, LocalizedPage
from bycco.service import request2account

log = logging.getLogger('bycco')

def renderPage(slug: str, lang: str, template: str = 'page'):
    """
    renders a page 
    """
    try:
        page = PageModel.find_by_slug(slug)
    except NotFound:
        abort(404)
    assert page.template is not None
    slugtemplates = page.get_slug_templates()
    stjson = json.dumps(slugtemplates)
    return render_template(f'{template}.html', configstub= f"""
        window.config.locale = '{lang}';
        window.config.slug = '{slug}';
        window.config.slugtemplates = JSON.parse('{stjson}');
      """)

def getPage(id: str) -> PageModel:
    """
    get the page by id 
    """
    log.info(f'getting page by id {id}')
    page = PageModel.find_by_id(id)
    return page

def updatePage(id: str, pagedict: dict) -> PageModel:
    """
    update a page  
    """
    log.info(f'updating page by id {id}')
    # clean up
    pagedict.pop('id', None)
    pagedict.pop('_id', None)
    pagedict['modificationtime'] = datetime.utcnow()
    page = PageModel.update_page(id, pagedict)
    return page


def getPageBySlug(slug: str) -> PageModel:
    """
    get the page by slug 
    """
    log.info(f'getting page by slug {slug}')
    page = PageModel.find_by_slug(slug)
    return page

def getPageBySlugLocale(slug: str, lang: str) -> LocalizedPage:
    """
    get the content of a page 
    """
    log.info(f'getting page  by slug {slug}, locale {lang}')    
    page = PageModel.find_i18n_by_slug(slug, lang)
    return page

def getPages() -> List[BasicPage]:
    """
    get all pages
    """
    # request2account().check_right('ViewPages')
    pages = PageModel.find_pages()
    return pages