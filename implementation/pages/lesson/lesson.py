'''
lesson.py fil for lesson related operations.

Contains operations for all lessons

@author Matthew Tytel

'''
from django.template.defaultfilters import slugify
from models import *

def CreateLesson(name):
	return Lesson(slug=slugify(name), name=name)
