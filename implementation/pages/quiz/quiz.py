'''
quiz.py fil for quiz related operations.

Contains operations for all lessons

@author Evan Kleist
'''
from django.template.defaultfilters import slugify
from models import *
from question.models import *
from question.question import isMultipleChoiceQuestion
from question.question import removeQuestion
from pages.page import removePage
from stats.models import Stat


def addMultipleChoiceQuestion(self):
	'''
		Takes a quiz and adds a blank multiple choice question to it
	'''
	questions = self.questions.all()
	newQuestion = MultipleChoiceQuestion(order=(len(questions)+1), quiz=self)
	newQuestion.save()
	return newQuestion

def addCodeQuestion(self):
	'''
		Takes a quiz and adds a blank code question to it
	'''
	questions = self.questions.all()
	newQuestion = CodeQuestion(order=(len(questions)+1), quiz=self)
	newQuestion.save()
	return newQuestion

#def createQuiz(name):
	#return Quiz(text=name)
	#return Quiz(slug=slugify(name), name=name)

def removeQuiz(self):
	'''
		Removes a quiz from the database, as well as all related 
		objects
	'''
	questions = self.questions.all()
	for q in questions:
		removeQuestion(q)
	removePage(self)
	# should also remove all associated quiz objects such as stats, questions, answers, paths
	return 0

def reorderQuestions(self):
	'''
		Takes a quiz, retrieves its questions, and then reorders the 
		questions into a valid state.
	'''
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

def saveQuiz(request, course, pid):
	'''
		Takes a request, a course, and a page id. It then pulls the 
		quiz from the post data and updates the elements in the 
		database. Before saving, it validates for proper data before 
		saving
	'''
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
		# Delete current prerequisites
		curPrereqs = quiz.prerequisites.all()
		for p in curPrereqs:
			p.delete()
		print request.POST
		if "prereqs" in request.POST:
			# Create prerequisites
			for p in request.POST.getlist("prereqs"):
				reqQuiz = Course.objects.get(slug=course).pages.get(slug=p).quiz
				newPrereq = Prerequisite(containingQuiz=quiz, requiredQuiz=reqQuiz)
				newPrereq.save()
				
		questions = [question for question in quiz.questions.all()]
		origQuestions = []
		origAnswers = []
		for q in questions:
			if (isMultipleChoiceQuestion(q)):
				q = q.multiplechoicequestion
				origQuestions.append(MultipleChoiceQuestion(text = q.text, order = q.order))
				for a in q.answers.all():
					origAnswers.append(Answer(question = a.question, correct = a.correct, order = a.order, text = a.text))
					a.text = request.POST['mcq%sa%s' % (q.order, a.order)]
					a.correct = (request.POST['mcq%sac' % q.order] == str(a.order))
					a.save()
				q.text = request.POST['mcq%stext' % q.order]
				q.order = request.POST['mcq%sorder' % q.order]
			else:
				q = q.codequestion
				origQuestions.append(CodeQuestion(text = q.text, order = q.order, expectedOutput = q.expectedOutput))
				q.text = request.POST['cq%stext' % q.order]
				q.order = request.POST['cq%sorder' % q.order]
				q.expectedOutput = request.POST['cq%seo' % q.order]
			q.save()
		if (validateQuestionOrder(quiz)):
			quiz.save()
			return quiz.slug
		else:
			origQuestions = iter(origQuestions)
			origAnswers = iter(origAnswers)
			for q in questions:
				orig = origQuestions.next()
				if (isMultipleChoiceQuestion(q)):
					q = q.multiplechoicequestion
					q.text = orig.text
					q.order = orig.order
					for a in q.answers.all():
						origA = origAnswers.next()
						a.correct = origA.correct
						a.order = origA.order
						a.text = origA.text
						a.save()
				else:
					q.codequestion
					q.text = orig.text
					q.order = orig.order
					q.expectedOutput = orig.expectedOutput
				q.save()
	return -1

def scoreQuiz(self, request, course_slug, quiz_slug):
	'''
		Takes a quiz and a request. Pulls the submitted answers from 
		the form contained in the request and compares it to the 
		correct answers specified in the quiz. Generates a statistic 
		for a quiz, adds it to the database and returns their score.
	'''
	questions = self.questions.all()
	course = Course.objects.get(slug=course_slug)
	score = 0

	for q in questions:
		if (isMultipleChoiceQuestion(q)):
			q = q.multiplechoicequestion
			theirAnswer = request.POST['mcq%s' % q.order]
			if (q.answers.get(order=theirAnswer).correct):
				score = score + 1
		else:
			q = q.codequestion
			print "Grade multiple choice question"

	if (not request.user.is_anonymous()):
		Stat.CreateStat(course, self, request.user, score)
	
	return score

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
