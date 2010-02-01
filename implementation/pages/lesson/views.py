from django.shortcuts import render_to_response
from courses.models import Course

def create_lesson(request):
	print "Create Lesson\n" #TODO
	return render_to_response('lesson/create-lesson.html', {'courses': Course.objects.all()})

def show_lesson(request, course, courses, pid):
  # To get lessonConent now, you need to retreieve the page from the database, cast it to a lesson, and get the "text" attribute
	return render_to_response('page/lesson/index.html', 
									{'course':course, 'courses':courses, 'pid':pid})

