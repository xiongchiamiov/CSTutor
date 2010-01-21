'''
Models file for the stats and related classes. 

These store and load user statistics. 
'''
from django.db import models
from users.models import User
from courses.models import Course
from page.models import Page

# Create your models here.

class Stat(models.Model):
	course = models.ForeignKey(Course, related_name='stats')
	page = models.ForeignKey(Page, related_name='stats')
	user = models.ForeignKey(User, related_name='stats')
	score = models.IntegerField()
	date = models.DateTimeField(auto_now_add=True)

	@staticmethod
	def CreateStat(course_, page_, user_, score):
		''' Create a new Stat Entry

			 Creates a new entry in the stats table for the passed course, page,
			 and user.  The entry is timestamped automatically.

			 Returns the statistic after saving it to the database
		'''
		s = stat(course=course_, page=page_, user=user_, score=score_)
		s.save()
		return s
