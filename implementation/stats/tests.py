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
		self.assertEquals(testStat.maxScore , 3)

		#And test the that it's in the database
		dbTestStat = Stat.objects.get(id=testStat.id)
		self.assertEquals(dbTestStat,testStat)

		




	
