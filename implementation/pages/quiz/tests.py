'''
This file contains tests for the Quiz package. 

@author Evan Kleist
'''

import unittest
from django.test.client import Client
from django.contrib.auth.models import User

class QuizUnitTests(unittest.TestCase):
	'''
		Unit Tests on backend quiz operations.

	'''
	fixtures = ['QuizUnitTests']

	def setUp(self):
		self.courseSlug = 'QuizUnitTests_Course'
		self.quizSlug1 = 'QuizUnitTests_Quiz1'
		self.quizSlug2 = 'QuizUnitTests_Quiz2'

	def test1(self):
		pass

class QuizViewTests(unittest.TestCase):
	''' 
		Unit Tests on Quiz Views.  Tests use an emulated Web Client
		to simulate a user making requests via the web interface

		Test fixtures include...

		@author Evan Kleist
	'''
	fixtures = ['QuizViewTests']

	def setUp(self):
		'''
			Set up the tests
		'''
		self.client = Client()
		self.courseSlug = 'QuizViewTests_Course'
		self.quizSlug1 = 'QuizViewTests_Quiz1'
		self.quizSlug2 = 'QuizViewTests_Quiz2'

	def testQuizUrl(self):
		'''
			Test that the urls to a known quiz page works properly

			Case no.    Input                                                        Expected Output         Remark
			1           url = /course/courseSlug/page/quizSlug1/                     200                     302 is a found code
			2           url = /course/badCourse/page/quizSlug1/                      404                     404 is a bad link error
			3           url = /course/courseSlug/page/badQuiz/                       404                     404 is a bad link error
			4           url = /course/badCourse/page/badQuiz/                        404                     404 is a bad link error
		'''

		# Case 1 - A good course and a good quiz should display properly		
		response = self.client.get('/course/' + self.courseSlug + '/page/' + self.quizSlug1 + '/')
		self.failUnlessEqual(response.status_code, 200)

		# Case 2 - A bad course and a good quiz should display an error
		response = self.client.get('/course/' + 'badClass' + '/page/' + self.quizSlug1 + '/')
		self.failUnlessEqual(response.status_code, 404) 

		# Case 3 - A good course and a bad quiz should display an error
		response = self.client.get('/course/' + self.courseSlug + '/page/' + 'badQuiz' + '/')
		self.failUnlessEqual(response.status_code, 404) 

		# Case 4 - A bad course and a bad quiz should display an error
		response = self.client.get('/course/' + 'badClass' + '/page/' + 'badQuiz' + '/')
		self.failUnlessEqual(response.status_code, 404) 

	def testSubmitQuizUrl(self):
		'''
			Test that the urls to submit a quiz page works properly

			Case no.    Input                                                        Expected Output         Remark
			1           url = /course/courseSlug/page/quizSlug1/submitQuiz/                200                     302 is a found code
			2           url = /course/badCourse/page/quizSlug1/submitQuiz/                 404                     404 is a bad link error
			3           url = /course/courseSlug/page/badQuiz/submitQuiz/                  404                     404 is a bad link error
			4           url = /course/badCourse/page/badQuiz/submitQuiz/                   404                     404 is a bad link error
		'''

		# Case 1 - A good course and a good quiz should display properly		
		response = self.client.get('/course/' + self.courseSlug + '/page/' + self.quizSlug1 + '/submitQuiz/')
		self.failUnlessEqual(response.status_code, 200)

		# Case 2 - A bad course and a good quiz should display an error
		response = self.client.get('/course/' + 'badClass' + '/page/' + self.quizSlug1 + '/submitQuiz/')
		self.failUnlessEqual(response.status_code, 404) 

		# Case 3 - A good course and a bad quiz should display an error
		response = self.client.get('/course/' + self.courseSlug + '/page/' + 'badQuiz' + '/submitQuiz/')
		self.failUnlessEqual(response.status_code, 404) 

		# Case 4 - A bad course and a bad quiz should display an error
		response = self.client.get('/course/' + 'badClass' + '/page/' + 'badQuiz' + '/submitQuiz/')
		self.failUnlessEqual(response.status_code, 404) 

	def testSubmitQuizUrl_BadData(self):
		'''
			Test the urls to make sure that submitting a quiz with 
			bad data is properly handeled

		'''
		pass

	def testEditQuizUrl(self):
		'''
			Test that the urls to edit a known quiz page works properly

			Case no.    Input                                                        Expected Output         Remark
			1           url = /course/courseSlug/page/quizSlug1/edit/                200                     302 is a found code
			2           url = /course/badCourse/page/quizSlug1/edit/                 404                     404 is a bad link error
			3           url = /course/courseSlug/page/badQuiz/edit/                  404                     404 is a bad link error
			4           url = /course/badCourse/page/badQuiz/edit/                   404                     404 is a bad link error
		'''

		# Case 1 - A good course and a good quiz should display properly		
		response = self.client.get('/course/' + self.courseSlug + '/page/' + self.quizSlug1 + '/edit/')
		self.failUnlessEqual(response.status_code, 200)

		# Case 2 - A bad course and a good quiz should display an error
		response = self.client.get('/course/' + 'badClass' + '/page/' + self.quizSlug1 + '/edit/')
		self.failUnlessEqual(response.status_code, 404) 

		# Case 3 - A good course and a bad quiz should display an error
		response = self.client.get('/course/' + self.courseSlug + '/page/' + 'badQuiz' + '/edit/')
		self.failUnlessEqual(response.status_code, 404) 

		# Case 4 - A bad course and a bad quiz should display an error
		response = self.client.get('/course/' + 'badClass' + '/page/' + 'badQuiz' + '/edit/')
		self.failUnlessEqual(response.status_code, 404) 
