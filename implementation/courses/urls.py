''' 
	URL to View Regular Expression mappings 
	@author Jon Inloes
'''
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

#if the original url was "/coursename/pagename/"
#the expression here would be "pagename/"
#if it were just "/coursename/" then it would be "" (an empty string)
	
urlpatterns = patterns('',
   # create a quiz in these pages
	(r'create-quiz', 'pages.quiz.views.create_quiz'),
	(r'create-lesson', 'pages.lesson.views.create_lesson'),

   # redirect to stats
	(r'stats/.*', include ('stats.urls')),
   # redirect to lesson or quiz
	(r'page/(?P<page_slug>[\w-]+)/', include('pages.urls')),
)

urlpatterns += patterns('courses.views',
	# roster requests
	(r'roster/addPendingRequests/$', 'manage_pending_requests'),
	(r'roster/updateRoster/$', 'update_roster'),
	(r'roster/adduser/$', 'add_user'),
	(r'roster/adduser/cancel', 'cancel_add'),
	(r'roster/$', 'show_roster'),
	#redirect to the chat page
	(r'chat/$', 'show_chat'),

	# Catch just the course and render the course index anyway
	(r'^$', 'show_course'),
)
