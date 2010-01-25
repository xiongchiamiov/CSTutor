from django.shortcuts import render_to_response
#from page.models import Page
from models import Page
#from page.lesson.views import show_lesson
#from lesson.views import show_lesson
from quiz.views import show_quiz
from courses.views import show_course

def show_page(request, course, courses, pid):
	
	page = Page.objects.get(slug=pid)

	if page.__class__ == 'page.quiz.models.Quiz':
	#should be page.quiz.models.Quiz b/c of new folder structure?
		return show_quiz(request, course, courses, pid)
	elif page.__class__ == 'page.lesson.models.Lesson':
		return show_lesson(request, course, courses, pid)
	else:
		return show_course(request, course, courses)

