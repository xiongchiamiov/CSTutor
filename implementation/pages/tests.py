'''
Unit Tests for Classes in the Page module

@author Mark Gius
'''

from django.test import TestCase
from django.test.client import Client
from courses.models import Course
from pages.models import Page
from pages.page import *
from lesson.models import Lesson

class PageTests(TestCase):
	''' Unit tests and other tests on the Page class and it's related functions

		   Phase 0: Load test fixtures

         Phase 1: Unit test adding pages to a course

         Phase 2: Unit test removing pages from a course

         Phase 3: Unit test moving pages within a course

         Phase 4: Stress test by creating a tree of 10000 pages, of approx depth
                  4, and attempting add/remove operations from it

         --------------------------------------------------------
			FIXTURE:
			Contains 1 course.
			Contains 2 users: testuser1 has full permission, testuser2 has everything but edit.

         Page structure for these Phases 1-3 (from PageTests Fixture):

                             1 PageTestsIndexPage 12 
                               /       |       \   \ 
                              /        |        \   \ 
              2 PageTestsPage1 3       |         \  10 PageTestPage5 11
                                       |          \ 
                           4 PageTestsPage2 5      \ 
                                                    \ 
                                              6 PageTestPage3 9
                                                        |
                                                  7 PageTestPage4 8
	'''
	fixtures = ['PageTests']
	courseName = 'PageTestsCourse'
	user1 = "testuser1"
	password = "password"
	user2 = "testuser2"

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

	def test_insertPage(self):
		'''
		Tests adding a new page to the tree as a sibling of an existing
		page
		'''
		olderSibling = Page.objects.get(slug='PageTestsPage1')
		youngerSibling = getNextPage(olderSibling)
		newPage = Page(slug="testAddPageAsSibling", name="testAddPageAsSibling")
		insertPage(newPage, olderSibling)
		self.validateTree()

      # have to reload these
		olderSibling = Page.objects.get(id=olderSibling.id)
		youngerSibling = Page.objects.get(id=youngerSibling.id)

		self.assertEquals(getPrevPage(newPage), olderSibling)
		self.assertEquals(getNextPage(olderSibling), newPage)
		self.assertEquals(getNextPage(newPage), youngerSibling)
		self.assertEquals(getPrevPage(youngerSibling), newPage)

	def test_insertChildPage(self):
		'''
		Tests adding a new page to the tree as a child of an existing page
		'''
		parent = Page.objects.get(slug='PageTestsPage1')
		youngerUncle = getNextPage(parent)

		newPage = Page(slug="testAddPageAsChild", name="testAddPageAsChild")
		insertChildPage(newPage, parent)
		self.validateTree()

		# reload these because their contents have changed
		parent = Page.objects.get(id=parent.id)
		youngerUncle = Page.objects.get(id=youngerUncle.id)

		self.assertEquals(getPrevPage(newPage), parent)
		self.assertEquals(getNextPage(parent), newPage)
		self.assertEquals(getNextPage(newPage), youngerUncle)
		self.assertEquals(getPrevPage(youngerUncle), newPage)

	def test_removeParent(self):
		'''
		Tests removing a parent page from the tree (all child pages also deleted)
		'''
		pass
	
	def test_removeFirstChild(self):
		'''
		Tests removing the first child of a tree
		'''

		toRemovePage = Page.objects.get(slug='PageTestsPage1')
		removePage(toRemovePage)

		self.validateTree()

		parentPage = Page.objects.get(slug='PageTestsIndexPage')
		middleChild = Page.objects.get(slug='PageTestsPage2')

		self.assertEquals(getPrevPage(middleChild), parentPage)
		self.assertEquals(getNextPage(parentPage), middleChild)
	
	def test_removeMiddleChild(self):
		'''
		Tests removing the middle child of a tree
		'''
		toRemovePage = Page.objects.get(slug='PageTestsPage2')
		removePage(toRemovePage)

		self.validateTree()

		olderChild = Page.objects.get(slug='PageTestsPage1')
		youngerChild = Page.objects.get(slug='PageTestsPage3')

		self.assertEquals(getPrevPage(youngerChild), olderChild)
		self.assertEquals(getNextPage(olderChild), youngerChild)
	
	def test_removeLastChild(self):
		'''
		Tests removing the last child of a tree
		'''
		toRemovePage = Page.objects.get(slug='PageTestsPage5')
		removePage(toRemovePage)

		self.validateTree()

		parent = Page.objects.get(slug='PageTestsIndexPage')
		nephew = Page.objects.get(slug='PageTestsPage4')

		self.assertEquals(getNextPage(nephew), None)


	def test_movePage(self):
		'''
		Tests moving a page from one part of the tree to another
		
		case no.    inputs         expected output       remark
		1           page,page      ValidateTree == True
		'''
		#test that a move doesn't break page->lesson linkage
		#currently moving a page will disassociate it from its lesson or quiz
		pageToMove = Lesson.objects.get(slug='PageTestsPage5')
		newSibling = Lesson.objects.get(slug='PageTestsPage2')
		r = movePage(pageToMove, newSibling)

		#test the return of movePage
		try:
			r.lesson
		except:
			print "testMovePage page isn't a lesson"
			self.assertTrue(False)#any exception should indicate failure

		#get a new copy of pageToMove from the database and test it
		r = Page.objects.get(slug='PageTestsPage5')
		try:
			r.lesson
		except:
			self.assertTrue(False)#any exception should indicate failure
		
		self.assertTrue(True)

	def test_move_page_view(self):
		'''
		Tests the basic functionality of the move_page view
		@author Russell Mezzetta

		case    input                                                                expected output
		1       try to view move with anonymous user                                 user redirected to login
		2       try to view move with user2(no edit perm)                            page forbidden
		3       User1(has edit perm) move PageTestPage5 to sibling of PageTestPage2  Successful Move
		4       User1(has edit perm) move PageTestPage5 to be child of PageTestPage2 Successful Move
		'''
		c = Client()
		page2 = "PageTestsPage2"
		page5 = "PageTestsPage5"
		
		#check that anonymous user is redirected login
		response = c.get("/course/" + self.courseName + "/page/" + page2 + "/move/")
		self.assertRedirects(response, "/login/?next=/course/" + self.courseName + "/page/" + page2 + "/move/")
		#login as user without edit permissions
		c.post("/login/", {'username': self.user2, 'password': self.password})
		#check that user cannot view move
		response = c.get("/course/" + self.courseName + "/page/" + page2 + "/move/")
		self.assertContains(response, "User does not have edit permissions on the course", status_code = 403)
		#log this user out, then log in with user who has edit permissions
		c.post("/logout/")
		c.post("/login/", {'username': self.user1, 'password': self.password})
		#check that user can view move
		response = c.get("/course/" + self.courseName + "/page/" + page5 + "/move/")
		self.assertTemplateUsed(response, "page/move_page.html")
		
		#move testpage5 to sibling of testpage2
		response = c.post("/course/" + self.courseName + "/page/" + page5 + "/move/", {'siblingOrChild': 'sibling', 'referencePageID': page2})
		self.assertRedirects(response, "/course/" + self.courseName + "/page/" + page5 + "/edit/")

		#move testpage5 to child of testpage2
		response = c.post("/course/" + self.courseName + "/page/" + page5 + "/move/", {'siblingOrChild': 'child', 'referencePageID': page2})
		self.assertRedirects(response, "/course/" + self.courseName + "/page/" + page5 + "/edit/")

