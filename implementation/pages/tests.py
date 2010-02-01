'''
Unit Tests for Classes in the Page module
@author Mark Gius
'''

import unittest
from django.test.client import Client
from courses.models import Course
from pages.models import Page

class PageTests(unittest.TestCase):
	''' Unit tests and other tests on the Page class and it's related functions
	'''
	def addPageAsSibling(self):
		'''
		Tests adding a new page to the tree as a sibling of an existing
		page
		'''
		print "Why am I nt being run huh?"
		self.assertTrue(False)

	def addPageAsChild(self):
		'''
		Tests adding a new page to the tree as a child of an existing page
		'''
		self.failUnlessEqual(False, True)

	def removePageTest(self):
		'''
		Tests removing a page from the tree
		'''
		self.assertTrue(False)

	def removeTwoPagesTest(self):
		'''
		Tests removing several pages from the tree
		'''
		self.assertTrue(False)
