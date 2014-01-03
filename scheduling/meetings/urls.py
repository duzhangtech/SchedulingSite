from django.conf.urls import patterns, url
from meetings import views

urlpatterns = patterns('',
    url(r'^createMtn/$', views.createMtn, name='createMtn'),
    url(r'^create/$', views.create, name='create'),
    # url(r'^meeting_creation_success/$', views.meeting_creation_success, name='meeting_creation_success'),
	url(r'^organized/(?P<meeting_id>\w{6})/$', views.MtnOrganized, name="MtnOrganized"),
	url(r'^organized/(?P<meeting_id>\w{6})/delete/$', views.delete, name="delete"),
	url(r'^organized/(?P<meeting_id>\w{6})/update/$', views.updateMtn, name="updateMtn"),
	url(r'^organized/(?P<meeting_id>\w{6})/update/update/$', views.update, name="update"),
	url(r'^invited/(?P<meeting_id>\w{6})/$', views.MtnInvited, name="MtnInvited"),
	url(r'^invited/(?P<meeting_id>\w{6})/(\w{9}\/)?respond/$', views.respond, name="respond"),
	url(r'^invited/(?P<meeting_id>\w{6})/responded/$', views.responded, name="responded"),
	)