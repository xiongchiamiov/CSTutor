from django.db import models

# Create your models here.
class QuizResponse (models.Model):
	''' Model for a student's response to an individual quiz question.

		There should be one of these for every question in a given quiz. It is
		used to calculate the user statistics upstream. 
	'''
	pass

