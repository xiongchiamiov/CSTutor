'''
Unit Tests for Classes in the Page module
@author Mark Gius
'''

from django.test import TestCase
from django.test.client import Client
from courses.models import Course
from pages.models import Page
from pages.page import *

class PageTests(TestCase):
	''' Unit tests and other tests on the Page class and it's related functions
	'''
	fixtures = ['PageTests']
	courseName = 'PageTestsCourse'

	def validateTree(self):
		'''
		Verifies that the left/right indexes of the test Course are valid

		The indexes are valid if for every page in a course, all left/rights are
		unique, the lowest left is 1, and the highest right is the number
		of pages multiplied by two.

		@Post: True if all left/right indexes are unique, and the index range is
		 		 1 -> (# of pages) * 2 inclusive, otherwise False
		
		case no.    inputs           expected output    remark
		1           Valid Course     True
		2           Invalid Course   False  
		'''
		pages = Page.objects.filter(course__name=self.courseName)
		usedNumbers = set([page.left for page in pages]) |\
						  set([page.right for page in pages])

		self.assertEquals(len(pages) * 2, len(usedNumbers))
		self.assertEquals(min(usedNumbers), 1)
		self.assertEquals(max(usedNumbers), len(pages) * 2)
			
	def testAddPageAsSibling(self):
		'''
		Tests adding a new page to the tree as a sibling of an existing
		page
		'''
		olderSibling = Page.objects.get(slug='PageTestsPage1')
		newPage = Page(slug="testAddPageAsSibling", name="testAddPageAsSibling")
		insertPage(newPage, olderSibling)
		self.validateTree()
		self.assertEquals(getPrevPage(newPage), olderSibling)
		self.assertEquals(getNextPage(olderSibling), newPage)


	def testAddPageAsChild(self):
		'''
		Tests adding a new page to the tree as a child of an existing page
		'''
		self.failUnlessEqual(True, True)

	def testRemovePageTest(self):
		'''
		Tests removing a page from the tree
		'''
		self.assertTrue(True)

	def testRemoveTwoPagesTest(self):
		'''
		Tests removing several pages from the tree
		'''
		self.assertTrue(True)
