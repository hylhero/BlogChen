#!/usr/bin/env python
#-*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url
import settings
from django.contrib import admin
from blog.sitemap import BlogSitemap
admin.autodiscover()
from blog.views import Home, About

sitemaps = {
    'blog': BlogSitemap
}

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'cblog.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ueditor/', include('DjangoUeditor.urls')),
    url(r'^mcaptcha/', include('mcaptcha.urls', namespace='mcaptcha')),
    url(r'^$', Home.as_view(), name='home'),
    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^about/$', About.as_view(), name='about'),
    url(r'feedback/$', 'blog.views.feedback', name='feedback'),
    url(r'chat/', include('chat.urls', namespace='chat')),
    url(r'photo/', include('photo.urls', namespace='photo')),
    url(r'interest/', include('interest.urls', namespace='interest')),

    url(r'^sitemap\.xml/$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': {'blog':BlogSitemap,}}),

)
from django.conf import settings

if settings.DEBUG is False:
    urlpatterns += patterns('',
        #url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
         #   {'document_root': settings.MEDIA_ROOT}
       # ),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
   )