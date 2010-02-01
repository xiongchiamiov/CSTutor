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
		slug = 'gene-fishers-cpe102-fall-08'
		# Commented out by mgius because it causes compile errors
		#response = self.client.get(slug + '/roster/')
		#self.failUnlessEqual(response.status_code, 200)

	def testEnrollUser(self):
		slug = 'gene-fishers-cpe102-fall-08'
		username = 'jinloes'

		enrollments = Enrollment.objects.all()
		for e in enrollments:
			print e.user.username + ' ' + e.course.slug	
		
		print '------------------------'

		self.client.post('/' + slug + '/roster/adduser/', {'username': username, 'command': 'add'})
		enrollments = Enrollment.objects.all()
		for e in enrollments:
			print e.user.username + ' ' + e.course.slug
		course = Course.objects.get(slug=slug)
		enrollments = course.roster.all()
		users = []
		for enrollment in enrollments:
			users.append(enrollment.user)
      #users = enrollments.enrollments.filter(user__name__exact=username)		
		#enrollment = Enrollment.objects.get(user=username, course=slug)
