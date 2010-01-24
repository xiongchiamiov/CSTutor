from django.shortcuts import render_to_response
#from page.models import Page
from models import Page
#from page.lesson.views import show_lesson
from lesson.views import show_lesson

def show_page(request, course, courses, pid):

	#take these two lines out when we have data to work with
	if 1 == 1:	
		return show_lesson(request, course, courses, pid)
	
	
	page = Page.objects.get(slug=pid)

	if page.__class__ == 'page.models.Quiz':
	#should be page.quiz.models.Quiz b/c of new folder structure?
		return show_quiz(request, course, courses, pid)
	elif page.__class__ == 'page.lesson.models.Lesson':
		return show_lesson(request, course, courses, pid)

def show_quiz(request, course, courses, pid):
	return render_to_response('quiz/index.html', {'course':course, 'courses':courses, 'pid':pid})

