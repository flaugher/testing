from django.conf.urls import url

from . import views

urlpatterns = [
    # localhost:8000/run
    url(r'^$', views.index, name='index'),
    # localhost:8000/run/locale
    url(r'^locale/$', views.change_locale, name='locale'),
    # localhost:8000/run/posargs/1/foo
    url(r'^get/$',
        views.get_view,
        name='get-view'),
    url(r'^posargs/(\d+)/(\w+)/$',
        views.posargs_view,
        name='posargs-view'),
    # localhost:8000/run/kwargs/1/foo
    url(r'^kwargs/(?P<uid>\d+)/(?P<uname>\w+)/$',
        views.kwargs_view,
        name='kwargs-view'),
    # localhost:8000/run/post/1/foo
    url(r'^post/(?P<uid>\d+)/(?P<uname>\w+)/$',
        views.post_view,
        name='post-view'),
    # localhost:8000/run/json/1/foo
    url(r'^json/(?P<uid>\d+)/(?P<uname>\w+)/$',
        views.json_view,
        name='json-view'),
]

