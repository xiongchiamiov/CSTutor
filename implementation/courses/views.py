from django.shortcuts import render_to_response
from courses.models import Course

def show_roster(request, course, courses):
	course = Course.objects.get(slug=course)
	enrollments = course.roster.all();
	#userList = []


	#for enrollment in enrollments:
		#userList.append(enrollment.user.first_name + ' ' + enrollment.user.last_name)

	return render_to_response('roster/index.html', {'course': course, 'enrollments': enrollments, 'courses': courses})

def show_course(request, courses, course):
	return render_to_response('index.html', {'courses': courses, 'course': course})
