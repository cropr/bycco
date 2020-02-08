# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging

import json
from datetime import datetime
from flask import render_template, abort
from werkzeug.exceptions import NotFound, BadRequest
from slugify import slugify
from typing import List, Optional, Union
from bycco import app
from bycco.models import DocumentModel, BasicDocument, I18nView
from bycco.service import request2account
from bycco.util.dates import iso2date

log = logging.getLogger('bycco')

def createDoc(docdict: dict) -> str:
    """
    add a document
    """
    name = docdict.get('name', None)
    if not name:
        raise BadRequest(description='MissingDocParameter')
    docdict['owner'] = docdict.get('owner', 'webmaster')
    if 'slug' not in docdict:
        docdict['slug'] = slugify(name)
    return DocumentModel.create_doc(docdict).id

def deleteDoc(id: str) -> None:
    DocumentModel.remove_doc(id)

def getDoc(id: str) -> DocumentModel:
    """
    get the document 
    """
    return DocumentModel.get_byid(id)

def getDocBySlug(slug: str) -> DocumentModel:
    """
    get the docuemnt by slug 
    """
    return DocumentModel.find_byslug(slug)

def getDocs(options: dict = {}) -> List[BasicDocument]:
    """
    get all docs
    """
    return DocumentModel.find(options)

def getLocalizedDoc(slug: str, lang: str) -> I18nView:
    """
    get the localized content of a document
    """
    return DocumentModel.find_localized(slug, lang)

def renderDoc(slug: str, lang: str):
    """
    renders a document
    """
    try:
        doc = DocumentModel.find_byslug(slug)
        return render_template('document.html', configstub= f"""
            window.config.locale = '{lang}';
            window.config.slug = '{slug}';
        """)
    except NotFound:
        abort(404)

def updateDoc(id: str, updatedict: dict) -> DocumentModel:
    """
    update a document
    """
    # remove readonly fields
    updatedict.pop('id', None)
    updatedict.pop('_id', None)
    updatedict.pop('creationtime', None)
    # import dates as isoformat string
    try:
        updatedict['publishedtime'] = iso2date(updatedict['publishedtime'])
    except ValueError:
        log.exception('invalid publishedtime')
        raise BadRequest(description='InvalidPublishedtime')
    try:
        updatedict['expirytime'] = iso2date(updatedict['expirytime'])
    except ValueError:
        log.exception('invalid expirytime')
        raise BadRequest(description='InvalidExpirytime')
    updatedict['modificationtime'] = datetime.utcnow()
    return DocumentModel.update_doc(id, updatedict)
