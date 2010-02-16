'''
question.py fil for quiestion related operations.

@author Evan Kleist
'''
from django.template.defaultfilters import slugify
from models import *

def removeQuestion(self):
	self.delete()
	# also need to delete all answers
	return 0

