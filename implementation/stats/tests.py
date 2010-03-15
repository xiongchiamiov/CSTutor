# vim: set noet:
'''
Unit tests for functions in the Stats module

@author Andrew J. Musselman
'''

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from courses.models import Course
from stats.models import Stat
from pages.models import Page
from stat import *

class StatsTests(TestCase):
	'''
	This class runs test for Stats functions.

	This tests the insertStat function, and the various queries that 
	get information from stats. These tests depend on the StatTest
	fixture, which provides 2 courses, 2 users, and three 10-question 
	quizzes ind addation to the initalData.xml It also includes some
	statistics objects that are organized in such a way to produce easily
	known average, min and max values. 
	
	Due to the interpreted nature of Python, every function that is used in
	the code has at least one test. This is to ensure that the user will
	never see an embarrassing syntax error.
	@author Andrew J. Musselman
	'''
	fixtures = ['StatTest']

	def setUp(self):
		'''
		Sets up the envrioment for StatsTests
		'''
		pass

	def test_addStat(self):
		'''
		Tests the add stat function.
		Inputs: The user 'fakeuser' as grabbed from the database
		        The quiz 'samplequiz' as grabbed from the database
				The course 'gene-fishers-cpe102-fall-08' from the database
				And the score of 0
		Expected output: A properly created stat object that is in the database

		@author Andrew J. Musselman
		'''
		user = User.objects.get(username = 'fakeuser')
		quiz = Page.objects.get(pk = '4') #sample quiz 
		course = Course.objects.get(pk = '1')  
		score = 0 #A score of 0 is always safe
		testStat = Stat.CreateStat(course,quiz,user,score)
		#Test to see if the returned stat is correct
		self.assertEquals(testStat.course, course)
		self.assertEquals(testStat.page , quiz)
		self.assertEquals(testStat.user , user)
		self.assertEquals(testStat.score , score)
		self.assertEquals(testStat.maxscore , 3)

		#And test the that it's in the database
		dbTestStat = Stat.objects.get(id=testStat.id)
		self.assertEquals(dbTestStat,testStat)

		#Test to see if the stat object from the DB is correct		
		self.assertEquals(dbTestStat.course, course)
		self.assertEquals(dbTestStat.page , quiz)
		self.assertEquals(dbTestStat.user , user)
		self.assertEquals(dbTestStat.score , score)
		self.assertEquals(dbTestStat.maxscore , 3)
	
	def test_removeUserStats(self):
		'''This test tests the return User stats function.
		It enters in a stat, gets it back, then removes it.
		
		Then the test confirms the test is gone
		Inputs: The user 'fakeuser' as grabbed from the database
		        The quiz 'samplequiz' as grabbed from the database
				The course 'gene-fishers-cpe102-fall-08' from the database
				And the score of 0 
				 - Thse create a stat, which we attempt to delete.
		Expected Output: None... This function tests the effect on
		the database.

		@author Andrew J. Musselman
		'''
		user = User.objects.get(username = 'fakeuser')
		#First we insert it into the database.
		quiz = Page.objects.get(pk = '4') #sample quiz 
		course = Course.objects.get(pk = '1')  
		score = 0 #A score of 0 is always safe
		testStat = Stat.CreateStat(course,quiz,user,score)

		#Make sure it's happned
		dbTestStat = Stat.objects.get(id=testStat.id)
		self.assertEquals(dbTestStat,testStat)

		#Now remove it from the database
		dropAllUserStats(user)
		try:
			Stat.objects.get(user=user)
			self.assertTrue(False)
		except Stat.DoesNotExist:
			self.assertTrue(True)


	def test_getBestCourseStats(self):
		'''
		Tests the getBestCourseStats function.
		The fixture should include a course with a pair of users and a pair
		of quizes. Each user has taken the quiz three times, so there should
		be a grand total of 6 stats in the DB (2 users * 3 tries).
		This should get the BEST score, not the latest from each try. So, it
		should return a total of 2 results.

		
		Input: The course 'testcourse1' from the database
		Expected Output: A list of stat objects that only contains
		the best results from each students for each quiz

		@author Andrew J. Musselman
		'''
		course = Course.objects.get(pk = '4')
		statsList = getBestCourseStats(course)
		#First, the list should give me only two results
		#self.assertEquals(len(statsList),2)
		# THIS TEST IS NOT FINISHED!!! FIXME
		#Test disabled, I may not even need this code. 
	
	def test_NumGetQuizBestAggregates(self):
		'''
		Tesets the getBestQuizBestAggregates. This function is supposed to 
		calculate the aggregates of the best results of each user on each
		quiz. It returns a list of dictionaries, one for each quiz, that 
		describes various aggrigates of the best user scores.

		Inputs: The course 'testcourseno1' from the database
		        (Also note that the fixture has a pair of  quizes and some 
				stats results in it)
		Expected output: Aggrigate stats for 2 quizes. (This test only tests
		                 number of aggrigate stats, not their correctness)

		@author Andrew J. Musselman
		'''
		course = Course.objects.get(pk = '4')
		aggregatesList = getQuizBestAggregates(course);
		#There there are two quiz in the test database for this course. So,
		# there should only be one element in the list.
		self.assertEquals(len(aggregatesList),2)
		

	def test_avgGetBesqQuizAggregates(self):
		'''
		Tests the getQuizBestAggregates function. This particular
		test checks the value of the returned average for each quiz.

		Inputs: The course 'testcourseno1' from the database
		        (Also note that the fixture has a pair of  quizes and some 
				stats results in it)
		Expected output: Aggrigate stats for 2 quizes. (This test tests
			the average results)

		@author Andrew J. Musselman
		'''
		course = Course.objects.get(pk = '4')
		aggregatesList = getQuizBestAggregates(course)

		#Now, we loop though the quizes 
		for aggregates in aggregatesList:
			if(aggregates['page_slug'] == 'test_class_no01_quiz'):
				#Quiz no 1, which should have an average of 10
				#Since each student in the test data has a best result of
				#10
				self.assertEquals(aggregates['result_avg'],10*100)
			elif(aggregates['page_slug'] == 'test_class_no01_quiz2'):
				#Quiz no 2, which should have an average of 5
				self.assertEquals(aggregates['result_avg'],10*100)
	

	def test_numGetBestUserAggregates(self):
		'''
		Tests the per-user aggregates function. This particular test
		checks that the proper number of results is returned

		Inputs: The course 'testcourseno1' from the database
		        (Also note that the fixture has a pair of  quizes and some 
				stats results in it. The course has 2 users)
		Expected output: Aggrigate stats for 2 users. (This test only tests
		                 number of aggrigate stats, not their correctness)

		@author Andrew J. Musselman
		'''
		course = Course.objects.get(pk = '4')
		aggregatesList = getUserBestAggregates(course) 

		#There are two users with stats results in this course.
		self.assertEquals(len(aggregatesList),2)
		

