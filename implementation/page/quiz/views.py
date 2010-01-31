from django.shortcuts import render_to_response
from courses.models import Course
from models import Page

'''
Views file for quiz related views

This file contains methods for creating a quiz and showing a quiz. More methods will be added to this file in time.

@author Evan Kleist
'''

def create_quiz(request):
	print "Create Quiz\n" #TODO
	return render_to_response('quiz/create-quiz.html', {'courses': Course.objects.all()})

def show_quiz(request, course, courses, pid, quizTitle):
	quiz = Page.objects.get(slug=pid)
	quiz = quiz.quiz
	questions = quiz.questions.all()

	mcQuestions = []
	codeQuestions = []

	for q in questions:
		try:
			mcQuestions.append(q.MultipleChoiceQuestion)
		except Quiz.MultipleChoiceQuestion.DoesNotExist:
			codeQuestions.append(q.CodeQuestions)
	
	return render_to_response('quiz/index.html', {'course':course, 'courses':courses, 'pid':pid, 'quizTitle':quizTitle, 'mcQuestions':mcQuestions})

