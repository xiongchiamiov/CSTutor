from django.conf.urls.defaults import *
from django.conf import settings

from courses.models import Course

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = []

if settings.DEBUG:
		import os
		media_dir = os.path.join(os.path.dirname(__file__), 'static/')

		urlpatterns += patterns('',
				(r'^media/(.*)$', 'django.views.static.serve', {'document_root': media_dir}),
		)

urlpatterns += patterns('',
	(r'^admin/(.*)', admin.site.root),
	
	(r'^/?$', 'home.views.index'),
	(r'^profile', 'users.views.show_profile'),
	(r'^create-course', 'courses.views.create_course'),
	(r'^join-course', 'courses.views.join_course'),
	(r'^create-lesson', 'page.lesson.views.create_lesson'),
	(r'^create-quiz', 'page.quiz.views.create_quiz'),
	(r'^(?P<course_slug>[\w-]+)/', include('courses.urls'), {'courses': Course.objects.all()}),


	# Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
	# to INSTALLED_APPS to enable admin documentation:
	# (r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
