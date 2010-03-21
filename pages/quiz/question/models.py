'''
Models file for question related classes

Contains the Overall "Question" class, plus the Classes that are primarily
contained within a Question, such as MultipleChoiceQuestion, CodeQuestion and Answer.

@author Evan Kleist

'''

from django.db import models
from pages.quiz.models import Quiz

class Question(models.Model):
	'''
	Model for a Question.

	A Question is a particular question on a quiz. It contains a string for the question
	text, an ordering, and a quiz that the question belongs to. A question is then further
	defined in the following models

	Data Fields:
	   text = the prompt for the question
	   order = the order of the question
	   quiz = a link to the container quiz for the question

	@author Evan Kleist
	'''
	text = models.TextField()
	order = models.IntegerField()
	quiz = models.ForeignKey(Quiz, related_name='questions')


class MultipleChoiceQuestion(Question):
	'''
	Model for MultipleChoiceQuestion.

	A MultipleChoiceQuestion is a specific type of question. It contains a list of all
	possible answers to the question. Note that a MultipleChoiceQuestion has no data
	fields. It inherits the data fields from the Question class, and all answers for 
	the question to are linked to from the answer class.

	@author Evan Kleist
	'''
	# answers is implied from Answer
	# quiz inherited from Question

class CodeQuestion(Question):
	'''
	Model for CodeQuestion.

	A CodeQuestion is a specific type of question which involves the user typing in code
	which is then executed and compared against desired output.

	Data Fields:
	   expectedOutput - This isnt the output of the program itself. It is the "correct"
	                    program which in turn will generate the "correct" output. In
	                    order for a student to get a code question correct, they need
	                    not match the correct program. Instead, both the "correct"
	                    program contained in this data field as well as the submitted
	                    program are ran and the outputs of both are diff'd.

	@author Evan Kleist
	'''

	expectedOutput = models.TextField()
	# quiz inherited from Question

class Answer(models.Model):
	'''
	Model for Answer.

	An Answer is a possible answer to a multiple choice question. Each Answer contains
	the string associated with the Answer and a boolean indicating whether or not it is
	the correct answer to the multiple choice question.

	Data Fields:
	   question - the container question for the answer
	   correct - boolean indication of correct or not
	   order - order of the answer
	   text - text for the answer

	@author Evan Kleist
	'''
	question = models.ForeignKey(MultipleChoiceQuestion, related_name='answers')
	correct = models.BooleanField(default=False)
	order = models.IntegerField()
	text = models.TextField()
