'''
Unit tests for functions in the Stats module

@author Andrew J. Musselman
'''

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from courses.models import Course
from stats.models import Stat
from pages.models import Page
from stat import *

class StatsTests(TestCase):
	'''
	This class runs test for Stats functions

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
		@precondition The user and quiz must exist, 
		and the user must be enrolled in the course that has the quiz
		@precondition.
		@postcondition A new stat is added for the given data
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
	
	def test_getBestCourseStats(self):
		'''
		Tests the getBestCourseStats function.
		The fixture should include a course with a pair of users and a pair
		of quizes. Each user has taken the quiz three times, so there should
		be a grand total of 6 stats in the DB (2 users * 3 tries).
		This should get the BEST score, not the latest from each try. So, it
		should return a total of 2 results.
		@precondition The course must exist. There may or may not be any stats
		in it. (I'll test that functionality in another test).
		@postcondition The function returns a list of the best stat each user
		has posted in each quiz.
		'''
		course = Course.objects.get(pk = '4')
		statsList = getBestCourseStats(course)
		#First, the list should give me only two results
		self.assertEquals(len(statsList),2)
		# THIS TEST IS NOT FINISHED!!! FIXME
	
	def test_basicgetQuizBestAggregates(self):
		'''
		Tesets the getBestQuizBestAggregates. This function is supposed to 
		calculate the aggregates of the best results of each user on each
		quiz. It returns a list of dictionaries, one for each quiz, that 
		describes various aggrigates of the best user scores.
		'''
		course = Course.objects.get(pk = '4')
		#aggregatesList = getQuizBestAggregates(course);
		#There is only one quiz in the test database for this course. So,
		# there should only be one element in the list.
		#self.assertEquals(len(aggregatesList),1)

		#We also know that the two users have taken the quiz
		


