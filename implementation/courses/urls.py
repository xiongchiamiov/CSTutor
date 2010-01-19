from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.conf import settings

urls.pattern(r'^roster/(.*)', (r'^/?$', views.show_roster),)
