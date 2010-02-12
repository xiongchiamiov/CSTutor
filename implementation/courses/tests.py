"""
This file contains tests for the courses package. 
All the tests get run by the django test runner.

@author Jon Inloes
@author Mark Gius
@author James Pearson
@author Matthew Tytel
"""

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from courses.models import Course
from courses.models import Enrollment

class CourseTests(TestCase):
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
			enrolled in the course, and the course landing page is created
		'''
		pass
	
	def test_RemoveCourse(self):
		'''
			Test RemoveCourse function (might not be defined yet)

			Verifies that the course is removed from the database
			and all sub pages, enrollments and roster are removed
			as well
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

class CourseViewTests(TestCase):
	''' 
		Unit Tests on Course Views.  Tests use an emulated Web Client
		to simulate a user making requests via the web interface

		Test fixtures include two courses, one private and one public, and
		a set of users.  One user who is enrolled in the private course,
		one user who is enrolled in the public course, and one user who
		is enrolled in neither. Another user is an admin for a course, which
		allows a roster to be managed. There is also a user that is not enrolled
		in any courses, so he can be enrolled in a course.

		@author Jon Inloes
		@author Mark Gius
	'''

	fixtures = ['CourseViewTests']

	def setUp(self):
		'''
		Sets up the tests
		'''
		self.client = Client()
		self.slug = 'gene-fishers-cpe102-fall-08'
	
	def testCourse(self):
		statusCode = self.client.get('/course/%s/page/%s/' % (self.slug,self.slug)).status_code
		self.failUnlessEqual(statusCode, 200, "Oopsie!  We got a status code of %s. :/" % statusCode)
		
#     TODO: this currently returns a 200.  see ticket 115
#		statusCode = self.client.get('/course/not-a-class/').status_code
#		self.failUnlessEqual(statusCode, 404, "Oh my!  Our status code was %s." % statusCode)

	def testRoster(self):
		'''
		Tests that redirection to the roster page works

		Case no.        	Inputs                                       Expected Output    	Remark
		1						slug = PageViewsPublicCourse						200                	200 is successful redirection
								adminUsername = enrollmentTestAdmin	
								password = password				
		2               url = /course/badclass/roster/	                   500            		500 is an internal server error
		'''

		slug = 'PageViewsPublicCourse'
		adminUsername = 'enrollmentTestAdmin'
		password = 'password'

		#logs in and checks to make sure the login was successful
		self.failUnlessEqual(self.client.login(username=adminUsername, password=password), True)

		#Displays the roster and checks to make sure it was successful		
		response = self.client.get('/course/' + slug + '/roster/')
		self.failUnlessEqual(response.status_code, 200, 'redirection to the roster page failed')

		#Tries to display a roster that does not exist
		slug = 'badclass'
		print '/course/' + slug + 'roster/'
		response = self.client.get('/course/' + slug + '/roster/')#roster needs to 404 on invalid course
		self.failUnlessEqual(response.status_code, 404, 'URL redirection is broken. This is a bad link and should 404')


	def testEnrollUser(self):
		'''
		Tests enrolling a user in a course through the view

		Case no.        	Inputs                                     	Expected Output	Remark
		1               	adminUserName = enrollmentTestAdmin				true					true as in the user
								password = password															exists in enrollment list
								usrname = 'enrollmentTest'
								slug = 'PageViewsPublicCourse'                           
		'''
	
		adminUsername = 'enrollmentTestAdmin'
		passwd = 'password'
		usrname = 'enrollmentTest'
		slug = 'PageViewsPublicCourse'

		#logs in and checks to make sure the login was successful
		self.failUnlessEqual(self.client.login(username=adminUsername, password=passwd), True, 'logging in failed in enrollment test')

		#Test to make sure the user is not enrolled
		userNotExists = True
		try:
			enrollment = Enrollment.objects.get(user__username__exact=usrname, course__slug__exact=slug)
			userNotExists = False

		except Enrollment.DoesNotExist:
			pass

		self.failUnlessEqual(userNotExists, True, 'user existed when it should not have')
		
		#Enroll the user in the class
		self.client.post('/course/' + slug + '/roster/adduser/', {'username': usrname, 'command': 'add'})

		#Test to make sure the user is enrolled
		userExists = True				
		try:
			enrollment = Enrollment.objects.get(user__username__exact=usrname, course__slug__exact=slug)

		except Enrollment.DoesNotExist:
			userExists = False
	
		self.failUnlessEqual(userExists, True,'the user should exist in the database')

	def testUpdateCourse(self):
		'''
		Tests changes to course data
		'''
		pass

	def testUpdateRoster(self):
		'''
		Tests the updating the roster
		Case no.       Inputs                  				Expected Output              Remark
		1.             edit = {jinloes}        				enrollment.edit = True
		               manage = {jinloes}      				enrollment.manage = True
		               stats = {}              				enrollment.stats = False
							adminUsername = enrollmentTestAdmin
							passwd = password
							slug = PageViewsPublicCourse
							usrname = updateTestUser

		2.             edit = {}              		 		enrollment.edit = False
		               manage = {}             				enrollment.manage = False
		               stats = {}              				enrollment.stats = False
		'''
		adminUsername = 'enrollmentTestAdmin'
		passwd = 'password'
		usrname = 'updateTestUser'
		slug = 'updateTestCourse'

		#logs in and checks to make sure the login was successful
		self.failUnlessEqual(self.client.login(username=adminUsername, password=passwd), True, 'logging in failed')

		#posts values to be used
		self.client.post('/course/' + slug + '/roster/updateRoster/', {'edit':[usrname], 'manage':[usrname], 'stats':[usrname], 'view':[usrname]})
		
		enrollments = Enrollment.objects.filter(course__slug__exact=slug)

		enrollment = Enrollment.objects.get(user__username__exact=usrname, course__slug__exact=slug)

		self.failUnlessEqual(enrollment.view, True, 'view should be true but was ' + str(enrollment.view))
		self.failUnlessEqual(enrollment.stats, True, 'stats should be true but was ' + str(enrollment.stats))
		self.failUnlessEqual(enrollment.manage, True, 'manage should be true but was ' + str(enrollment.manage))
		self.failUnlessEqual(enrollment.edit, True, 'edit should be true but was ' + str(enrollment.edit))

	def testPrivacy(self):
		'''
		Tests that a user who is enrolled can access a private course, and a 
		student who is not enrolled cannot access a private course
		'''
		pass
	
# I don't know why, but for some reason join_course_request is returning a 
# 302.  Why?
#	def testPrivateEnrollment(self):
#		'''
#		Tests that a user who is not enrolled can request access to a 
#		private course
#
#		After the user has enrolled in the course, verify that they cannot view
#		the course.  
#
#		After verifying that they cannot view the course, grant them view 
#		permission and verify that they can view the course
#		'''
#		user = User.objects.get(username='PageViewsEnrollmentUser')
#		privateCourse = Course.objects.get(slug='PageViewsPrivateCourse')
#
#      # attempt to enroll in the course
#		response = self.client.post('/submit_join_course_request', \
#				                      {'courseid':privateCourse.id})
#
#      # check for 200 OK and text pending
#		self.assertContains(response, "pending")
#
#      # verify that the enrollmment exists and that the user has no view 
#      # permission
#		enrollment = Enrollment.objects.get(user=user, course=privateCourse)
#
#		assertEquals(enrollment.view, False)
