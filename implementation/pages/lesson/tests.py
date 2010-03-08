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
	Unit tests on some lesson specific functions.
	These functions are tested by performing changes to lessons in the fixture
	and verifying that expected behavior results.
	
	TODO FIXTURE!!!
	'''

	def setUp(self):
		'''
		Run before each test. Gets a fresh copy of the course.
		'''
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
		self.assertEquals(r,{'message': 'Name change failed: name must be non-empty'})

		#test adding a duplicate entry
		r = saveLessonName(l, "testpage2")
		self.assertEquals(r,{'message': 'Name change failed. A page with that name already exists in this course'})
		#test adding a valid entry
		r = saveLessonName(l, "testtestpage6")
		self.assertEquals(r['lesson'].name,"testtestpage6")
		self.assertEquals(r['lesson'].slug,"testtestpage6")
		#test adding small valid entries
		r = saveLessonName(l,"x")
		self.assertEquals(r['lesson'].name,"x")
		self.assertEquals(r['lesson'].slug,"x")
		r = saveLessonName(l, "xx")
		self.assertEquals(r['lesson'].name,"xx")
		self.assertEquals(r['lesson'].slug,"xx")

	def test_saveLessonWorkingCopy(self):
		'''
		Tests a simple function that saves the working copy of a lesson
		'''
		l = Lesson.objects.filter(course=self.course).get(slug="testpage6")
		r = saveLessonWorkingCopy(l, "abcd")
		self.assertEquals(r.workingCopy, "abcd")
	
