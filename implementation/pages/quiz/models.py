'''
Models file for Quiz related classes

Contains the Overall "Quiz" class, plus the Classes that are primarily
contained within a Quiz, such as Path and Prerequisite. Questions and Answer
are located in a separate subpackage.

@author Evan Kleist
'''

from django.db import models
from pages.models import Page
from courses.models import Course

class Quiz(Page):
	'''
	Model for a Quiz.

	A quiz is a specific type of Page. Questions, paths, and prerequisites
	contained by a quiz are not held directly by the quiz itself. Rather,
	they are linked to from their specific models (Meaning, a quiz doesnt
	contain a question. A question links to a quiz)

	Data fields:
	   text - the title of the quiz
		hidden - boolean representing if the quiz is hidden or not
	   upToDate - boolean representing if the quiz is up to date or not

	@author Evan Kleist
	'''
	text = models.TextField()
	# paths implied from Path
	# questions implied from Question
	# course inherited from Page
	# prerequisites inherited from Prerequisites
	hidden = models.BooleanField()
	upToDate = models.BooleanField()

	@staticmethod
	def createQuiz(text_, hidden_, course_, parent_, ):
		'''
		Creates a new Quiz object, and returns it unsaved

		@author Evan Kleist
		'''
		q = Quiz(text=text_, hidden = hidden_)
		return q

	def __unicode__(self):
		'''
		Like toString in java
		
		@author Evan Kleist
		'''
		return self.text

	@models.permalink
	def get_absolute_url(self):
		'''
			Returns the url pattern neccesary to get display a quiz
		'''
		return ('pages.quiz.views.show_page', \
		        [str(self.course.slug), self.slug])

class Path(models.Model):
	'''
	Model for a Path. A path is an optional quiz element used in grading quizzes.
	Given a quiz score, it determines whether or not that score is passing.
	It also will display an optional message and link to a reccommended
	next page

	Data fields:
	   text - the optional dialogue to display after submitting a quiz
	   quiz - a link to the containing quiz
	   highscore - the highest score that will match the path
	   lowscore - the lowest score that will match the path
	   toPage - the page displayed in the link for the student
	   passed - boolean representing whether lowscore <= score < highscore
	            is a passing mark or not 

	@author Evan Kleist
	'''
	quiz = models.ForeignKey(Quiz, related_name='paths')
	highscore = models.IntegerField()
	lowscore = models.IntegerField()
	text = models.TextField()
	toPage = models.ForeignKey(Page)
	passed = models.BooleanField()

	def __unicode__(self):
		'''
		Like toString in java

		@author Evan Kleist
		'''
		return u'Path on Quiz ' + unicode(self.quiz)

class NoMatchingPath(Exception):
	'''
	An exception used in Paths. When checking for a matching path
	given a quiz score, it no paths match the score, it raises this exception.
	This could be because no paths exist or because a path doesnt exist for a
	specific score

	@author Evan Kleist
	'''
	def __str__(self):
		return repr(self.value)

class Prerequisite(models.Model):
	'''
	Model for a Prerequisite.

	A prerequsite is a quiz that must be "passed" before being able 
	to submit the quiz. If a quiz is hidden, the prerequisites must 
	also be met before being able to view the quiz. It contains the 
	page being required, and a link to the quiz it belongs to

	Data Fields
	   containingQuiz = the quiz the prerequisite belongs to
		requiredQuiz = the quiz the prerequisite is requiring

	@author Evan Kleist
	'''
	containingQuiz = models.ForeignKey(Quiz, related_name='prerequisites')
	requiredQuiz = models.ForeignKey(Quiz)

	def __unicode__(self):
		'''
		Link toString in java

		@author Evan Kleist
		'''
		return u'Prerequsite on Quiz ' + unicode(self.containingQuiz)
