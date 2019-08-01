from django.conf.urls import url

from . import views

urlpatterns = [
    # GET - returns a JSON formatted list of actuators
    # POST - adds a new actuator item
    url(r'^$', views.index, name='index'),
    # GET - returns a JSON formatted of the current state of the actuator
    # POST - sets the current state of the actuator
    url(r'^(?P<control_id>[0-9]+)/setpoint/$', views.setpoint, name='setpoint'),
    # GET - returns a JSON formatted of a particular actuator
    # POST - overwrites an existing actuator entry
    url(r'^(?P<control_id>[0-9]+)/$', views.item, name='item'),
    # GET - returns a JSON formatted of a particular actuator
    # POST - overwrites an existing actuator entry
    url(r'^(?P<control_id>[0-9]+)/enabled/$', views.enabled, name='enabled'),
    # GET - returns a JSON formatted of a particular actuator
    # POST - overwrites an existing actuator entry
    url(r'^(?P<control_id>[0-9]+)/error/$', views.error, name='error'),
    # GET - returns a JSON formatted of a particular actuator
    # POST - overwrites an existing actuator entry
    url(r'^(?P<control_id>[0-9]+)/delete/$', views.delete, name='delete'),
]
