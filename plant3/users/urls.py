# log/urls.py
from django.conf.urls import url

from . import views

# We are adding a URL called /home
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^recipe/$', views.recipe, name='recipe'),
    url(r'^images/$', views.images, name='images'),
    url(r'^control/$', views.control, name='control'),
    url(r'^setup/$', views.setup, name='setup'),
    url(r'^about/$', views.about, name='about'),
    url(r'^about/$', views.about, name='about'),
    url(r'^password/change/$', views.userchangepassword, name='userchangepassword'),
    url(r'^password/reset/$', views.userresetpassword, name='userresetpassword'),
    url(r'^user/add/$', views.useradd, name='useradd'),
    url(r'^user/list/$', views.userlist, name='userlist'),
]