''' URL to View Regular Expression mappings '''
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
	(r'', 'pages.views.show_page'),
)
