from django.conf.urls import url

from . import views

urlpatterns = [
    # GET - returns a JSON formatted command states
    # POST - nothing
    url(r'^$', views.index, name='index'),
    # GET - nothing
    # POST - post a command
    url(r'^execute/$', views.execute, name='execute'),
    # GET - nothing
    # POST - post a response
    url(r'^response/$', views.response, name='response'),
    # GET - nothing
    # POST - post a response
    url(r'^runs/current/$', views.current_run, name='current_run'),
    # GET - nothing
    # POST - post a response
    url(r'^runs/currentindex/$', views.current_run_index, name='current_run_index'),
]
