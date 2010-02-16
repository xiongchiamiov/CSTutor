'''
quiz.py fil for quiz related operations.

Contains operations for all lessons

@author Evan Kleist
'''
from django.template.defaultfilters import slugify
from models import *
from question.models import *
from pages.page import removePage

#def createQuiz(name):
	#return Quiz(text=name)
	#return Quiz(slug=slugify(name), name=name)

def validateQuestionOrder(self):
	'''
		Takes in a quiz, and verifies that all of its questions have
		a unique ordering, and are ordered from 1 -> # of questions

		Returns True if the above constraints are met, False otherwise
	'''
	questions = self.questions.all()
	usedNumbers = set([question.order for question in questions])
	if len(questions) != len(usedNumbers) or \
		min(usedNumbers) != 1 or max(usedNumbers) != len(questions):
			return False
	return True

def saveQuiz(request, course, pid):
	if (request.method != "POST"):
		return -1
	if "Save" in request.POST:
		quiz = Page.objects.get(slug=pid).quiz
		quiz.text = request.POST["quizTitle"]
		quiz.name = request.POST["quizTitle"]
		quiz.slug = slugify(quiz.name)
		if "hidden" in request.POST:
			quiz.hidden = True
		else:
			quiz.hidden = False
		questions = [question for question in quiz.questions.all()]
		origQuestions = []
		origAnswers = []
		for q in questions:
			try:
				q = q.multiplechoicequestion
				origQuestions.append(MultipleChoiceQuestion(text = q.text, order = q.order))
				for a in q.answers.all():
					origAnswers.append(Answer(question = a.question, correct = a.correct, order = a.order, text = a.text))
					a.text = request.POST['mcq%sa%s' % (q.order, a.order)]
					a.save()
				q.text = request.POST['mcq%dtext' % q.order]
				q.order = request.POST['mcq%dorder' % q.order]
			except MultipleChoiceQuestion.DoesNotExist:
				q = q.codequestion
				origQuestions.append(CodeQuestion(text = q.text, order = q.order))
				q.text = request.POST['cq%dtext' % q.order]
				q.order = request.POST['cq%dorder' % q.order]
			q.save()
		if (validateQuestionOrder(quiz)):
			quiz.save()
			return quiz.slug
		else:
			origQuestions = iter(origQuestions)
			origAnswers = iter(origAnswers)
			for q in questions:
				orig = origQuestions.next()
				try:
					q = q.multiplechoicequestion
					q.text = orig.text
					q.order = orig.order
					for a in q.answers.all():
						origA = origAnswers.next()
						a.correct = origA.correct
						a.order = origA.order
						a.text = origA.text
						a.save()
				except MultipleChoiceQuestion.DoesNotExist:
					q.text = orig.text
					q.order = orig.order
					print "Revert code question"
				q.save()
	return -1

def removeQuiz(self):
	removePage(self)
	# should also remove all associated quiz objects such as stats, questions, answers, paths
	return 0

def addMultipleChoiceQuestion(self):
	questions = self.questions.all()
	newQuestion = MultipleChoiceQuestion(text='Blank Question', order=(len(questions)+1), quiz=self)
	newQuestion.save()
	return 0

def reorderQuestions(self):
	questions = self.questions.all().order_by("order")
	qNum = 1
	for q in questions:
		q.order = qNum
		q.save()
		qNum = qNum + 1
	# Sanity check to make sure the question ordering is still valid
	if (validateQuestionOrder(self)):
		return 0
	return -1
