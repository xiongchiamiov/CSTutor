from django.db import models

# Create your models here.

class Course(models.Model):
	''' 
		A course is a set of zero or more pages.  A course is either public or
	   private, and contains a roster of authorized users.  Every course has a
	   landing page. 
	'''
	pass

class Lesson(models.Model):
	pass

class Quiz(models.Model):
	pass
