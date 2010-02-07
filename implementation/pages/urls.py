''' URL to View Regular Expression mappings '''
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
	(r'submitQuiz/', 'pages.quiz.views.submitQuiz'),
	(r'edit/', 'pages.views.edit_page'),
	(r'', 'pages.views.show_page'),
)
