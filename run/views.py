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

def user_posargs(request, uid, uname, *args, **kwargs):
    """
    Positional args
    """
    context = {'uid': uid, 'uname': uname}
    return render(request, 'run/user.html', context)

def user_kwargs(request, *args, **kwargs):
    """
    Keyword args
    """
    print("Running user_kwargs")
    uid = kwargs['uid']
    uname = kwargs['uname']
    context = {'uid': uid, 'uname': uname}
    return render(request, 'run/user.html', context)

def user_post(request, *args, **kwargs):
    """
    POST plus kwargs
    """
    print("Running user_post")
    uid = kwargs['uid']
    uname = kwargs['uname']
    data1 = request.POST.get('data1', '')
    data2 = request.POST.get('data2', '')
    context = {'uid': uid, 'uname': uname}
    print(uid, uname, data1, data2)
    return render(request, 'run/user.html', context)

def json_view(request, *args, **kwargs):
    """
    JSON plus kwargs
    """
    uid = kwargs['uid']
    uname = kwargs['uname']
    #print("JSON data: " + str(request.body))
    context = {'uid': uid, 'uname': uname}
    return JsonResponse({'status': '200'})
