'''
Views file for quiz related views

This file contains methods for creating a quiz and showing a quiz. More methods will be added to this file in time.

@author Evan Kleist
'''

from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, Http404
from courses.models import Course, Enrollment
from models import Page
from models import Quiz
from quiz import *
from question.models import MultipleChoiceQuestion
from question.models import CodeQuestion
from question.question import *
from home.views import master_rtr, custom_403
from pages.page import insertLastChildPage
from django.core.exceptions import ObjectDoesNotExist

def create_quiz(request, course_slug, page_slug):
	''' create_Quiz View
		This view will create a quiz and take the user to the quiz editor screen.
	'''
	#enforcing permissions
	try:
		e = Enrollment.objects.get(course__slug = course_slug, user = request.user)
	except Enrollment.DoesNotExist:
		return custom_403(request, "User cannot create a quiz in the course because the user is not enrolled in this course")
	if not e.edit:
		return custom_403(request, "User cannot create a quiz in the course because the user does not have edit permissions on the course")

	page_slug = safeSlug(page_slug)
	
	if request.method == "POST" and "Create Quiz" in request.POST:
		course = Course.objects.get(slug=course_slug)
		name = request.POST['name']
		newQuiz = Quiz(course=course, name=name, slug=slugify(name), text=name, upToDate=True)
		insertLastChildPage(newQuiz, Page.objects.get(slug=page_slug))
		newQuiz = Quiz.objects.get(slug=newQuiz.slug)
		workingCopy = Quiz(course=newQuiz.course, name=newQuiz.name, slug=(newQuiz.slug + "_workingCopy"), text=newQuiz.name, left=0, right=0)
		workingCopy.save()
		return HttpResponseRedirect(reverse('pages.views.edit_page', args=[course_slug, newQuiz.slug]))
	else:
		return master_rtr(request, 'page/quiz/create-quiz.html')

def show_quiz(request, course, page_slug):
	''' show_Quiz View
		This view displays a quiz on the screen. The user can then answer the
		questions and submit the result

		If the user is trying to view the working_copy, they are shown the
		regular copy instead. This is to prevent a student from looking
		at unpublished quizzes
	'''
	page_slug = safeSlug(page_slug)
	quiz = Quiz.objects.get(slug=page_slug)

	# If the quiz is hidden, make sure prerequisites have been met
	if (quiz.hidden and not checkPrerequisites(quiz, request.user)):
		return master_rtr(request, 'page/denied.html', {'course':course, 'course_slug':course, 'prereqs':True})
	
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
	page_slug = safeSlug(page_slug)
	quiz = Quiz.objects.get(slug=page_slug)

	return master_rtr(request, 'page/quiz/delete_quiz.html', \
			            {'course':course_slug, 'course_slug':course_slug, 'page_slug':page_slug, 'quiz':quiz})

def add_path(request, course_slug, page_slug, errors):
	''' add_path View
		This view allows you to add a path to the quiz. The user can then choose
		 to save the path or cancel
	'''
	page_slug = safeSlug(page_slug)
	quiz = Quiz.objects.get(slug=page_slug)
	course = Course.objects.get(slug=course_slug)
	allPages = course.pages.all()
	pages = []
	for p in allPages:
		if (p.slug == safeSlug(p.slug)):
			pages.append(p)

	return master_rtr(request, 'page/quiz/path.html', \
			            {'course_slug':course_slug, 'page_slug':page_slug, 'pages':pages, 'errors':errors})

def edit_path(request, course_slug, page_slug, errors):
	''' edit_path View
		This view allows you to edit an existing path for the quiz. The user can then choose
		 to save the path or cancel
	'''
	page_slug = safeSlug(page_slug)
	quiz = Quiz.objects.get(slug=page_slug + "_workingCopy")
	course = Course.objects.get(slug=course_slug)
	allPages = course.pages.all()
	pages = []
	for p in allPages:
		if (p.slug == safeSlug(p.slug)):
			pages.append(p)

	path = quiz.paths.get(lowscore=request.POST["path"])

	return master_rtr(request, 'page/quiz/path.html', \
			            {'course_slug':course_slug, 'page_slug':page_slug, 'pages':pages, 'path':path, 'errors':errors})



def remove_question(request, course_slug, page_slug, qNum):
	''' remove_question View
		This view confirms deletion of a question. The user can then choose
		 to delete the question or cancel
	'''
	page_slug = safeSlug(page_slug)
	quiz = Quiz.objects.get(slug=page_slug)
	question = quiz.questions.get(order=qNum)

	return master_rtr(request, 'page/quiz/remove_question.html', \
			            {'course':course_slug, 'course_slug':course_slug, 'page_slug':page_slug, 'question':question})

def submitQuiz(request, course_slug, page_slug):
	''' submitQuiz View
		This view will submit a quiz and create a statistic in the database. It will give the user
		their score and then direct the user to the appropriate path
	'''
	page_slug = safeSlug(page_slug)

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

	#if the course is private then check that the user is enrolled and has view permissions
	if course.private:
		if not request.user.is_authenticated():
			return master_rtr(request, 'page/denied.html', {'course':course_slug, 'enrolled':False, 'edit':False, 'loggedIn':False})
		try:#try to get the enrollment for this user and check view permission
			e = quiz.course.roster.get(user=request.user)
			if not e.view:
				return master_rtr(request, 'page/denied.html', {'course':course_slug, 'enrolled':True, 'edit':False, 'loggedIn':True})
		except ObjectDoesNotExist:
			# user is not enrolled in this course
			return master_rtr(request, 'page/denied.html', {'course':course_slug, 'enrolled':False, 'edit':False, 'loggedIn':True})

	# Make sure prerequisites are satisfied
	if (not checkPrerequisites(quiz, request.user)):
		return master_rtr(request, 'page/denied.html', {'course':course_slug, 'course_slug':course_slug, 'prereqs':True})

	maxScore = len(quiz.questions.all())
	score = 0
	percentage = 100

	if (request.method == "POST"):
		score = scoreQuiz(quiz, request, course_slug, page_slug)

	if (not (maxScore == 0)):
		percentage = round(float(score) / float(maxScore), 2) * 100

	try:
		path = matchPath(quiz, percentage)
	except NoMatchingPath:
		path = False
			
	return master_rtr(request, 'page/quiz/submitQuiz.html', \
			{'course':course_slug, 'course_slug':course_slug, \
			 'page_slug':page_slug, 'pid':page_slug, 'score':score, 'maxScore':maxScore, 'percentage':percentage, 'path':path})

