from django.conf.urls import url

from . import views

urlpatterns = [
    # localhost:8000/run
    url(r'^$', views.index, name='index'),
    # localhost:8000/run/locale
    url(r'^locale/$', views.change_locale, name='locale'),
    # localhost:8000/run/user/1/foo
    url(r'^user/(\d+)/(\w+)/$',
        views.user_posargs,
        name='user-posargs'),
    url(r'^user/(?P<uid>\d+)/(?P<uname>\w+)/$',
        views.user_kwargs,
        name='user-kwargs'),
    url(r'^userpost/(?P<uid>\d+)/(?P<uname>\w+)/$',
        views.user_post,
        name='user-post'),
    url(r'^json_view/(?P<uid>\d+)/(?P<uname>\w+)/$',
        views.json_view,
        name='json-view'),
    # TODO: change view names to X_view
]

