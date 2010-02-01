"""
This file contains tests for the courses package. 

@author Jon Inloes
"""

import unittest
from django.test.client import Client
from django.contrib.auth.models import User
from courses.models import Course
from courses.models import Enrollment
from django.test.client import Client


class CourseTests(unittest.TestCase):
	def setUp(self):
		'''
		Sets up the tests
		'''
		self.client = Client()

		userList = User.objects.all()
		courses = Course.objects.all()
		enrollments = Enrollment.objects.all()

		for user in userList:
			print user.username
		for course in courses:
			print course.slug
		for enrollment in enrollments:
			print enrollment.user.username + ' ' + enrollment.course.slug

	def testRoster(self):
		'''
		Tests that redirection to the roster page works
		'''
		slug = 'gene-fishers-cpe102-fall-08'
		response = self.client.get('/' + slug + '/roster/')
		self.failUnlessEqual(response.status_code, 200)


	def testEnrollUser(self):
		'''
		Tests enrolling a user in a course
		'''
		slug = 'gene-fishers-cpe102-fall-08'
		username = 'jinloes'

		self.client.post('/' + slug + '/roster/adduser/', {'username': username, 'command': 'add'})
		enrollment = Enrollment.objects.get(user__username__exact=username, course__slug__exact=slug)
		self.assertEquals(enrollment.user.username, username)

