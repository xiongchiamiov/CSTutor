''' URL to View Regular Expression mappings '''
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
	# this is for admin, don't touch
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	(r'^admin/(.*)', admin.site.root),
	
   # these are things that are not page specific, and therefore should be
   # handled here directly
	(r'^submit_join_course_request', 'courses.views.join_course_request'),
	(r'^login/?$', 'users.views.show_login'),
	(r'^login/register-new-account/?$', 'users.views.show_register_new_user'),
	(r'^logout/?', 'users.views.show_logout'),
	(r'^/?$', 'home.views.index'),
	(r'^profile', 'users.views.show_profile'),
	(r'^stats', 'stats.views.display_all_stats'),
	(r'^create-course', 'courses.views.create_course'),
	(r'^join-course', 'courses.views.join_course_form'),

   # courses should be handled by course urls
	(r'^course/(?P<course_slug>[\w-]+)/', include('courses.urls')),
)
