'''
	Functions in this file allow an instructor to create a course, add users to the course, search for user names, and remove users. In addition, there are functions that allow a student to join a course. 
	@author Jon Inloes
'''
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from courses.models import Course
from courses.course import *
from users.models import User
from django.db import IntegrityError
from django.template.defaultfilters import slugify
from home.views import master_rtr
from django.contrib.auth.decorators import login_required


@login_required
def create_course(request):
	'''
	Creates a new course if course name is long enough
	and the coursename is unique.  If not gives an error.
	'''
	if request.method == "POST":
		name = request.POST['coursename'].strip()

		if len(name) < 3:
			return master_rtr(request, 'courses/create_course_length.html')

		try:
			CreateCourse(name, request.user)
		except IntegrityError:
			return master_rtr(request, 'courses/create_course_dup.html')

	return master_rtr(request, 'courses/create_course.html')

@login_required
def show_roster(request, course_slug):
	'''
	Displays the roster
	'''
	course = Course.objects.get(slug=course_slug)

	# It is better to get the enrollment by this method, because in this case
   # the database searches using Primary Keys, which are indexed, instead of 
   # username, which is not indexed. -mgius
	#enrollment = Enrollment.objects.get(user__username__exact=request.user.username, course__slug__exact=course_slug)
	enrollment = request.user.enrollments.get(course=course)
	
	if enrollment.manage:
		enrollments = course.roster.all();

		return master_rtr(request, 'roster/index.html', {'course': course, 'enrollments': enrollments, 'course_slug': course.slug})

	else:
		return master_rtr(request, 'roster/invalid_permissions.html', {'course': course})

def show_course(request, course_slug):
	return master_rtr(request, 'index.html', {'course_slug': course_slug})

def add_user(request, course_slug):
	'''
	Handles the commands given by the add user screen

	@precondition none
	@postcondition The user exists in the database if it is a valid user.
	'''
	course = Course.objects.get(slug=course_slug)
	
	#if the request method was a post determine the command that was given
	if request.method == 'POST':
		
		#if the command was an add try to add the user
		if request.POST['command'] == 'add':
			
			usr = request.POST['username']

			try:
				#if the user exists add it
				user = User.objects.get(username=usr)
				addUser(course, user)

			except User.DoesNotExist:
				#if the user does not exist print error message
				return master_rtr(request, 'adduser/failed.html', {'course_slug':course_slug, 'course': course})
			
			#show the roster screen
			return HttpResponseRedirect("/%s/roster/" % course_slug)
		elif request.POST['command'] == 'search':
			#if the command was a search, search for the user
	
			firstname = request.POST['firstname']
			lastname = request.POST['lastname']

			users = User.objects.filter(first_name = firstname, last_name = lastname)

	
			return master_rtr(request, 'adduser/search.html', {'course_slug': course_slug, 'course':course, 'users':users, 'firstname': firstname, 'lastname': lastname})
	else:
		
		#display the adduser page
		return master_rtr(request,'adduser/index.html', {'course_slug': course_slug, 'course': course, 'url': request.path})

def search_username(request, course_slug, courses):
	'''This function is not called any more'''
	course = Course.objects.get(slug=course_slug)
	
	firstname = request.POST['firstname']
	lastname = request.POST['lastname']
	
	url = request.path
	print url

	users = User.objects.filter(first_name = firstname, last_name = lastname)

	
	return master_rtr(request, 'adduser/search.html', {'course_slug': course_slug, 'course':course, 'users':users, 'firstname': firstname, 'lastname': lastname, 'url': request.path})

def remove_user(request, course_slug):
	'''
	Removes a user from a course's enrollment list
	@precondition The username entered in is valid.
	@postcondition The username is no longer in the roster list. 
	'''
	removeName = request.POST['username']
	course = Course.objects.get(slug=course_slug)

	try:
		user = User.objects.get(username=removeName)
		removeUser(course,user)
	except	User.DoesNotExist:
		pass
	
	
	return HttpResponseRedirect("/%s/roster/" % course_slug)

def cancel_add(request, course_slug, courses):
	'''
	Redirects to the roster screen when viewing the add user page
	'''
	return HttpResponseRedirect("/%s/roster/" % course_slug)

def join_course_form(request):
	'''
		Displays a list of unenrolled courses for a user to request to join.
	'''
	if request.user.is_authenticated():
		enrollmentIds = [e.course.id for e in request.user.enrollments.all()]
		courses = Course.objects.exclude(id__in=enrollmentIds)
	else:
		courses = Course.objects.all()

	return master_rtr(request, 'courses/join_course_form.html', \
			{'join_courses' : courses})

@login_required
def join_course_request(request):
	'''Displays the classes a user can join'''
	courseid = request.GET['courseid']
	course = Course.objects.get(id=courseid)
	user = User.objects.get(username=request.user.username)
	enrollment = addUser(course, user, True)
	if enrollment == None:
		return master_rtr(request, 'courses/join_course_already_enrolled.html', \
				{'course':course, 'user':user})
	else:
		return master_rtr(request, 'courses/join_course_successful.html', \
				{'course':course, 'user':user})
