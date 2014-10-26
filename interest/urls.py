# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from interest import views

urlpatterns = patterns(
    '',
    url(r'^movie/$', views.movieIndex, name='movie'),
)
