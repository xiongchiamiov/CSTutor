from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from courses.models import Course
from courses.course import *
from users.models import User
from django.db import IntegrityError
from django.template.defaultfilters import slugify 

'''
	Functions in this file allow an instructor to create a course, add users to the course, search for user names, and remove users. In addition, there are functions that allow a student to join a course. 
	@author Jon Inloes
'''
def create_course(request):
	print "Create Class\n" #TODO
	if request.method == "POST":
		name = request.POST['coursename']

		try:
			c = Course.objects.get(slug=name)
			return render_to_response('courses/create_course_dup.html', {'courses': Course.objects.all()})
		except Course.DoesNotExist:
			course = CreateCourse(name, User.objects.get(username = "fakeuser"))
			course.save()
		
	return render_to_response('courses/create_course.html', {'courses': Course.objects.all()})

def show_roster(request, course_slug, courses):
	course = Course.objects.get(slug=course_slug)
	enrollments = course.roster.all();

	return render_to_response('roster/index.html', {'course': course, 'enrollments': enrollments, 'courses': courses, 'course_slug': course.slug})

def show_course(request, courses, course_slug):
	return render_to_response('index.html', {'courses': courses, 'course_slug': course_slug})

def add_user(request, course_slug, courses):
	
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
				return render_to_response('adduser/failed.html', {'course_slug':course_slug, 'courses': courses, 'course': course})
			
			#show the roster screen
			return HttpResponseRedirect("/%s/roster/" % course_slug)
		elif request.POST['command'] == 'search':
			#if the command was a search, search for the user
	
			firstname = request.POST['firstname']
			lastname = request.POST['lastname']

			users = User.objects.filter(first_name = firstname, last_name = lastname)

	
			return render_to_response('adduser/search.html', {'course_slug': course_slug, 'courses':courses, 'course':course, 'users':users, 'firstname': firstname, 'lastname': lastname})
	else:
		
		#display the adduser page
		return render_to_response('adduser/index.html', {'course_slug': course_slug, 'courses':courses, 'course': course, 'url': request.path})

def search_username(request, course_slug, courses):
	course = Course.objects.get(slug=course_slug)
	
	firstname = request.POST['firstname']
	lastname = request.POST['lastname']
	
	url = request.path
	print url

	users = User.objects.filter(first_name = firstname, last_name = lastname)

	
	return render_to_response('adduser/search.html', {'course_slug': course_slug, 'courses':courses, 'course':course, 'users':users, 'firstname': firstname, 'lastname': lastname, 'url': request.path})

def remove_user(request, course_slug, courses):
	removeName = request.POST['username']
	course = Course.objects.get(slug=course_slug)

	try:
		user = User.objects.get(username=removeName)
		removeUser(course,user)
	except	User.DoesNotExist:
		pass
	
	
	return HttpResponseRedirect("/%s/roster/" % course_slug)

def cancel_add(request, course_slug, courses):

	return HttpResponseRedirect("/%s/roster/" % course_slug)

def join_course_form(request):
	courses = Course.objects.all()
	return render_to_response('courses/join_course_form.html', \
			{'courses':courses})

def join_course_request(request):
	courseid = request.GET['courseid']
	course = Course.objects.get(id=courseid)
	user = User.objects.get(username='fakeuser')
	enrollment = addUser(course, user, True)
	if enrollment == None:
		return render_to_response('courses/join_course_already_enrolled.html', \
				{'course':course, 'user':user})
	else:
		return render_to_response('courses/join_course_successful.html', \
				{'course':course, 'user':user})
