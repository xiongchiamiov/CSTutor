from django.shortcuts import render_to_response
from courses.models import Course
from models import Page
from question.models import MultipleChoiceQuestion

'''
Views file for quiz related views

This file contains methods for creating a quiz and showing a quiz. More methods will be added to this file in time.

@author Evan Kleist
'''

def create_quiz(request):
	print "Create Quiz\n" #TODO
	return render_to_response('quiz/create-quiz.html', {'courses': Course.objects.all()})

def show_quiz(request, course, courses, pid):
	quiz = Page.objects.get(slug=pid)
	quiz = quiz.quiz
	quizTitle = quiz.text
	questions = quiz.questions.all()

	mcQuestions = []
	codeQuestions = []

	for q in questions:
		try:
			q = q.multiplechoicequestion
			mcQuestions.append(q)
		except MultipleChoiceQuestion.DoesNotExist:
			codeQuestions.append(q.CodeQuestions)
	
	return render_to_response('quiz/index.html', {'course':course, 'courses':courses, 'pid':pid, 'quizTitle':quizTitle, 'mcQuestions':mcQuestions})

