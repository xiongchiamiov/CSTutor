'''users/models.py This is probably going to go away as we are using django's built in user class'''

from django.db import models
from django.contrib.auth.models import User

# @author John Hartquist
# Create your models here.

# All the functionality we are looking for is completely covered by 
# contrib.auth.models.User
#class User(User):
#	''' 
#		Model for a User
#
#		A user contains a boolean determining whether or not the user has 
#		instructor permissions, a string for the username, a string for the 
#		password, and a list of Courses that the user is enrolled in.
#		Additionally, a user may provide an email address.
#	'''
