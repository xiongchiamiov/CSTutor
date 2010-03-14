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
	This class tests the "home" screen.
	This is accomplished by having an anonymous user and a logged in user view the homepage before and after viewing lesson and quizzes to fully test the functionality of the homepage.

	Test data includes a public course with a lesson and page, a private course,
	and a single user.

	@author Mark Gius
	'''

	fixtures = ['HomeTests.xml']

	# these are defined in the fixture, and are also defined here to avoid
   # magic strings and numbers
	course_slug = "HomeTestsCourse"
	course_id = 100
	privateCourse_id = 101
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
	
	def test_pending_course(self):
		'''
		Verifies that the homepage displays the pending courses
		@author Mark Gius

		Case no.    Inputs                    Expected
		1           url=/
		            requested entry to        private course listed as 
						 private course           enrollment pending
		'''
		# log in
		self.assertTrue(self.client.login(username=self.username, \
					                         password=self.password))

		# enroll in a private course
		self.client.post('/submit_join_course_request', \
							  {'courseid':self.privateCourse_id})

		# visit the homepage
		response = self.client.get("/")
		self.assertContains(response, "pending")

	def test_custom404(self):
		'''
		Verifies that our custom 404 handler is being called
		@author Mark Gius

		Case no.    Inputs                    Expected
		1           url=/invalidurl/          custom 404 page
		'''

		response = self.client.get("/invalidurl/")
		self.assertContains(response, "can't seem to find", status_code=404)
	
	def test_show_help(self):
		'''
		Simple test to verify that help page is loaded
		@author Mark Gius

		Case no.    Inputs                    Expected
		1           url=/help                 Help page displayed
		'''
		# visit the help page
		response = self.client.get("/help/")

		self.assertContains(response, "Help page")
