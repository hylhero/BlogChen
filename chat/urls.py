from django.conf.urls import patterns, url
from chat import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^djWebSocket/$', views.djWebSocket, name='djWebSocket'),
    url(r'^update/$', views.update, name='update'),
)
