'''
Unit Tests for Classes in the Page module
@author Mark Gius
'''

from django.test import TestCase
from django.test.client import Client
from courses.models import Course
from pages.models import Page

class PageTests(TestCase):
	''' Unit tests and other tests on the Page class and it's related functions
	'''
	fixtures = ['PageTests']
	def testAddPageAsSibling(self):
		'''
		Tests adding a new page to the tree as a sibling of an existing
		page
		'''
		print "Why am I nt being run huh?"
		self.assertTrue(False)

	def testAddPageAsChild(self):
		'''
		Tests adding a new page to the tree as a child of an existing page
		'''
		self.failUnlessEqual(False, True)

	def testRemovePageTest(self):
		'''
		Tests removing a page from the tree
		'''
		self.assertTrue(False)

	def testRemoveTwoPagesTest(self):
		'''
		Tests removing several pages from the tree
		'''
		self.assertTrue(False)
