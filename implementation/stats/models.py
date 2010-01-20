'''
Models file for the stats and related classes. 

These store and load user statistics. 
'''
from django.db import models
from users.models import User
from page.models import Quiz
from page.models import Question

# Create your models here.
class StatAnswer (models.Model):
	''' Model for a student's response to an individual quiz question.

		There should be one of these for every question in a given quiz. It is
		used to calculate the user statistics upstream. 
	'''
	student = models.ForeignKey(User)
	quiz = models.ForeignKey(Quiz)
	question = models.ForeignKey(Question)
	

	
