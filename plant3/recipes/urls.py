from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^hidden/$', views.indexhidden, name='indexhidden'),
    url(r'^clear/$', views.clear, name='clear'),
    url(r'^(?P<recipes_id>[0-9]+)/$', views.get, name='get'),
    url(r'^runs/$', views.runs, name='runs'),
    url(r'^runs/stop/$', views.runstop, name='runstop'),
    url(r'^control/$', views.control, name='control'),
]
