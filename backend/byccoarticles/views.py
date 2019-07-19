# Copyright Ruben Decrop

import logging
log = logging.getLogger(__name__)

from django.shortcuts import render
from byccoarticles.models import ByccoArticle

def articlespage(request):
    return render(request, 'byccoarticles/articles.html')
 
def articlepage(request, slug):
    try:
        art = ByccoArticle.objects.get(slug=slug)
    except ByccoArticle.DoesNotExist:
        return render(request, 'byccoarticles/notfound.html')
    return render(request, 'byccoarticles/article.html', {'id': art.id})
