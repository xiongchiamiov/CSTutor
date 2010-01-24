from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('courses.views',
	(r'roster/$', 'show_roster'),
	(r'^(?P<pid>[\w-]+)/', include('page.urls')),
	(r'', 'show_course'),
)
