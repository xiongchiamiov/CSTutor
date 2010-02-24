'''
This file contains tests for the Quiz package. 

@author Evan Kleist
'''

import unittest
from django.test.client import Client
from django.contrib.auth.models import User
from pages.quiz.models import *
from pages.quiz.quiz import *
from pages.quiz.question.models import *

class QuizUnitTests(unittest.TestCase):
	'''
		Unit Tests on backend quiz operations.

	'''
	fixtures = ['QuizUnitTests']

	def setUp(self):
		'''
			Set up the tests
		'''
		self.courseSlug = 'QuizUnitTests_Course'
		self.quizSlug1 = 'QuizUnitTests_Quiz1'
		self.quizSlug2 = 'QuizUnitTests_Quiz2'

	def test_addMultipleChoiceQuestion(self):
		'''
			Test that adding a multiple choice question to a quiz works as expected

			Case no.    Input                                     Expected Output                           Remark
			1           questionCount, newQuestionCount           questionCount + 1 == questionCount        Ensure that 1 new question has been added
			2           newQuestion.order, newQuestionCount       newQuestion.order == newQuestionCount     Ensure that the new question is the last question
			3           newQuestion.text                          newQuestion.text == "Blank Question"      Ensure that the new question is indeed a new question               
		'''
		quiz = Quiz.objects.get(slug=self.quizSlug1)
		questionCount = len(quiz.questions.all())

		# Add a question to the quiz
		newQuestion = addMultipleChoiceQuestion(quiz)

		# Case 1
		newQuestionCount = len(quiz.questions.all())
		self.failUnlessEqual(questionCount + 1, newQuestionCount)

		# Case 2
		self.failUnlessEqual(newQuestion.order, newQuestionCount)

		# Case 3
		self.failUnlessEqual(newQuestion.text, "")

	def test_addCodeQuestion(self):
		'''
			Test that adding a code question to a quiz works as expected

			Case no.    Input                                     Expected Output                           Remark
			1           questionCount, newQuestionCount           questionCount + 1 == questionCount        Ensure that 1 new question has been added
			2           newQuestion.order, newQuestionCount       newQuestion.order == newQuestionCount     Ensure that the new question is the last question
			3           newQuestion.text                          newQuestion.text == "Blank Question"      Ensure that the new question is indeed a new question               
		'''
		quiz = Quiz.objects.get(slug=self.quizSlug1)
		questionCount = len(quiz.questions.all())

		# Add a question to the quiz
		newQuestion = addCodeQuestion(quiz)

		# Case 1
		newQuestionCount = len(quiz.questions.all())
		self.failUnlessEqual(questionCount + 1, newQuestionCount)

		# Case 2
		self.failUnlessEqual(newQuestion.order, newQuestionCount)

		# Case 3
		self.failUnlessEqual(newQuestion.text, "")

	def test_removeQuiz(self):
		'''
			Test that removing a quiz actually removes it and all its associated data

			Case no.    Input          Expected Output          Remark
			1           quiz           Quiz.DoesNotExist        Make sure the quiz does not exist anymore
			2           questions      Question.DoesNotExist    Make sure all of the quizzes questions were also deleted
			3           answers        Answer.DoesNotExist      Make sure all of the answers were also deleted
		'''
		quiz = Quiz.objects.get(slug=self.quizSlug2)
		questions = quiz.questions.all()
		answers = []

		# Get all the answers
		for q in questions:
			if (isMultipleChoiceQuestion(q)):
				q = q.multiplechoicequestion
				answers.append(q.answers.all())
		
		# Delete the quiz
		removeQuiz(quiz)

		# Case 1
		try:
			Quiz.objects.get(slug=self.quizSlug2)
			self.failUnlessEqual(0, 1, "The quiz was not deleted")
		except Quiz.DoesNotExist:
			pass

		# Case 2
		for q in questions:
			try:
				quiz.objects.get(order=q.order)
				self.failUnlessEqual(0, 1, "A question still exists in the database")
			except Question.DoesNotExist:
				pass

		# Case 3
		answers = iter(answers)
		for q in questions:
			if (isMultipleChoiceQuestion(q)):
				q = q.multiplechoicequestion
				a = answers.next()
				try:
					q.answers.get(order=a.order)
					self.failUnlessEqual(0, 1, "An answer still exists in the database")
				except Answer.DoesNotExist:
					pass

	def test_reorderQuestions(self):
		'''
			Test that reoderQuestions actually does reorder the questions into a valid state

			Case no.    Input          Expected Output          Remark
			1           quiz           false                    Make sure the questions are not in order
			2           quiz           true                     Check to make sure that the questions are in a valid state
		'''
		quiz = Quiz.objects.get(slug=self.quizSlug1)
		questions = quiz.questions.all()

		# Make the questions order something arbitrary
		for q in questions:
			q.order = 0
			q.save()

		# Case 1
		self.failUnlessEqual(validateQuestionOrder(quiz), False)

		# Now reorder the questions
		reorderQuestions(quiz)

		# Case 2
		self.failUnlessEqual(validateQuestionOrder(quiz), True)

	def test_saveQuiz(self):
		'''
			Test that saveQuiz actually saves a quiz and updates all of its components

			Case no.    Input          Expected Output          Remark
			1           
			2           
		'''
		pass

	def test_saveQuiz_badData(self):
		'''
			Test that saveQuiz with bad data does not modify any of its components

			Case no.    Input          Expected Output          Remark
			1           
			2           
		'''
		pass

	def test_scoreQuiz(self):
		'''
			Test that scoreQuiz correctly returns a score for the submitted quiz

			Case no.    Input          Expected Output          Remark
			1           
			2           
		'''
		pass

	def test_validateQuestionOrder(self):
		'''
			Test that reoderQuestions actually does reorder the questions into a valid state

			Case no.    Input          Expected Output          Remark
			1           quiz           true                     Quiz with all questions in valid order
			2           quiz           false                    Quiz with first question 0, not 1
			3           quiz           false                    Quiz with duplicate ordering
			4           quiz           false                    Quiz with last question not last order
		'''
		quiz = Quiz.objects.get(slug=self.quizSlug1)
		questions = quiz.questions.all()

		# Case 1
		self.failUnlessEqual(validateQuestionOrder(quiz), True)

		# Case2
		q = quiz.questions.get(order=1)
		q.order = 0
		q.save()
		self.failUnlessEqual(validateQuestionOrder(quiz), False)
		q = quiz.questions.get(order=0)
		q.order = 1
		q.save()

		# Case 3
		q = quiz.questions.get(order=2)
		q.order = 1
		q.save()
		self.failUnlessEqual(validateQuestionOrder(quiz), False)
		q = quiz.questions.get(text="Test question 2")
		q.order = 2
		q.save()

		# Case 4
		q = quiz.questions.get(order=3)
		q.order = 99
		q.save()
		self.failUnlessEqual(validateQuestionOrder(quiz), False)
		q = quiz.questions.get(order=99)
		q.order = 3
		q.save()

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

	def testPublicQuizUrl(self):
		'''
			Test that the urls to a known public quiz page works properly

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

	def testPrivateQuizUrl(self):
		'''
			Test that the urls to a known private quiz page works properly when logged in and errors otherwise

			Case no.    Input                                                        Expected Output         Remark
			1           url = /course/courseSlug/page/quizSlug1/                     200                     302 is a found code
			2           url = /course/badCourse/page/quizSlug1/                      404                     404 is a bad link error
			3           url = /course/courseSlug/page/badQuiz/                       404                     404 is a bad link error
			4           url = /course/badCourse/page/badQuiz/                        404                     404 is a bad link error
		'''

		pass

	def testHiddenQuizUrl(self):
		'''
			Test that the urls to a known hiddeb quiz page works properly when logged in and prerequisites are satisfied and errors otherwise

			Case no.    Input                                                        Expected Output         Remark
			1           url = /course/courseSlug/page/quizSlug1/                     200                     302 is a found code
			2           url = /course/badCourse/page/quizSlug1/                      404                     404 is a bad link error
			3           url = /course/courseSlug/page/badQuiz/                       404                     404 is a bad link error
			4           url = /course/badCourse/page/badQuiz/                        404                     404 is a bad link error
		'''

		pass

	def testSubmitPublicQuizUrl(self):
		'''
			Test that the urls to submit a public quiz page works properly

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

	def testSubmitPrivateQuizUrl(self):
		'''
			Test that the urls to submit a private quiz page works properly

			Case no.    Input                                                        Expected Output         Remark
			1           url = /course/courseSlug/page/quizSlug1/submitQuiz/                200                     302 is a found code
			2           url = /course/badCourse/page/quizSlug1/submitQuiz/                 404                     404 is a bad link error
			3           url = /course/courseSlug/page/badQuiz/submitQuiz/                  404                     404 is a bad link error
			4           url = /course/badCourse/page/badQuiz/submitQuiz/                   404                     404 is a bad link error
		'''

		pass

	def testSubmitHiddenQuizUrl(self):
		'''
			Test that the urls to submit a hidden quiz page works properly

			Case no.    Input                                                        Expected Output         Remark
			1           url = /course/courseSlug/page/quizSlug1/submitQuiz/                200                     302 is a found code
			2           url = /course/badCourse/page/quizSlug1/submitQuiz/                 404                     404 is a bad link error
			3           url = /course/courseSlug/page/badQuiz/submitQuiz/                  404                     404 is a bad link error
			4           url = /course/badCourse/page/badQuiz/submitQuiz/                   404                     404 is a bad link error
		'''

		pass

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
