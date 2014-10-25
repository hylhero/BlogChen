#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.conf.urls import patterns, url

from blog import views
from blog.feed import LatestBlogFeed


urlpatterns = patterns(
    '',
    url(r'^$', views.BlogIndex.as_view(), name='index'),
    url(r'^detail/(?P<blog_id>\d+)/$', views.BlogDetail.as_view(), name='detail'),
    url(r'^cate/(?P<cate_id>\d+)/$', views.BlogCate.as_view(), name='catelist'),
    url(r'^tag/(?P<tag_id>\d+)/$', views.BlogTag.as_view(), name='taglist'),
    url(r'^comment/', views.comment, name='comment'),
    url(r'^rss/$', LatestBlogFeed()),
)
