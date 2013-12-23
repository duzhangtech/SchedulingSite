from django.conf.urls import patterns, url
from meetings import views

urlpatterns = patterns('',
    url(r'^createMtn/$', views.createMtn, name='createMtn'),
    url(r'^create/$', views.create, name='create'),
    # url(r'^meeting_creation_success/$', views.meeting_creation_success, name='meeting_creation_success'),
    url(r'^organized/$', views.organized, name='organized'),
    url(r'^invited/$', views.invited, name='invited'),
	)