'''
This file contains tests for the Quiz package. 

@author Evan Kleist
'''

import unittest
from django.test.client import Client
from django.contrib.auth.models import User

class QuizViewTests(unittest.TestCase):
	''' 
		Unit Tests on Quiz Views.  Tests use an emulated Web Client
		to simulate a user making requests via the web interface

		@author EVan Kleist
	'''	
	def setUp(self):
		'''
			Set up the tests
		'''
		#TODO - Instead of using a known quiz page, create a quiz 
		#	page here and test on that page
		self.client = Client()

	def testQuizUrl(self):
		'''
			Test that the urls to a known quiz page works properly
		'''
		courseSlug = 'gene-fishers-cpe102-fall-08'
		quizSlug = 'samplequiz'
		response = self.client.get('/' + courseSlug + '/' + quizSlug + '/')
		self.failUnlessEqual(response.status_code, 200)

