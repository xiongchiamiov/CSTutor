'''
quiz.py fil for quiz related operations.

Contains operations for all lessons

@author Evan Kleist
'''
from django.template.defaultfilters import slugify
from models import *
from question.models import *

def CreateQuiz(name):
	return Lesson(slug=slugify(name), name=name)

def saveQuiz(request, course, pid):
	if (request.method != "POST"):
		return -1
	if "Save" in request.POST:
		quiz = Page.objects.get(slug=pid)
		quiz = quiz.quiz
		quiz.text = request.POST["quizTitle"]
		quiz.name = request.POST["quizTitle"]
		quiz.slug = slugify(quiz.name)
		quiz.hidden = request.POST["hidden"]
		questions = quiz.questions.all()
		for q in questions:
			try:
				q = q.multiplechoicequestion
				for a in q.answers.all():
					a.text = request.POST['mcq%sa%s' % (q.order, a.order)]
					a.save()
				q.text = request.POST['mcq%dtext' % q.order]
				q.order = request.POST['mcq%dorder' % q.order]
			except MultipleChoiceQuestion.DoesNotExist:
				q = q.codequestion
				q.text = request.POST['cq%dtext' % q.order]
				q.order = request.POST['cq%dorder' % q.order]
			q.save()
		quiz.save()
		return quiz.slug
	return -1

def removeQuiz(request, course, pid):
	if (request.method != "POST"):
		return -1
	if "Delete" in request.POST:
		Quiz.objects.get(slug=pid).delete()
		return 0

def addMultipleChoiceQuestion(request, course, pid):
	quiz = Quiz.objects.get(slug=pid)
	newQuestion = MultipleChoiceQuestion(text='Blank Question', order=99, quiz=quiz)
	newQuestion.save()
	return 0
