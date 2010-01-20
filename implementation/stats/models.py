'''
Models file for the stats and related classes. 

These store and load user statistics. 
'''
from django.db import models
from users.models import User
from courses.models import Course
from page.models import Page

# Create your models here.

class stat(models.Model):
	user = models.ForeignKey(User, related_name='stats')
	course = models.ForeignKey(Course, related_name='stats')
	lesson = models.ForeignKey(Page, related_name='stats')
	score = models.IntegerField()
	date = models.DateTimeField(auto_now_add=True)
