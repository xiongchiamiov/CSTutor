'''
Models file for the stats. 

These store and load user statistics.

@author Mark Guis 
@author Andrew J. Musselman
'''
from django.db import models
from django.contrib.auth.models import User
from courses.models import Course
from pages.models import Page
from pages.quiz.models import Quiz
from pages.quiz.question.models import Question

# Create your models here.

class Stat(models.Model):
	'''
	This is an individual tuple for a stat. 
    
    This stores an individual users result from a single quiz taken a sigle 
    single time. If a single user takes a quiz mutple times, it will generate
    mutple stats. 
	'''
	course = models.ForeignKey(Course, related_name='stats')
	user = models.ForeignKey(User, related_name='stats')
	page = models.ForeignKey(Page, related_name='stats')
	score = models.IntegerField()
	maxscore = models.IntegerField()
	date = models.DateTimeField(auto_now_add=True)

	@staticmethod
	def CreateStat(course, page, user, score):
		''' Create a new Stat Entry
		Creates a new entry in the stats table for the passed course, page,
		and user.  The entry is timestamped automatically. The maxscore
		is generated at the time that stat is created. This field is 
		simply the number of questions in the quiz. 

		Returns the statistic after saving it to the database.

		We assume you the page you are calling this function with is a quiz.
		It is an error to call this function with a page that isn't a quiz.
		Don't do that.
		'''
		maxscore = page.quiz.questions.count() 
		s = Stat(course=course, page=page, user=user, score=score, 
			maxscore = maxscore)
		s.save()
		return s

	def __unicode__(self):
		''' Returns the string representation of a stat for debugging. '''  
		return u'Stat for User ' + unicode(self.user) + u' and Lesson ' \
			+ unicode(self.page)
