from django.conf.urls import url

from . import views

urlpatterns = [
    # localhost:8000/run
    url(r'^$', views.index, name='index'),
    # localhost:8000/run/locale
    url(r'^locale/$', views.change_locale, name='locale'),
    # localhost:8000/run/user/1/foo
    url(r'^user/(\d+)/(\w+)/$',
        views.user_pos,
        name='user-pos'),
    url(r'^user/(?P<uid>\d+)/(?P<uname>\w+)/$',
        views.user_kw,
        name='user-kw'),
]

