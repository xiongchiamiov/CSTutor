'''
question.py fil for quiestion related operations.

@author Evan Kleist
'''
from django.template.defaultfilters import slugify
from models import *

def removeQuestion(self):
	if (isMultipleChoiceQuestion(self)):
		self = self.multiplechoicequestion
		answers = self.answers.all()
		for a in answers:
			removeAnswer(self, a)
	self.delete()
	# also need to delete all answers

def removeAnswer(self):
	self.delete()

def isMultipleChoiceQuestion(self):
	try:
		self = self.multiplechoicequestion
	except MultipleChoiceQuestion.DoesNotExist:
		return False
	return True

def addAnswer(self):
	if (isMultipleChoiceQuestion(self)):
		self = self.multiplechoicequestion
		answers = self.answers.all()
		newAnswer = Answer(question=self, correct=False, order=(len(answers)+1))
		newAnswer.save()
		return 0
	return -1

def removeAnswer(self, answer):
	answer.delete()
	reorderAnswers(self)
	return 0;

def reorderAnswers(self):
	answers = self.answers.all().order_by("order")
	aNum = 1
	for a in answers:
		a.order = aNum
		a.save()
		aNum = aNum + 1
	return 0