def edit_quiz(request, course_slug, page_slug):
	''' edit_quiz View
		This view allows an instructor or other priviledged user to edit a quiz. The instructor can add, modify,
		or remove questions and other quiz attributes. The modified quiz is then submitted to the database.

		Note 1) Pressing "New Multiple Choice Question" will discard any changes made to the quiz, returning it 
				to its previous state but with a new multiple choice question appended at the end
	'''
	page_slug = safeSlug(page_slug)
	# Make sure the course actually exists in the database
	try:
		course = Course.objects.get(slug=course_slug)
	except Course.DoesNotExist:
		raise Http404

	# Make sure the quiz actually exists in the database
	try:
		quiz = Quiz.objects.get(slug=(page_slug))
		workingCopy = Quiz.objects.get(slug=(page_slug + "_workingCopy"))
	except Quiz.DoesNotExist:
		raise Http404

	allPages = Course.objects.get(slug=course_slug).pages.all()
	questions = workingCopy.questions.all().order_by("order")
	prerequisites = workingCopy.prerequisites.all()
	paths = workingCopy.paths.all().order_by("lowscore")
	prereqs = []
	errors = []
	pages = []

	for p in allPages:
		if (p.slug == safeSlug(p.slug)):
			pages.append(p)


	for p in prerequisites:
		prereqs.append(p.requiredQuiz.slug)

	if (request.method == "POST"):
		if "Save" in request.POST:
			r = saveQuiz(request, course_slug, page_slug)
			page_slug = safeSlug(r["quiz_slug"])
			errors = r["errors"]
			if (len(errors) == 0):
				return HttpResponseRedirect(reverse('pages.views.show_page', args=[course_slug, page_slug]))

		elif "Cancel" in request.POST:
			return HttpResponseRedirect(reverse('pages.views.show_page', args=[course_slug, page_slug]))

		elif "Delete" in request.POST:
			return delete_quiz(request, course_slug, page_slug)
		elif "ConfirmDelete" in request.POST:
			removeQuiz(quiz)
			return HttpResponseRedirect(reverse('courses.views.show_course', args=[course_slug]))

		elif "Move" in request.POST:
			return HttpResponseRedirect(reverse('pages.views.move_page', args=[course_slug, page_slug]))

		elif "NewMultQuestion" in request.POST:
			addMultipleChoiceQuestion(workingCopy)
			return HttpResponseRedirect(request.path)

		elif "NewCodeQuestion" in request.POST:
			addCodeQuestion(workingCopy)
			return HttpResponseRedirect(request.path)

		elif "Publish" in request.POST:
			r = saveQuiz(request, course_slug, page_slug)
			page_slug = safeSlug(r["quiz_slug"])
			errors = r["errors"]
			if (len(errors) == 0):
				workingCopy = Quiz.objects.get(slug=(page_slug + "_workingCopy"))
				publishQuiz(workingCopy)
				return HttpResponseRedirect(reverse('pages.views.show_page', args=[course_slug, page_slug]))

		elif "Revert" in request.POST:
			revertQuiz(workingCopy)
			return HttpResponseRedirect(reverse('pages.views.show_page', args=[course_slug, page_slug]))

		elif "AddPath" in request.POST:
			return add_path(request, course_slug, page_slug, errors)
		elif "SubmitAddPath" in request.POST:
			errors = addPath(workingCopy, request, course_slug)
			if (len(errors) == 0):
				return HttpResponseRedirect(request.path)
			else:
				return add_path(request, course_slug, page_slug, errors)

		elif "EditPath" in request.POST:
			if ("path" in request.POST):
				return edit_path(request, course_slug, page_slug, errors)
			else:
				errors.append("You must select a path to edit")
		elif "SubmitEditPath" in request.POST:
			errors = editPath(workingCopy, request, course_slug)
			if (len(errors) == 0):
				return HttpResponseRedirect(request.path)
			else:
				return edit_path(request, course_slug, page_slug, errors)

		elif "RemovePath" in request.POST:
			if ("path" in request.POST):
				errors = removePath(workingCopy, request)
				if (len(errors) == 0):
					return HttpResponseRedirect(request.path)
			else:
				errors.append("You must select a path to remove")

		for q in questions:
			if ("removeQuestion%s" % q.order) in request.POST:
				return remove_question(request, course_slug, page_slug, q.order)
			if ("confirmRemoveQuestion%s" % q.order) in request.POST:
				removeQuestion(q)
				reorderQuestions(workingCopy)
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

	return master_rtr(request, 'page/quiz/edit_quiz.html', {'course_slug':course_slug, 'page_slug':page_slug, 'pages':pages, 'quiz':workingCopy, 'questions':questions, 'prereqs':prereqs, 'errors':errors, 'paths':paths})
