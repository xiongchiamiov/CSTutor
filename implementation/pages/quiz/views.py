'''
Views file for quiz related views

This file contains methods for creating a quiz and showing a quiz. More methods will be added to this file in time.

@author Evan Kleist
'''

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from courses.models import Course
from models import Page
from models import Quiz
from quiz import *
from question.models import MultipleChoiceQuestion
from question.models import CodeQuestion
from home.views import master_rtr

def create_quiz(request):
	''' create_Quiz View
		This view will create a quiz and take the user to the quiz editor screen.
	'''
	print "Create Quiz\n" #TODO
	return master_rtr(request, 'quiz/create-quiz.html', {'courses': Course.objects.all()})

def show_quiz(request, course, pid):
	''' show_Quiz View
		This view displays a quiz on the screen. The user can then answer the
		questions and submit the result
	'''
	quiz = Quiz.objects.get(slug=pid)
	quizTitle = quiz.text
	questions = quiz.questions.all().order_by("order")

	return master_rtr(request, 'quiz/viewQuiz.html', {'course':course, 'pid':pid, 'quizTitle':quizTitle, 'questions':questions})

def submitQuiz(request, course_slug, pid):
	''' submitQuiz View
		This view will submit a quiz and create a statistic in the database. It will give the user
		their score and then direct the user to the appropriate path
	'''
	return master_rtr(request, 'quiz/submitQuiz.html', {'course':course_slug, 'pid':pid})

def edit_quiz(request, course_slug, pid):
	''' edit_quiz View
		This view allows an instructor or other priviledged user to edit a quiz. The instructor can add, modify,
		or remove questions and other quiz attributes. The modified quiz is then submitted to the database.
	'''
	if (request.method == "POST"):
		if "Save" in request.POST:
			pid = saveQuiz(request, course_slug, pid)
			return HttpResponseRedirect("/%s/%s/" % (course_slug, pid))
		if "Cancel" in request.POST:
			return HttpResponseRedirect("/%s/%s/" % (course_slug, pid))
	quiz = Quiz.objects.get(slug=pid)
	quizTitle = quiz.text
	questions = quiz.questions.all().order_by("order")
	return master_rtr(request, 'quiz/edit_quiz.html', {'course':course_slug, 'pid':pid, 'quizTitle':quizTitle, 'questions':questions})
