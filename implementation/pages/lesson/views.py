from django.shortcuts import render_to_response
from courses.models import Course
from pages.lesson.models import Lesson

def create_lesson(request):
	print "Create Lesson\n" #TODO
	return render_to_response('lesson/create-lesson.html', {'courses': Course.objects.all()})

def show_lesson(request, course, courses, pid):
  # To get lessonConent now, you need to retreieve the page from the database, cast it to a lesson, and get the "text" attribute
	#shouldn't have to try/except because previous calls should guarentee the page exists	
	content = Lesson.objects.get(slug=pid).content
	return render_to_response('page/lesson/index.html', 
									{'course':course, 'courses':courses, 'pid':pid, 'content':content})

