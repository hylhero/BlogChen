#!/usr/bin/env python
#-*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url
import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cblog.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ueditor/',include('DjangoUeditor.urls')),
    url(r'^mcaptcha/', include('mcaptcha.urls', namespace='mcaptcha')),
    url(r'^$', 'blog.views.home',name='home'),
    url(r'^blog/',include('blog.urls',namespace='blog')),
    url(r'^about/$', 'blog.views.about',name='about'),
    url(r'feedback/$', 'blog.views.feedback', name='feedback'),
    url(r'chat/', include('chat.urls', namespace='chat')),
    url(r'photo/', include('photo.urls', namespace='photo')),
    url(r'interest/', include('interest.urls', namespace='interest')),

)
urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}
        ),
)