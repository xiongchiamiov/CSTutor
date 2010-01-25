from django.db import models
from page.models import Page
from courses.models import Course
from views import show_quiz

# Create your models here.

class Quiz(Page):
	'''
	Model for a Quiz.

	A quiz is a specific type of Page.  It contains a number of questions of
	various types.
	'''
	text = models.TextField()
	# paths implied from Path
	# questions implied from Question
	# course inherited from Page
	hidden = models.BooleanField()

	@staticmethod
	def createQuiz(text_, hidden_, course_, parent_, ):
		''' Creates a new Quiz object, and returns it unsaved '''
		q = Quiz(text=text_, hidden = hidden_)
		return q

	def __unicode__(self):
		return self.text
	
	def show(self, request, course, courses, pid):
		return show_quiz(request, course, courses, pid)

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

	def __unicode__(self):
		return u'Path on Quiz ' + unicode(quiz)
