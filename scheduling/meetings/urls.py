from django.conf.urls import patterns, url
from meetings import views

urlpatterns = patterns('',
    url(r'^createMtn/$', views.createMtn, name='createMtn'),
    url(r'^create/$', views.create, name='create'),
    # url(r'^meeting_creation_success/$', views.meeting_creation_success, name='meeting_creation_success'),
	url(r'^organized/(?P<meeting_id>\w{6})/$', views.MtnOrganized, name="MtnOrganized"),
	url(r'^invited/(?P<meeting_id>\w{6})/$', views.MtnInvited, name="MtnInvited"),
	)