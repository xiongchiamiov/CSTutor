'''
Views file for quiz related views

This file contains methods for creating a quiz and showing a quiz. More methods will be added to this file in time.

@author Evan Kleist
'''

from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, Http404
from courses.models import Course
from models import Page
from models import Quiz
from quiz import *
from question.models import MultipleChoiceQuestion
from question.models import CodeQuestion
from question.question import *
from home.views import master_rtr
from pages.page import insertChildPage

def create_quiz(request, course_slug, page_slug):
	''' create_Quiz View
		This view will create a quiz and take the user to the quiz editor screen.
	'''
	print "Create Quiz\n" #TODO
	#quiz = Quiz.createQuiz("New Quiz", False)
	#print("quiz" + quiz.text)
	
	if request.method == "POST" and "Create Quiz" in request.POST:
		print "Creating quiz name: " 
		course = Course.objects.get(slug=course_slug)
		name = request.POST['name']
		newQuiz = Quiz(course=course, name=name, slug=slugify(name), text=name)
		insertChildPage(newQuiz, Page.objects.get(slug=page_slug))
		return edit_quiz(request, course_slug, slugify(name))
	else:
		return master_rtr(request, 'page/quiz/create-quiz.html')

def show_quiz(request, course, page_slug):
	''' show_Quiz View
		This view displays a quiz on the screen. The user can then answer the
		questions and submit the result
	'''
	quiz = Quiz.objects.get(slug=page_slug)
	quizTitle = quiz.text
	questions = quiz.questions.all().order_by("order")

	return master_rtr(request, 'page/quiz/viewQuiz.html', \
			            {'course':course, 'course_slug':course, \
							 'quizTitle':quizTitle, \
							 'page_slug':page_slug, 'questions':questions})

def delete_quiz(request, course_slug, page_slug):
	''' delete_quiz View
		This view confirms deletion of a quiz. The user can then choose
		 to delete the quiz or cancel
	'''
	quiz = Quiz.objects.get(slug=page_slug)

	return master_rtr(request, 'page/quiz/delete_quiz.html', \
			            {'course':course_slug, 'course_slug':course_slug, 'page_slug':page_slug, 'quiz':quiz})

def remove_question(request, course_slug, page_slug, qNum):
	''' remove_question View
		This view confirms deletion of a question. The user can then choose
		 to delete the question or cancel
	'''
	quiz = Quiz.objects.get(slug=page_slug)
	question = quiz.questions.get(order=qNum)

	return master_rtr(request, 'page/quiz/remove_question.html', \
			            {'course':course_slug, 'course_slug':course_slug, 'page_slug':page_slug, 'question':question})

def submitQuiz(request, course_slug, page_slug):
	''' submitQuiz View
		This view will submit a quiz and create a statistic in the database. It will give the user
		their score and then direct the user to the appropriate path
	'''
	# Make sure the course actually exists in the database
	try:
		course = Course.objects.get(slug=course_slug)
	except Course.DoesNotExist:
		raise Http404

	# Make sure the quiz actually exists in the database
	try:
		quiz = Quiz.objects.get(slug=page_slug)
	except Quiz.DoesNotExist:
		raise Http404

	maxScore = len(quiz.questions.all())
	score = 0
	percentage = 100

	if (request.method == "POST"):
		score = scoreQuiz(quiz, request, course_slug, page_slug)
	else:
		return master_rtr(request, 'page/denied.html', {'course':course_slug, 'loggedIn':False})

	if (not (maxScore == 0)):
		percentage = round(float(score) / float(maxScore), 2) * 100
			
	return master_rtr(request, 'page/quiz/submitQuiz.html', \
			{'course':course_slug, 'course_slug':course_slug, \
			 'page_slug':page_slug, 'pid':page_slug, 'score':score, 'maxScore':maxScore, 'percentage':percentage})

def edit_quiz(request, course_slug, page_slug):
	''' edit_quiz View
		This view allows an instructor or other priviledged user to edit a quiz. The instructor can add, modify,
		or remove questions and other quiz attributes. The modified quiz is then submitted to the database.

		Note 1) Pressing "New Multiple Choice Question" will discard any changes made to the quiz, returning it 
				to its previous state but with a new multiple choice question appended at the end
	'''
	# Make sure the course actually exists in the database
	try:
		course = Course.objects.get(slug=course_slug)
	except Course.DoesNotExist:
		raise Http404

	# Make sure the quiz actually exists in the database
	try:
		quiz = Quiz.objects.get(slug=page_slug)
	except Quiz.DoesNotExist:
		raise Http404

	pages = Course.objects.get(slug=course_slug).pages.all()
	questions = quiz.questions.all().order_by("order")
	prerequisites = quiz.prerequisites.all()
	prereqs = []
	print pages
	for p in prerequisites:
		prereqs.append(p.requiredQuiz.slug)
	print prereqs
	if (request.method == "POST"):
		if "Save" in request.POST:
			r = saveQuiz(request, course_slug, page_slug)
			if (r == -1):
				print "Bad question ordering!"
			else:
				return HttpResponseRedirect(reverse('pages.views.show_page', args=[course_slug, r]))

		if "Cancel" in request.POST:
			return HttpResponseRedirect(reverse('pages.views.show_page', args=[course_slug, page_slug]))

		if "Delete" in request.POST:
			return delete_quiz(request, course_slug, page_slug)
		if "ConfirmDelete" in request.POST:
			removeQuiz(quiz)
			return HttpResponseRedirect(reverse('courses.views.show_course', args=[course_slug]))

		if "Move" in request.POST:
			return HttpResponseRedirect(reverse('pages.views.move_page', args=[course_slug, page_slug]))

		if "NewMultQuestion" in request.POST:
			addMultipleChoiceQuestion(quiz)
			return HttpResponseRedirect(request.path)

		if "NewCodeQuestion" in request.POST:
			print "new code question"
			addCodeQuestion(quiz)
			return HttpResponseRedirect(request.path)

		for q in questions:
			if ("removeQuestion%s" % q.order) in request.POST:
				return remove_question(request, course_slug, page_slug, q.order)
			if ("confirmRemoveQuestion%s" % q.order) in request.POST:
				removeQuestion(q)
				reorderQuestions(quiz)
				return HttpResponseRedirect(request.path)
			if (isMultipleChoiceQuestion(q)):
				q = q.multiplechoicequestion
				if ("addAnswer%s" % q.order) in request.POST:
					addAnswer(q)
					return HttpResponseRedirect(request.path)
				for a in q.answers.all():
					if ("removeAnswerQ%sA%s" % (q.order, a.order)) in request.POST:
						removeAnswer(q, a)
						return HttpResponseRedirect(request.path)

	return master_rtr(request, 'page/quiz/edit_quiz.html', \
			{'course':course_slug, 'course_slug':course_slug, 'page_slug':page_slug, \
			 'pages':pages, 'quiz':quiz, 'questions':questions, 'prereqs':prereqs})
