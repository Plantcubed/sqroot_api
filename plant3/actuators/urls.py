from django.conf.urls import url

from . import views

urlpatterns = [
    # GET - returns a JSON formatted list of actuators
    # POST - adds a new actuator item
    url(r'^$', views.index, name='index'),
    # the API's in this group do a bit more than usual. During the GET & POST, the currnet
    # time is compared to the override end time, if its past, the override setting
    # will be cleared.
    # GET - returns a JSON formatted of the current state, override, override times
    # of the actuator
    # POST - sets the current state, override of the actuator
    url(r'^(?P<actuators_id>[0-9]+)/value/$', views.value, name='value'),
    # GET - returns a JSON formatted of a particular actuator
    # POST - overwrites an existing actuator entry
    url(r'^(?P<actuators_id>[0-9]+)/$', views.item, name='item'),
    # GET - returns a JSON formatted of a particular actuator
    # POST - overwrites an existing actuator entry
    url(r'^(?P<actuators_id>[0-9]+)/error/$', views.error, name='error'),
    # GET - returns a JSON formatted of a particular actuator
    # POST - overwrites an existing actuator entry
    url(r'^(?P<actuators_id>[0-9]+)/dose_to/$', views.dose_to, name='dose_to'),
]
