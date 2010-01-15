'''
Models file for page related classes

Contains the Overall "Page" class, plus the Classes that are primarily
contained within a Page, such as Quiz and Lesson. In addition it contains
classes for path, question, codeQuestion, multipleChoiceQuestion, and answer.

Author(s): Russell Mezzetta

'''
from django.db import models

# Create your models here.

class Page(models.Model):
	'''
	A single unit of a course

	A page contains links to other pages based on the Course flow.
	'''
	pass

class Lesson(Page):
	'''
	Model for a Lesson.

	A lesson is a specific type of Page.  It represents a single Topic that
	is represented on a single "Page."  Lessons can include executable code
	segments and images.
	'''
	pass

class Quiz(Page):
	'''
	Model for a Quiz.

	A quiz is a specific type of Page.  It contains a number of questions of
	various types.
	'''
	pass

class Path(models.Model):
	'''
	Model for a Path.

	A path determines where a student is sent after taking a quiz. It contains a range
	of scores, a destination page number, and some text to display to the student.
	'''
	pass

class Question(models.Model):
	'''
	Model for a Question.

	A Question is a particular question on a quiz. It contains a string for the question
	text and a title.
	'''
	pass

class MultipleChoiceQuestion(Question):
	'''
	Model for MultipleChoiceQuestion.

	A MultipleChoiceQuestion is a specific type of question. It contains a list of all
	possible answers to the question. Note the data indicating which answer is correct 
	is contained within the answer object.
	'''
	pass

class CodeQuestion(Question):
	'''
	Model for CodeQuestion.

	A CodeQuestion is a specific type of question which involves the user typing in code
	which is then executed and compared against desired output. This class contains a 		
	string for the code(if some is provided) and a string for the desired output
	'''
	pass

class Answer(models.Model):
	'''
	Model for Answer.

	An Answer is a possible answer to a multiple choice question. Each Answer contains
	the string associated with the Answer and a boolean indicating whether or not it is
	the correct answer to the multiple choice question.
	'''
	pass

