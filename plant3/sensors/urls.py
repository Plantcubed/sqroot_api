from django.conf.urls import url

from . import views

urlpatterns = [
    # GET - returns a JSON formatted list of sensors
    # POST - adds a new sensor item
    url(r'^$', views.index, name='index'),
    # GET - returns a JSON formatted of the current reading of the sensor
    # POST - sets the current value of the sensor
    url(r'^(?P<sensor_id>[0-9]+)/value/$', views.value, name='value'),
    # GET - returns a JSON formatted of a particular sensor
    # POST - overwrites an existing sensor entry
    url(r'^(?P<sensor_id>[0-9]+)/$', views.item, name='item'),
]
