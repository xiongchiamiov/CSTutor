from django.shortcuts import render_to_response
from courses.models import Course
from pages.lesson.models import Lesson
from home.views import master_rtr

def create_lesson(request):
	print "Create Lesson\n" #TODO
	return master_rtr(requeset, 'lesson/create-lesson.html')

def show_lesson(request, course, pid):
  # To get lessonConent now, you need to retreieve the page from the database, cast it to a lesson, and get the "text" attribute
	#shouldn't have to try/except because previous calls should guarentee the page exists	
	content = Lesson.objects.get(slug=pid).content
	return master_rtr(request, 'page/lesson/index.html', {'course':course, 'pid':pid, 'content':content})

