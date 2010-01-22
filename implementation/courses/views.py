from django.shortcuts import render_to_response
from courses.models import Course

def show_roster(request, course, courses):
	course = Course.objects.get(slug=course)
	enrollments = course.roster.all();
	userList = []

	for enrollment in enrollments:
		#do something
		userList.append(enrollment.user.first_name)

	return render_to_response('roster/index.html', {'course': course, 'users': userList, 'courses': courses})

def show_course(request, courses, course):
	return render_to_response('index.html', {'courses': courses})
