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

		@author Evan Kleist
	'''
	courseSlug = 'gene-fishers-cpe102-fall-08'
	quizSlug = 'samplequiz'

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
			Case no.    Input                                                        Expected Output         Remark
			1           url = /course/gene-fishers-cpe102-fall-08/page/samplequiz/   200                     302 is a found code
			2           url = /course/badclass/page/badquiz/                         404                     404 is a bad link error
			3           url = /course/gene-fishers-cpe102-fall-08/page/badquiz/      404                     404 is a bad link error
			4           url = /course/badclass/page/samplequiz/                      404                     404 is a bad link error
		'''
		response = self.client.get('/course/' + self.courseSlug + '/page/' + self.quizSlug + '/')
		self.failUnlessEqual(response.status_code, 200)

	def testSubmitQuizUrl(self):
		'''
			Test that the urls to submit a known quiz page works properly
			Case no.    Input                                                        Expected Output         Remark
			1           url = /course/gene-fishers-cpe102-fall-08/page/samplequiz/   200                     302 is a found code
			2           url = /course/badclass/page/badquiz/                         404                     404 is a bad link error
			3           url = /course/gene-fishers-cpe102-fall-08/page/badquiz/      404                     404 is a bad link error
			4           url = /course/badclass/page/samplequiz/                      404                     404 is a bad link error
		'''
		response = self.client.get('/course/' + self.courseSlug + '/page/' + self.quizSlug + '/submitQuiz/')
		self.failUnlessEqual(response.status_code, 200)

	def testEditQuizUrl(self):
		'''
			Test that the urls to edit a known quiz page works properly
			Case no.    Input                                                        Expected Output         Remark
			1           url = /course/gene-fishers-cpe102-fall-08/page/samplequiz/   200                     302 is a found code
			2           url = /course/badclass/page/badquiz/                         404                     404 is a bad link error
			3           url = /course/gene-fishers-cpe102-fall-08/page/badquiz/      404                     404 is a bad link error
			4           url = /course/badclass/page/samplequiz/                      404                     404 is a bad link error
		'''

		response = self.client.get('/course/' + self.courseSlug + '/page/' + self.quizSlug + '/edit/')
		self.failUnlessEqual(response.status_code, 200)
