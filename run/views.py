from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    """docstring for index"""
    return HttpResponse("Hello, world!")

def change_locale(request):
    """docstring for locale"""
    locale = request.POST.get('locale', '')
    request.session['locale'] = locale
    return HttpResponse("Ran change_locale")
