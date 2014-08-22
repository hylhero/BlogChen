from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(r'^image/(?P<key>[\w\.]+)/$',views.mcaptcha,name='mcaptcha'),
    url(r'^refresh/$', views.mcaptcha_refresh, name='mcapt_refresh'),
)