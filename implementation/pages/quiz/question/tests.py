'''
This file contains tests for the Question package. 

@author Evan Kleist
'''

import unittest
from django.test.client import Client
from django.contrib.auth.models import User

class QuestionTests(unittest.TestCase):
	''' 
		Unit Tests on Quiz Views.  Tests ensure that all Question
		related functionality works properly
		@author Evan Kleist
	'''	
	def setUp(self):
		'''
			Set up the tests

			@author Evan Kleist
		'''
		#TODO - Instead of using a known quiz page, create a quiz 
		#	page here and test on that page
		self.client = Client()

