''' 
	URL to View Regular Expression mappings 
	@author Jon Inloes
'''
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

#if the original url was "/coursename/pagename/"
#the expression here would be "pagename/"
#if it were just "/coursename/" then it would be "" (an empty string)

urlpatterns = patterns('courses.views',
	(r'roster/addPendingRequests/$', 'manage_pending_requests'),
	(r'roster/updateRoster/$', 'update_roster'),
	(r'roster/adduser/$', 'add_user'),
	(r'roster/adduser/cancel', 'cancel_add'),
	(r'roster/$', 'show_roster'),
	(r'(?P<pid>[\w-]+)/', include('pages.urls')),
	(r'', 'show_course'),
)

