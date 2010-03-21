'''
Model file for the User Module

The Django User had pretty much all we needed. 
We added a UserLastViewed model to provide the homepage with the 
last page visited.

@author Russell Mezzetta
'''

from django.db import models
from django.contrib.auth.models import User

class UserLastViewed(models.Model):
	'''
	This model is essentially an extention of the User model
	It provides a way to save what the user was last viewing
	@author Russell Mezzetta
	'''
	user = models.ForeignKey(User, unique=True, related_name='lastviewed')
	courseSlug = models.SlugField()
	pageSlug = models.SlugField()
	#this indicates if they were editing the last page
	editBool = models.BooleanField(default=False)

