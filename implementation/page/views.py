from django.shortcuts import render_to_response
#from page.models import Page
from models import Page
#from page.lesson.views import show_lesson
from lesson.views import show_lesson
from quiz.views import show_quiz
from courses.views import show_course
from quiz.models import Quiz
from lesson.models import Lesson

def show_page(request, course_slug, courses, pid):
	page = Page.objects.get(slug=pid)

	try:
		page = page.lesson
	except Lesson.DoesNotExist:
		try:
			page = page.quiz
		except Quiz.DoesNotExist:
			print "Page is neither quiz or lesson"
	return page.show(request, course_slug, courses, pid)
