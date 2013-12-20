from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$',  'scheduling.views.index'),
	url(r'^auth/$',  'scheduling.views.auth_view'),
	url(r'^logout/$', 'scheduling.views.logout'),
	url(r'^loggedin/$', 'scheduling.views.loggedin'),
	url(r'^invalid/$', 'scheduling.views.invalid_login'),
	# registration   
	url(r'^register/$', 'scheduling.views.register_user'),
	url(r'^register_success/$', 'scheduling.views.register_success'),
)
