from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from courses.models import Course
from courses.course import *
from users.models import User
from django.db import IntegrityError
from django.template.defaultfilters import slugify 

def create_course(request):
	print "Create Class\n" #TODO
	
	return render_to_response('courses/create_course.html', {'courses': Course.objects.all()})

def show_roster(request, course_slug, courses):
	course = Course.objects.get(slug=course_slug)
	enrollments = course.roster.all();

	return render_to_response('roster/index.html', {'course': course, 'enrollments': enrollments, 'courses': courses, 'course_slug': course.slug})

def show_course(request, courses, course_slug):
	return render_to_response('index.html', {'courses': courses, 'course_slug': course_slug})

def add_user(request, course_slug, courses):
	if request.method == 'POST':
		firstname = request.POST['firstname']
		lastname = request.POST['lastname']
		usr = slugify(firstname+lastname)

		user = User()
		user.first_name = firstname
		user.last_name = lastname
		user.username = usr

		try:
			user = User.objects.get(username=usr)
			#user.save()
		except User.DoesNotExist:
			#import pdb; pdb.set_trace()
			#user = User.objects.get(username=usr)
			user.save()

		course = Course.objects.get(slug=course_slug)
		addUser(course, user)
		return HttpResponseRedirect("/%s/roster/" % course_slug)
	else:
		course = Course.objects.get(slug=course_slug)
		return render_to_response('adduser/index.html', {'course_slug': course_slug, 'courses':courses})

def join_course_form(request):
	courses = Course.objects.all()
	return render_to_response('courses/join_course_form.html', \
			{'courses':courses})

def join_course_request(request):
	courseid = request.GET['courseid']
	course = Course.objects.get(id=courseid)
	return render_to_response('courses/join_course_successful.html', \
			{'course':course})
