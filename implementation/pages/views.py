from django.shortcuts import render_to_response
from django.http import HttpResponse
#from page.models import Page
from models import Page
#from page.lesson.views import show_lesson
from lesson.views import show_lesson
from quiz.views import show_quiz
from lesson.views import edit_lesson
from quiz.views import edit_quiz
from courses.views import show_course
from quiz.models import Quiz
from lesson.models import Lesson
from models import Course

'''
Views file for page related view

Contains the show_page function

@author Evan Kleist
@author Russell Mezzetta
'''

def show_page(request, course_slug, pid):
	#check if the course is a real course in the database	
	try: 
		Course.objects.get(slug=course_slug)
	except Course.DoesNotExist:
		return HttpResponse("ERROR: BAD URL: The course: %s does not exist" % (course_slug))
	#check if the page is a real page in the database
	try:
		page = Page.objects.get(slug=pid)
	except Page.DoesNotExist:
		return HttpResponse("ERROR: BAD URL: The course: %s does not contain the page: %s." % (course_slug, pid))
	#case the page to a lesson or quiz then call show on it
	try:
		page = page.lesson
	except Lesson.DoesNotExist:
		try:
			page = page.quiz
		except Quiz.DoesNotExist:
			print "Page is neither quiz or lesson"
		return show_quiz(request, course_slug, pid)
	return show_lesson(request, course_slug, pid)

def edit_page(request, course_slug, pid):
	#check if the course is a real course in the database	
	try: 
		Course.objects.get(slug=course_slug)
	except Course.DoesNotExist:
		return HttpResponse("ERROR: BAD URL: The course: %s does not exist" % (course_slug))
	#check if the page is a real page in the database
	try:
		page = Page.objects.get(slug=pid)
	except Page.DoesNotExist:
		return HttpResponse("ERROR: BAD URL: The course: %s does not contain the page: %s." % (course_slug, pid))
	#cast the page to a lesson or quiz then call show on it
	try:
		page = page.lesson
	except Lesson.DoesNotExist:
		try:
			page = page.quiz
		except Quiz.DoesNotExist:
			return HttpResponse("ERROR: Page is neither quiz or lesson")
		return edit_quiz(request, course_slug, pid)
	return edit_lesson(request, course_slug, pid)
