'''
Unit Tests for Classes in the Page module
@author Mark Gius
'''

import unittest
from django.test import TestCase
from courses.models import Course
from pages.models import Page

class PageTests(unittest.TestCase):
	''' Unit tests and other tests on the Page class and it's related functions
	'''
	def setUp(self):
		''' Run before each testcase '''
		print Course.objects.all()

	def addPageAsSiblingTest(self):
	 	'''
		Tests adding a new page to the tree as a sibling of an existing
		page
		'''
		print "Why am I nt being run huh?"
		failUnlessTrue(False)

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
