from django.conf.urls import patterns, url
from meetings import views

urlpatterns = patterns('',
    url(r'^createMtn/$', views.create, name='create'),
    url(r'^create/$', views.create, name='create'),
    url(r'^createSuccess/$', views.createSuccess, name='createSuccess'),
    # url(r'^meeting_creation_success/$', views.meeting_creation_success, name='meeting_creation_success'),
	url(r'^organized/(?P<meeting_id>\w{6})/$', views.MtnOrganized, name="MtnOrganized"),
	url(r'^organized/(?P<meeting_id>\w{6})/delete/$', views.delete, name="delete"),
	url(r'^organized/(?P<meeting_id>\w{6})/update/$', views.updateMtn, name="updateMtn"),
	url(r'^organized/(?P<meeting_id>\w{6})/update/update/$', views.update, name="update"),
	url(r'^organized/(?P<meeting_id>\w{6})/addInvitees/$', views.addInvitees, name="addInvitees"),
	url(r'^invited/(?P<meeting_id>\w{6})/respond/$', views.respond, name="respond"),
	url(r'^invited/(?P<meeting_id>\w{6})/responded/$', views.responded, name="responded"),
	url(r'^invited/(?P<meeting_id>\w{6})/responded/respond/$', views.respond, name="respond"),
	url(r'^invited/(?P<meeting_id>\w{6})(?:/(?P<validity>\w{7,11}))?/$', views.MtnInvited, name="MtnInvited"),
	url(r'^ajaxTest/$', views.ajaxTest, name="ajaxTest"),
	)
