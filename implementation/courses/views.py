from django.shortcuts import render_to_response
from courses.models import Course

def show_roster(request):
	courseid = request.GET['courseid']
	course = Course.objects.filter(id=courseid)
	enrollments = course.roster.all();
	userList = []

	for enrollment in enrollments:
		#do something
		userList.append(user.name)

	return render_to_response('roster/index.html', {'course': course, 'users': usersList,})

def show_course(request, courses, course):
	return render_to_response('index.html', {'courses': courses})
