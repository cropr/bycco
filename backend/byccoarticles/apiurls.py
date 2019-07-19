# original Copyright Ruben Decrop
# modifications by Chessdevil Consulting BV

from django.urls import path, re_path
from byccoarticles import apiviews

urlpatterns = [
    path('articles', apiviews.article_all),
    path('articles/<int:id>', apiviews.article_one),
]
