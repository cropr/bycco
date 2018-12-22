
from django.http import HttpResponse
from django.shortcuts import render

def test_base(request):
    return render(request, 'base.html')

def test_cms(request):
    return render(request, 'test_cms.html')

def test_vue(request):
    return render(request, 'test_vue.html')

def test_vuecms(request):
    return render(request, 'test_vuecms.html')