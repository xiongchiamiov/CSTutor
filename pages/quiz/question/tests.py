'''
This file contains unit tests for the Question package.
Their are no views for the question package so no tests are needed.
question.py has 100% code coverage from these tests

@author Evan Kleist
'''

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from pages.quiz.models import *
from pages.quiz.question.question import *
from pages.quiz.question.models import *

class QuestionUnitTests(TestCase):
	''' 
		Unit Tests on Questions package.  Tests ensure that all Question
		related functionality works properly

		Test Fixture is described as follows
		
		USERS
		--------------------------------
		ekleist - Used as the user capable of editing course content.
		          Not actually used in the tests, but used in the creation
		          of the test fixtures
		--------------------------------

		COURSES
		--------------------------------
		QuestionUnitTests_Course - The container course for all of the used quizzes
		--------------------------------

		QUIZZES
		--------------------------------
		quiz1 - A quiz containg 1 code question and 1 multiple choice question
		quiz2 - A duplicate of quiz 1 containing 1 of each question
		--------------------------------
			
		@author Evan Kleist
	'''	
	fixtures = ['QuestionUnitTests']
	def setUp(self):
		'''
			Set up the tests

			@author Evan Kleist
		'''
		self.client = Client()
		self.courseSlug = 'QuestionUnitTests_Course'
		self.quiz1 = 'quiz1'
		self.quiz2 = 'quiz2'

	def test_removeQuestion(self):
		'''
			Test that removing a question actually removes the question from
			the database. If it was a multiple choice question, also tets that
			answers were removed

			Case no.    Input                       Expected Output          Remark
			1           multiple choice question    Question.DoesNotExist    Test removing a multiple choice question
			2				mcq.answers                 Answers.DoesNotExist     Make sure multiple choice questions were removed
			3           code question               Question.DoesNotExist    Test removing a code question
			@author Evan Kleist        
		'''
		quiz = Quiz.objects.get(slug=self.quiz2)

		# Case 1
		question = quiz.questions.get(order=2).multiplechoicequestion
		answers = question.answers.all()
		removeQuestion(question)
		try:
			question = quiz.questions.get(order=2)
			self.assertEquals(0,1, "The question wasnt actually removed")
		except Question.DoesNotExist:
			pass

		# Case 2
		for answer in question.answers.all():
			try:
				a = question.answers.get(order = answer.order)
				self.failUnlessEqual(0,1, "An answer was not deleted")
			except Answer.DoesNotExist:
				pass

		# Case 3
		question = quiz.questions.get(order = 1)
		removeQuestion(question)
		try:
			question = quiz.questions.get(order=1)
			self.assertEquals(0,1, "The question wasnt actually removed")
		except Question.DoesNotExist:
			pass

	def test_isMultipleChoiceQuestion(self):
		'''
			Test that a code question returns false and a multiple 
			choice question returns true.

			Case no.    Input                       Expected Output          Remark
			1           multiple choice question    True                     
			2           code question               False                    
			@author Evan Kleist        
		'''
		quiz = Quiz.objects.get(slug=self.quiz1)

		# Case 1
		question = quiz.questions.get(order=2)
		self.failUnlessEqual(isMultipleChoiceQuestion(question), True)

		# Case 2
		question = quiz.questions.get(order=1)
		self.failUnlessEqual(isMultipleChoiceQuestion(question), False)

	def test_isMultipleChoiceQuestion(self):
		'''
			Test that adding an answer to a code question produces no result.
			Adding an answer to a multiple choice question adds it to the end,
			as an incorrect, blank answer.

			Case no.    Input                       Expected Output          Remark
			1           multiple choice question    answer.text = ""         Test adding a multiple choice question
			                                        answer.order = last
			                                        answer.correct = False                     
			2           code question               Answer.DoesNotExist      Adding a answer to a code question has no effect
			@author Evan Kleist        
		'''
		quiz = Quiz.objects.get(slug=self.quiz1)

		# Case 1
		question = quiz.questions.get(order=2).multiplechoicequestion
		ansCount = question.answers.all().count()
		addAnswer(question)
		newAns = question.answers.get(order = ansCount + 1)
		self.failUnlessEqual(ansCount + 1, question.answers.all().count())
		self.failUnlessEqual(newAns.text, "")
		self.failUnlessEqual(newAns.correct, False)

		# Case 2
		ansCount = Answer.objects.all().count()
		question = quiz.questions.get(order=1)
		addAnswer(question)
		self.failUnlessEqual(ansCount, Answer.objects.all().count())

	def test_removeAnswer(self):
		'''
			Test that removing a answer actually removes the answer from
			the database.

			Case no.    Input      Expected Output          Remark
			1           answer     Answer.DoesNotExist      Successfully remove answer
			@author Evan Kleist        
		'''
		quiz = Quiz.objects.get(slug=self.quiz2)

		# Case 1
		question = quiz.questions.get(order=2).multiplechoicequestion
		answer = question.answers.get(order=2)
		removeAnswer(question, answer)
		try:
			answer = question.answers.get(order=2)
			self.assertEquals(0,1, "The question wasnt actually removed")
		except Answer.DoesNotExist:
			pass

	def test_reorderAnswers(self):
		'''
			Test that reordering the answers actually orders them into a valid state

			Case no.    Input      Expected Output             Remark
			1           mcq        validOrdering(answers)      Intentionally modify the answers order and make sure they get reordered properly
			@author Evan Kleist        
		'''
		quiz = Quiz.objects.get(slug=self.quiz2)

		# Case 1
		question = quiz.questions.get(order=2).multiplechoicequestion
		answer1 = question.answers.get(order=1)
		answer1.order = -10
		answer1.save()
		answer2 = question.answers.get(order=2)
		answer2.order = -10
		answer2.save()
		reorderAnswers(question)
		expectedOrder = 1
		for a in question.answers.all().order_by('order'):
			self.failUnlessEqual(expectedOrder, a.order)
			expectedOrder = expectedOrder + 1

