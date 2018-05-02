from pdb import set_trace as debug
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

def user_pos(request, uid, uname, *args, **kwargs):
    """
    Positional args
    """
    context = {'uid': uid, 'uname': uname}
    return render(request, 'run/user.html', context)

def user_kw(request, *args, **kwargs):
    """
    Keyword args
    """
    uid = kwargs['uid']
    uname = kwargs['uname']
    context = {'uid': uid, 'uname': uname}
    return render(request, 'run/user.html', context)
