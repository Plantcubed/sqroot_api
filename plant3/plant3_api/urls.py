#plant3_api URL Configuration

from django.contrib import admin
from django.conf import settings
from django.conf.urls import include, url, patterns
from django.conf.urls.static import static
from django.views import generic as django_generic_views
from django.contrib.auth import views
from users.forms import LoginForm

urlpatterns = [
    url(r'^', include('users.urls')),
    url(r'^login/$', views.login, {'template_name': 'users/login.html', 'authentication_form': LoginForm}),
    url(r'^logout/$', views.logout, {'next_page': '/login'}),
     url(r'^users/', include('users.urls')),
    url(r'^controls/', include('controls.urls')),
    url(r'^actuators/', include('actuators.urls')),
    url(r'^recipes/', include('recipes.urls')),
    url(r'^sensors/', include('sensors.urls')),
    url(r'^direct/', include('direct.urls')),
    url(r'^revisions/', include('revisions.urls')),
]
