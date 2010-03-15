from django.db import models
from pages.quiz.models import Quiz

'''
Models file for question related classes

Contains the Overall "Question" class, plus the Classes that are primarily
contained within a Question, such as MultipleChoiceQuestion, CodeQuestion and Answer.

@author Evan Kleist

'''

class Question(models.Model):
	'''
	Model for a Question.

	A Question is a particular question on a quiz. It contains a string for the question
	text, an ordering, and a quiz that the question belongs to.

	@author Evan Kleist
	'''
	text = models.TextField()
	order = models.IntegerField()
	quiz = models.ForeignKey(Quiz, related_name='questions')


class MultipleChoiceQuestion(Question):
	'''
	Model for MultipleChoiceQuestion.

	A MultipleChoiceQuestion is a specific type of question. It contains a list of all
	possible answers to the question. Note the data indicating which answer is correct 
	is contained within the answer object.

	@author Evan Kleist
	'''
	# answers is implied from Answer
	# quiz inherited from Question

class CodeQuestion(Question):
	'''
	Model for CodeQuestion.

	A CodeQuestion is a specific type of question which involves the user typing in code
	which is then executed and compared against desired output. This class contains a 
	string for the code(if some is provided) and a string for the desired output

	@author Evan Kleist
	'''

	beforeCode = models.TextField()
	showBeforeCode = models.BooleanField()
	editableCode = models.TextField()
	afterCode = models.TextField()
	showAfterCode = models.BooleanField()
	expectedOutput = models.TextField()
	# quiz inherited from Question

class Answer(models.Model):
	'''
	Model for Answer.

	An Answer is a possible answer to a multiple choice question. Each Answer contains
	the string associated with the Answer and a boolean indicating whether or not it is
	the correct answer to the multiple choice question.

	@author Evan Kleist
	'''
	question = models.ForeignKey(MultipleChoiceQuestion, related_name='answers')
	correct = models.BooleanField(default=False)
	order = models.IntegerField()
	text = models.TextField()
