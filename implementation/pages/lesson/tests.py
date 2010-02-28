"""
Unit tests for Lesson functions

@author Russell Mezzetta
"""

from django.test import TestCase
from models import Lesson
from pages.models import Page
from courses.models import Course
from lesson import *

class LessonTests(TestCase):
	'''
	Unit tests on some lesson specific functions
	'''

	def setUp(self):
		self.course = Course.objects.get(slug="large-testing-course")

	def test_revertLessonChanges(self):
		'''
		Tests a relatively simple function which takes a lesson and copies the
		published copy into the working copy
		'''
		l = Lesson.objects.filter(course=self.course).get(slug="testpage6")
		content = l.content
		#modify working copy to make sure it changes
		l.workingCopy = "xxx"
		r = revertLessonChanges(l)
		self.assertEquals(r.workingCopy, content)
		self.assertEquals(r.workingCopy, r.content)
	
	def test_publishLessonChanges(self):
		'''
		Tests a function which takes a lesson and copies the working copy to the
		published copy
		'''
		l = Lesson.objects.filter(course=self.course).get(slug="testpage6")
		l.workingCopy = content = "xxx"
		l.content="yyy"
		r = publishLessonChanges(l)
		self.assertEquals(r.workingCopy, content)
		self.assertEquals(r.workingCopy, r.content)

	def test_saveLessonName(self):
		'''
		Tests a function which attempts to save a lesson as a new name. It
		returns None if the name is already taken, otherwise it returns the
		lesson with the updated name/slug
		'''
		l = Lesson.objects.filter(course=self.course).get(slug="testpage6")
		#test adding a name that is too small
		r = saveLessonName(l, "")
		self.assertEquals(r,1)

		#test adding a duplicate entry
		r = saveLessonName(l, "testpage2")
		self.assertEquals(r,None)
		#test adding a valid entry
		r = saveLessonName(l, "testtestpage6")
		self.assertEquals(r.name,"testtestpage6")
		self.assertEquals(r.slug,"testtestpage6")
		#test adding small valid entries
		r = saveLessonName(l,"x")
		self.assertEquals(r.name,"x")
		self.assertEquals(r.slug,"x")
		r = saveLessonName(l, "xx")
		self.assertEquals(r.name,"xx")
		self.assertEquals(r.slug,"xx")

	def test_saveLessonWorkingCopy(self):
		'''
		Tests a simple function that saves the working copy of a lesson
		'''
		l = Lesson.objects.filter(course=self.course).get(slug="testpage6")
		r = saveLessonWorkingCopy(l, "abcd")
		self.assertEquals(r.workingCopy, "abcd")
	
