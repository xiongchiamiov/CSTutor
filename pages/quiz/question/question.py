'''
question.py for question related operations.

Contains operations that act on a question

@author Evan Kleist
'''
from django.template.defaultfilters import slugify
from models import *

def removeQuestion(self):
	'''
		Removes a question from a quiz. If the question is a multiple
		choice question, it also removed all linked answers to keep
		the database tidy.

		Parameters:
			self - the question being operated on

		@author Evan Kleist
	'''
	if (isMultipleChoiceQuestion(self)):
		self = self.multiplechoicequestion
		answers = self.answers.all()
		for a in answers:
			removeAnswer(self, a)
	self.delete()

def isMultipleChoiceQuestion(self):
	'''
		Determines whether or not a question is a multiple choice question.
		Returns a boolean.

		Parameters:
			self - the question being checked

		@author Evan Kleist
	'''
	try:
		self = self.multiplechoicequestion
	except MultipleChoiceQuestion.DoesNotExist:
		return False
	return True

def addAnswer(self):
	'''
		Adds a answer to a multiple choice question. If given a code 
		question, it does nothing. Answer is initiated to have blank text,
		set to be incorrect, and is the last answer for the question.

		Parameters:
			self - the question being operated on.

		@author Evan Kleist
	'''
	if (isMultipleChoiceQuestion(self)):
		self = self.multiplechoicequestion
		answers = self.answers.all()
		newAnswer = Answer(question=self, correct=False, order=(len(answers)+1))
		newAnswer.save()

def removeAnswer(self, answer):
	'''
		Removes an answer

		Parameters:
			self - the question being operated on
		   answer - the answer being removed

		@author Evan Kleist
	'''
	answer.delete()
	reorderAnswers(self)

def reorderAnswers(self):
	'''
		Reorders answers so that answers are uniquely ordered from
		1 - # answers

		Parameters:
			self - the question being operated on

		@author Evan Kleist
	'''
	answers = self.answers.all().order_by("order")
	aNum = 1
	for a in answers:
		a.order = aNum
		a.save()
		aNum = aNum + 1
