"""
This file contains tests for the courses package. 

@author Jon Inloes
@author Mark Gius
"""

import unittest
from django.test.client import Client
from django.contrib.auth.models import User
from courses.models import Course
from courses.models import Enrollment
from django.test.client import Client

class CourseTests(unittest.TestCase):
	''' 
		Unit Tests on backend Course functions
		@author Mark Gius
	'''
	def setUp(self):
		'''
			Sets up environment for CourseTests
		'''
		pass

	def test_CreateCourse(self):
		'''
			Tests CreateCourse function.

			Verifies that course is created, and the specified user is
			enrolled in the course
		'''
		pass
	
	def test_addPage(self):
		'''
			Tests addPage function

			Verifies that the page is successfully added to the course
		'''
		pass

	def test_addUser(self):
		''' Tests for addUser function

			 Tests adding a user of various levels of permission levels
		'''
		pass
	
	def test_removeUser(self):
		''' 
			Tests ability to remove users from a course
		'''
		pass
	
	def test_remove(self):
		'''
			Tests function to remove a course and it's associated pages,
			enrollments, and stats from the database
		'''
		pass

class CourseViewTests(unittest.TestCase):
	''' 
		Unit Tests on Course Views.  Tests use an emulated Web Client
		to simulate a user making requests via the web interface

		@author Jon Inloes
	'''
	def setUp(self):
		'''
		Sets up the tests
		'''
		self.client = Client()

	def testRoster(self):
		'''
		Tests that redirection to the roster page works
		Case no.    Input                                        Expected Output         Remark
		1           url = /gene-fishers-cpe102-fall-08/roster/   200                     302 is a found code
		2           url = /badclass/roster/                      404                     404 is a bad link error
		'''
		slug = 'gene-fishers-cpe102-fall-08'
		
		response = self.client.get('/' + slug + '/roster/')
		self.failUnlessEqual(response.status_code, 302)


	def testEnrollUser(self):
		'''
		Tests enrolling a user in a course through the view

        Case no.        Inputs                                     Expected Output    Remark
        1               url=/gene-fishers-cpe102-fall-08/roster/
                        username = jinloes                         true               true as in the user 
                                                                                      exists in enrollment list
		'''
		slug = 'gene-fishers-cpe102-fall-08'
		username = 'jinloes'

		self.client.post('/' + slug + '/roster/adduser/', {'username': username, 'command': 'add'})
		enrollment = Enrollment.objects.get(user__username__exact=username, course__slug__exact=slug)
		self.assertEquals(enrollment.user.username, username)

	def testPrivacy(self):
		'''
		Tests that a user who is enrolled can access a private course, and a 
		student who is not enrolled cannot access a private course
		'''
