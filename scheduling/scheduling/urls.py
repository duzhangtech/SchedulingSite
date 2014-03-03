from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^', include('userprofile.urls')),
	(r'^jasmineTest/$', include('django_jasmine.urls')),
	(r'^loggedin/', include('meetings.urls', namespace='meetings')),
	# DO I NEED TO CHANGE THIS???
	url(r'^database/admin/', include(admin.site.urls)),
	url(r'^$',  'scheduling.views.index'),
	url(r'^ready/$',  'scheduling.views.ready'),
	url(r'^auth/$',  'scheduling.views.auth_view'),
	url(r'^logout/$', 'scheduling.views.logout'),
	url(r'^loggedin/$', 'scheduling.views.loggedin', name='loggedin'),
	url(r'^invalid/$', 'scheduling.views.invalid_login'),
	# registration   
	url(r'^register/$', 'scheduling.views.register_user'),
	url(r'^register_success/$', 'scheduling.views.register_success'),
)