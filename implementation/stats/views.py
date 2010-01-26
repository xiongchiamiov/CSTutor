from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from models import Stat
from courses.models import Course
#from stats.stats import *
from users.models import User
from django.db import IntegrityError
from django.template.defaultfilters import slugify 

# Create your views here.
def display_couse_stats(request, course_slug):
	#return render_to_response('stats/show_couse_stats.html', 
	pass
	#STUB... FIXME

def display_all_stats(request):
	'''Displays stats for ALL users in all courses'''
	data = {}
	courses = Course.objects.all()
	data['courses'] = courses 

	return render_to_response('stats/show_all_stats.html',data)
	


