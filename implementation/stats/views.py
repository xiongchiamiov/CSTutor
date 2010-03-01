''' 
	This file describes the various views of user statistics

	@author Andrew J. Musselman
'''

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from courses.models import Course
from stats.models import Stat
from stats.stat import *
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.template.defaultfilters import slugify 
from django.contrib.auth.decorators import login_required
from home.views import master_rtr

# Create your views here.
@login_required
def display_course_stats(request, course_slug):
	'''Displays stats for a given course'''
	#Make sure the course is a real course in the DBMS
	try:
		course = Course.objects.get(slug=course_slug)   
	except Course.DoesNotExist:
		raise Http404
						
	#make sure the user has premissions to view stats.
	enrollment = request.user.enrollments.get(course=course)
	if enrollment.stats:
		bestQuizAggregates = getQuizBestAggregates(course)
		bestUserAggregates = getUserBestAggregates(course)
		stat_data = {'course':course,\
		             'bestQuizAggregates':bestQuizAggregates,\
					 'bestUserAggregates':bestUserAggregates, \
					 'course_slug':course_slug} 

		return master_rtr(request, 'stats/show_course_stats.html', stat_data)
	else:
		#Or else, you don't have premeission to view stats
		return master_rtr(request, 'stats/invalid__user_permissions.html', \
				{'course': course, \
				 'course_slug': course_slug})



