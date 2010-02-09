''' 
	This file describes the various views of user statistics

	@author Andrew J. Musselman
'''

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from courses.models import Course
from stats.models import Stat
#from stats.stats import *
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.template.defaultfilters import slugify 
from home.views import master_rtr

# Create your views here.
def display_course_stats(request, course_slug):
	#return render_to_response('stats/show_couse_stats.html', 
	pass
	#STUB... FIXME

def display_all_stats(request):
	'''Displays stats for ALL users in all courses''' 
	#FIXME Made changes because master_rtr must be used
	data = {}
	return master_rtr(request, 'stats/show_all_stats.html', data)
