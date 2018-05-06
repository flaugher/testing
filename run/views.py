from pdb import set_trace as debug
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

def index(request):
    """docstring for index"""
    return HttpResponse("Hello, world!")

def change_locale(request):
    """docstring for locale"""
    locale = request.POST.get('locale', '')
    request.session['locale'] = locale
    return HttpResponse("Ran change_locale")

def get_view(request, *args, **kwargs):
    """
    GET request
    """
    context = {}
    return render(request, 'run/get.html', context)

def posargs_view(request, uid, uname, *args, **kwargs):
    """
    POST request with positional args
    """
    context = {'uid': uid, 'uname': uname}
    return render(request, 'run/user.html', context)

def kwargs_view(request, *args, **kwargs):
    """
    POST request with keyword args
    """
    uid = kwargs['uid']
    uname = kwargs['uname']
    context = {'uid': uid, 'uname': uname}
    return render(request, 'run/user.html', context)

def post_view(request, *args, **kwargs):
    """
    POST form plus kwargs
    """
    uid = kwargs['uid']
    uname = kwargs['uname']
    data1 = request.POST.get('data1', '')
    data2 = request.POST.get('data2', '')
    context = {'uid': uid, 'uname': uname}
    return render(request, 'run/user.html', context)

def json_view(request, *args, **kwargs):
    """
    POST JSON data plus kwargs
    """
    uid = kwargs['uid']
    uname = kwargs['uname']
    context = {'uid': uid, 'uname': uname}
    return JsonResponse({'status': '200'})
