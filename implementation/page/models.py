'''
Models file for page related classes

Contains the Overall "Page" class, plus the Classes that are primarily
contained within a Page, such as Quiz and Lesson. In addition it contains
classes for path, question, codeQuestion, multipleChoiceQuestion, and answer.

Author(s): Russell Mezzetta, Mark Gius, James Pearson

'''
from django.db import models
from courses.models import Course

# Create your models here.

class Page(models.Model):
	'''
	A single unit of a course

	A page contains links to other pages based on the Course flow.
	'''
	course = models.ForeignKey(Course)
	nextPage = models.OneToOneField("self", related_name='prevPage')
	# prevPage implied from Page
	parent = models.ForeignKey("self", related_name='children')
	# children implied from Page
	slug = models.SlugField(unique=True)
	# prereqs: stupid.  Not doing it
	name = models.TextField()

class Lesson(Page):
	'''
	Model for a Lesson.

	A lesson is a specific type of Page.  It represents a single Topic that
	is represented on a single "Page."  Lessons can include executable code
	segments and images.
	'''
	content = models.TextField()
	# code?  Not sure how to handle

class Quiz(Page):
	'''
	Model for a Quiz.

	A quiz is a specific type of Page.  It contains a number of questions of
	various types.
	'''
	text = models.TextField()
	# paths implied from Path
	# questions implied from Question
	hidden = models.BooleanField()

class Path(models.Model):
	'''
	Model for a Path.

	A path determines where a student is sent after taking a quiz.  It contains
	a high and low score (path matches low <= score < high)
   and an optional message to display to a student.
	'''
	quiz = models.ForeignKey(Quiz, related_name='paths')
	highscore = models.IntegerField()
	lowscore = models.IntegerField()
	text = models.TextField()
	toPage = models.ForeignKey(Page)
	passed = models.BooleanField()

class Question(models.Model):
	'''
	Model for a Question.

	A Question is a particular question on a quiz. It contains a string for the question
	text and a title.
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
	'''
	# answers is implied from Answer
	# quiz inherited from Question

class CodeQuestion(Question):
	'''
	Model for CodeQuestion.

	A CodeQuestion is a specific type of question which involves the user typing in code
	which is then executed and compared against desired output. This class contains a 		
	string for the code(if some is provided) and a string for the desired output
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
	'''
	question = models.ForeignKey(MultipleChoiceQuestion, related_name='answers')
	correct = models.BooleanField(default=False)
	order = models.IntegerField()
	text = models.TextField()
