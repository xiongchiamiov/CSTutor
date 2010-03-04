"""
Tests for the home view.

@author James Pearson
"""

from django.test import TestCase
from django.test.client import Client
from pages.page import removePage
from pages.models import Page

class HomeTests(TestCase):
	'''
	Tests the "home" screen.

	Phase 1:  Anonymous User, with and without enrolled courses
	Phase 2:  Logged in user, with and without enrolled courses
	@author Mark Gius
	'''

	fixtures = ['HomeTests.xml']

	# these are defined in the fixture, and are also defined here to avoid
   # magic strings and numbers
	course_slug = "HomeTestsCourse"
	course_id = 100
	username = "HomeUser"
	password = "password"
	lesson_slug = "HomeTestsIndex"
	quiz_slug = "HomeTestsQuiz"

	def setUp(self):
		''' 
		Run before all tests

		Creates a clean test client before each test is run
		'''
		self.client = Client()

	def test_welcome_anonymous(self):
		'''
		Does the homepage "welcome" message behavior for an anonymous user
		
		Case no.    Inputs                    Expected
		1           url = /                   contains string "not enrolled"
		            no courses                status code of 200
		2           url = /                   contains string "enrolled in 1"
		            enrolled in a course      status code of 200
		
		@author Mark Gius
		'''
      # no courses
		response = self.client.get('/')
		self.failUnlessEqual(response.status_code, 200, \
				"Hmm, that's not good; we got a status code of %s instead." \
				% response)
		self.assertContains(response, "not enrolled")

      # enroll in a course
		self.client.post('/submit_join_course_request', \
				           {'courseid':self.course_id})

      # with course
		response = self.client.get('/')
		self.failUnlessEqual(response.status_code, 200, \
				"Hmm, that's not good; we got a status code of %s instead." \
				% response)
		self.assertContains(response, "enrolled in 1")
	
	def test_welcome_loggedin(self):
		'''
		Tests correct homepage "welcome" message behavior for logged in user

		Case no.    Inputs                    Expected
		1           url = /                   contains string "not enrolled"
		            no courses                status code of 200
		2           url = /                   contains string "enrolled in 1"
		            enrolled in a course      status code of 200

		@author Mark Gius
		'''
		# log in
		self.assertTrue(self.client.login(username=self.username, \
					                         password=self.password))
      # we're testing the same thing, so just call out to the above test
		self.test_welcome_anonymous()

	def test_last_visited_loggedin(self):
		# log in
		self.assertTrue(self.client.login(username=self.username, \
					                         password=self.password))
      # enroll in a course
		self.client.post('/submit_join_course_request', \
				           {'courseid':self.course_id})

		# visit a page
		response = self.client.get("/course/%s/page/%s/" \
				% (self.course_slug, self.lesson_slug))
		self.failUnlessEqual(response.status_code, 200, \
				"Hmm, that's not good; we got a status code of %s instead." \
				% response)

		# go back to the homepage
		response = self.client.get("/")
		self.failUnlessEqual(response.status_code, 200, \
				"Hmm, that's not good; we got a status code of %s instead." \
				% response)
		self.assertContains(response, "last viewing")
		self.assertContains(response, "/course/%s/page/%s" % \
				(self.course_slug, self.lesson_slug))

	def test_last_visited_quiz(self):
		# log in
		self.assertTrue(self.client.login(username=self.username, \
					                         password=self.password))
      # enroll in a course
		self.client.post('/submit_join_course_request', \
				           {'courseid':self.course_id})

		# visit a page
		response = self.client.get("/course/%s/page/%s/" \
				% (self.course_slug, self.quiz_slug))
		self.failUnlessEqual(response.status_code, 200, \
				"Hmm, that's not good; we got a status code of %s instead." \
				% response)

		# go back to the homepage
		response = self.client.get("/")
		self.failUnlessEqual(response.status_code, 200, \
				"Hmm, that's not good; we got a status code of %s instead." \
				% response)
		self.assertContains(response, "last viewing")
		self.assertContains(response, "/course/%s/page/%s" % \
				(self.course_slug, self.quiz_slug))

	def test_last_visited_deleted_lesson(self):
		# log in
		self.assertTrue(self.client.login(username=self.username, \
					                         password=self.password))
      # enroll in a course
		self.client.post('/submit_join_course_request', \
				           {'courseid':self.course_id})

		# visit a page
		response = self.client.get("/course/%s/page/%s/" \
				% (self.course_slug, self.lesson_slug))
		self.failUnlessEqual(response.status_code, 200, \
				"Hmm, that's not good; we got a status code of %s instead." \
				% response)

      # remove it
		removePage(Page.objects.get(slug=self.lesson_slug))

		response = self.client.get("/")
		self.failUnlessEqual(response.status_code, 200, \
				"Hmm, that's not good; we got a status code of %s instead." \
				% response)
		self.assertNotContains(response, "last viewing")
		self.assertNotContains(response, "/course/%s/page/%s" % \
				(self.course_slug, self.lesson_slug))
	
