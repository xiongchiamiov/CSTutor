from django.db import models

# Create your models here.

class User(models.Model):
	''' 
		Model for a User

		A user contains a boolean determining whether or not the user has 
		instructor permissions, a string for the username, a string for the 
		password, and a list of Courses that the user is enrolled in.
		Additionally, a user may provide an email address.
	'''
	pass
