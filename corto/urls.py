"""corto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^dashboard/$', views.dashboard),
    url(r'^dashboard/analyse/(?P<url_id>[0-9]+)$', views.analyse),
    url(r'^dashboard/analyse/', views.analyse_red),
    url(r'^logout/', views.logout),
    url(r'^(?P<short_url>[0-9A-Za-z]+)$', views.redirecting),
    url(r'^sign_in/', views.sign_in),
    url(r'^sign_up/', views.sign_up),
    url(r'^forgot/', views.forgot)
    ]
