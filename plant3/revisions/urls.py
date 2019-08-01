from django.conf.urls import url

from . import views

urlpatterns = [
    # GET - return all the software items in the revision list
    # POST - creates new revison info for a software item
    url(r'^$', views.revision, name='revision'),
    # GET - return all the software items in the revision list
    # POST - creates new revison info for a software item
    url(r'^(?P<revision_id>[0-9]+)/$', views.revisionitem, name='revisionitem'),
]