from django.conf.urls import url

from . import views

urlpatterns = [
    # localhost:8000/run
    url(r'^$', views.index, name='index'),
    # localhost:8000/run/locale
    url(r'^locale/$', views.change_locale, name='locale'),
    # localhost:8000/run/user/1/foo
    url(r'^user/(\d+)/(\w+)/$',
        views.user,
        {'template': 'run/user.html'},
        name='user'),
]

