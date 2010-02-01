'''
Unit Tests for Classes in the Page module
@author Mark Gius
'''

from django.test import TestCase
from courses.models import Course
from pages.models import Page

class PageTests(TestCase):
	''' Unit tests and other tests on the Page class and it's related functions
	'''
	def setUp(self):
		''' Sets up environment for tests '''
		# Create a new course, and two pages added to it (all by hand)
		newCourse = Course(name="testCourse", slug="testCourse")
		newCourse.save()

		indexPage = Page(course=newCourse, slug="testIndexPage", \
							  name="testIndexPage", left=1, right=6)
		indexPage.save()
						
		testPage1 = Page(course=newCourse, slug="testPage1", \
						 name="testPage1", left=2, right=3)
		testPage1.save()

		testPage2 = Page(course=newCourse, slug="testPage2", \
						 name="testPage2", left=4, right=5)
		testPage2.save()
		print "List of courses"
		print newCourse.pages.all()

	def addPageAsSiblingTest(self):
	 	'''
		Tests adding a new page to the tree as a sibling of an existing
		page
		'''
		print "Why am I nt being run huh?"
		self.failUnlessTrue(False)

	def addPageAsChildTest(self):
	 	'''
		Tests adding a new page to the tree as a child of an existing page
		'''
		pass

	def removePageTest(self):
	 	'''
		Tests removing a page from the tree
		'''
		pass

	def removeTwoPagesTest(self):
	 	'''
		Tests removing several pages from the tree
		'''
		pass
