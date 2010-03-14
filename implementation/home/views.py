''' @author James Pearson, Matt Tytel, John Hartquist, Jon Inloes '''

from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from courses.models import Course, Enrollment
from pages.lesson.models import Lesson
from pages.quiz.models import Quiz
from django.core.exceptions import ObjectDoesNotExist
import datetime

def master_rtr(request, template, data = {}):
	if request.user.is_authenticated():
		# Since we're only grabbing the enrollments to get at the courses, 
		# doing select_related() will save us from having to hit database for
		# every course the user is enrolled in
		data['courses'] = \
			[e.course for e in \
			 Enrollment.objects.select_related().filter(user=request.user) \
			 if e.view]
	else:
		if "anonCourses" in request.session:
			data['courses'] = request.session['anonCourses']
		else:
			data['courses'] = []
	
	data['THEME'] = settings.THEME

	return render_to_response(template, data, context_instance=RequestContext(request))

#def index(request):
#	return master_rtr(request, 'index.html')

def show_homepage(request):
	'''
	@author Russell Mezzetta
	This shows the homepage for anonymous and logged in users
	'''
	data={}
	if request.user.is_authenticated():
		#get and format the last login date/time
		lastLogin = request.user.last_login
		data['loginDate'] = "%s/%s/%s" % (lastLogin.month, lastLogin.day, lastLogin.year)
		data['loginTime'] = "%s:%s:%s" % (lastLogin.hour, lastLogin.minute, lastLogin.second)
		
		#check for last course / lesson in session
		if 'lastCourseSlug' in request.session and 'lastPageSlug' in request.session and 'lastPageEdit' in request.session:
			lastCourseSlug = request.session['lastCourseSlug']
			lastPageSlug = request.session['lastPageSlug']
			lastPageEdit = request.session['lastPageEdit']
			try:
				#may not still exist!
				c = Course.objects.get(slug=lastCourseSlug)
				p = c.pages.get(slug=lastPageSlug)
				try:
					p = p.lesson
				except Lesson.DoesNotExist:
					# lastCourseSlug, etc can ONLY exist if at some point
					# this combination of course/page slug was a 
					# real lesson or quiz.  Therefore, due to this fact,
					# DO NOT check if it's a quiz.  The ONLY way that
					# these variables could be set, and p.lesson and 
					# p.quiz were both invalid is if some asshat with 
					# database access dropped the Lesson/Quiz but
					# not the page.  Therefore due to difficulty in code coveraging
					# this path, we're just gonna assume that the damn thing exists
					#try: 
					p = p.quiz
					#except Quiz.DoesNotExist:
					#	print "OH NO! page is neither lesson nor quiz"
					#	data['lastPageNoLongerExists'] = True

				data['lastCourse'] = c
				data['lastPage'] = p
				data['lastPageEdit'] = lastPageEdit
			except ObjectDoesNotExist:
				#course or lesson no longer exists
				data['lastPageNoLongerExists'] = True

		#get the number of courses the user is enrolled in
		enrolled = request.user.enrollments.all()
		pending = []
		for e in enrolled:
			if e.view == False:
				pending.append(e.course)
		if len(pending):
			data['pending'] = pending

		data['numClasses'] = request.user.enrollments.count()
		if data['numClasses'] <= 0:
			data['not_enrolled'] = True
		else:#user enrolled in 1 or more classes
			data['not_enrolled'] = False
	else: #User is anonymous
		if not "anonCourses" in request.session:
			data['not_enrolled'] = True
		else:
			#added this in case someone clobbers request.session
			if request.session['anonCourses'] != None:
				data['numClasses'] = len(request.session['anonCourses'])
	
	return master_rtr(request, 'homepage.html', data)

def show_help(request):
	'''
	Displays the help page
	'''
	return master_rtr(request, 'help/index.html')

def custom_404(request, message=''):
	response = master_rtr(request, '404.html', {'message':message})
	response.status_code = 404
	return response


def custom_403(request, message=''):
	'''
	Generic forbidden page view
	'''
	response = master_rtr(request, '403.html', {'message':message})
	response.status_code = 403
	return response

