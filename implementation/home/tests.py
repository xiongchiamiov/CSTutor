"""
Tests for the home view.

@author James Pearson
"""

from django.test import TestCase
from django.test.client import Client

class HomeTests(TestCase):
	'''
	Tests the "home" screen.

	Phase 1:  Anonymous User, with and without enrolled courses
	Phase 2:  Logged in user, with and without enrolled courses
	@author Mark Gius
	'''

	fixtures = ['HomeTests.xml']

	def setUp(self):
		''' 
		Run before all tests

		Creates a clean test client before each test is run
		'''
		self.client = Client()

	def test_home_anonymous(self):
		'''
		Does the homepage behave correctly for an anonymous user
		
		Case no.    Inputs     Expected
		1           url = /    
		            no courses status code of 200
		2           url = /
		            enrolled in a course
		
		@author Mark Gius
		'''
      # no courses
		response = self.client.get('/')
		self.failUnlessEqual(response.status_code, 200, \
				"Hmm, that's not good; we got a status code of %s instead." \
				% response)
		self.assertContains(response, "not enrolled")

      # enroll in a course
		self.client.post('/submit_join_course_request', {'courseid':'100'})

      # with course
		response = self.client.get('/')
		self.failUnlessEqual(response.status_code, 200, \
				"Hmm, that's not good; we got a status code of %s instead." \
				% response)
		self.assertContains(response, "enrolled in 1")
