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
	
	This fixture consists of two courses:
		testcourseprivate has none.
		testcoursepublic has a lesson and a quiz.
		Two users:
		Testuser1 has full permissions in both courses. 
		Testuser2 has no enrollments. 

	@author Russell Mezzetta
	'''
	
	fixtures = ['LessonTests']

	user1 = "usertestuser1"
	user1email = "testuser1email"
	password = "password"
	user2 = "usertestuser2"
	user2email = "testuser2email"
	private_course = "testcourseprivate"
	public_course = "testcoursepublic"
	lessonPage = "publiclesson"
	quizPage = "publicquiz"
	
	def setUp(self):
		'''
		Run before each test. Gets a fresh copy of the course.
		@author Russell Mezzetta
		'''
		self.course = Course.objects.get(slug=self.public_course)

	def test_revertLessonChanges(self):
		'''
		Tests a relatively simple function which takes a lesson and copies the
		published copy into the working copy
		
		case		input										output
		----		-----										------
		1			lesson with								lesson with
					content="public lesson content"	content="public lesson content"
					workingCopy="xxx"						workingCopy="public lesson content"

		@author Russell Mezzetta
		'''
		l = Lesson.objects.get(course=self.course, slug=self.lessonPage)
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
		
		case		input										output
		----		-----										------
		1			lesson with								lesson with
					content="yyy"							content="xxx"
					workingCopy="xxx"						workingCopy="xxx"
		
		@author Russell Mezzetta
		'''
		l = Lesson.objects.get(course=self.course, slug=self.lessonPage)
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

		case		input										output
		----		-----										------
		1			lesson with								{'message': 'Name change failed: name must be non-empty'}
					name="publiclesson"
					slug="publiclesson"
					newName=""

		2			lesson with								{'message': 'Name change failed. A page with that name already exists in this course'}
					name=lessonPage
					slug=lessonPage
					newName=quizPage

		3			lesson with								lesson with
					name=lessonPage						name="name-is-not-taken"
					slug=lessonPage						slug="name-is-not-taken"
					newName="name-is-not-taken"

		4			lesson with								lesson with
					name='name-is-not-taken'			name="x"
					slug='name-is-not-taken'			slug="x"
					newName="x"

		5			lesson with								lesson with
					name='x'									name="xx"
					slug='x'									slug="xx"
					newName="xx"

		@author Russell Mezzetta
		'''
		l = Lesson.objects.get(course=self.course, slug=self.lessonPage)
		#test adding a name that is too small
		r = saveLessonName(l, "")
		self.assertEquals(r,{'message': 'Name change failed: name must be non-empty'})

		#test adding a duplicate entry
		r = saveLessonName(l, self.quizPage)
		self.assertEquals(r,{'message': 'Name change failed. A page with that name already exists in this course'})
		#test adding a valid entry
		r = saveLessonName(l, "name-is-not-taken")
		self.assertEquals(r['lesson'].name,"name-is-not-taken")
		self.assertEquals(r['lesson'].slug,"name-is-not-taken")
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

		case		input											output
		----		-----											------
		1			lesson with									lesson with
					content="public lesson content"		content="public lesson content"
					workingCopy="public lesson content"	workingCopy="abcd"
					newWorkingCopy="abcd"

		@author Russell Mezzetta
		'''
		l = Lesson.objects.get(course=self.course, slug=self.lessonPage)
		r = saveLessonWorkingCopy(l, "abcd")
		self.assertEquals(r.workingCopy, "abcd")
	
