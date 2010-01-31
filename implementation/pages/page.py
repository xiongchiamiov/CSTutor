'''
page.py file for page related operations.

Contains operations for all pages

@author Matthew Tytel
@author Mark Gius

'''
from models import *

def getNextPage(self):
	'''
	Gets the next page in the preorder traversal of the page hierarchy

	Returns the page object that is the "next" page
	'''
   # This returns the first object whose left is greater than mine, in my course
   # however it does this at the database level
	return Page.objects.filter(course__eq=self.course)\
	                   .filter(left__gt=self.left)[:1]
   # return Page.objects.get(nextPage=self)

def getPrevPage(self):
	'''
	Gets the previous page in the preorder traversal of the page heirarchy

	Returns the page object that is the "previous" page
	'''
   # returns the first object whose left is less than mine
	return Page.objects.filter(course__exact=self.course)\
	                   .filter(left__lt=self.left)[:1]
   #return Page.objects.get(nextPage=self)

def insertPageAfterNum(self, course, insertAfterNum):
	''' Inserts a page after "num"

		 Inserting a page at "0" makes this page the "first" page

		 Inserting a page after a pages "left" makes this page the first child
		 of the insertAfterNum page.

		 Inserting a page after a pages "right" makes this page the next sibling
		 of the insertAfterNum page.

		 Those who don't want to deal with the structure of the pages should use
		 insertPage instead of this
   '''
	self.left = insertAfterNum + 1
	self.right = insertAfterNum + 2
	self.course = course
	coursePages = Page.objects.filter(course__exact=self.course)
	# These pages are later in the tree, both left and right need to be inc by 2
	updateLeft = coursePages.filter(left__gt=insertAfterNum)
	for page in updateLeft:
		page.left += 2
		page.right += 2
		page.save()
	
	# these pages are previous in the tree, but need their "right" updated
	updateRight = coursePages.filter(right__gt=insertAfterNum)\
	                         .exclude(left__gt=insertAfterNum)
	for page in updateRight:
		page.right += 2
		page.save()

	self.save()

	return self

def insertPage(self, course, insertAfter):
	''' Inserts the page self after the page insertAfter in the course course

		 This creates the page as the next sibling of the insertAfter page

		 Returns the inserted page after committing it
	'''
	return insertPageAfterNum(self, course, insertAfter.right)

def insertChildPage(self, course, parentPage):
	''' Inserts the page self as the first child of the parentPage

		 Returns the inserted page after committing it
	'''
	return insertPageAfterNum(self, course, parentPage.left)

def movePage(self, neworder, newparent = None):
	'''
	Moves the page to a new location. 

	Removes the page from its current location, and add itself back in at the
	new location with a potentially new parent.

	If no parent is specified, keep the same parent

	'''
	pass


# Everything below:q
#




def displayPage(request):
	'''
	Gets a page in the request

	This operation returns an http response for viewing the requested page
	'''
	pass


def createPage(request):
	'''
	Creates a new page with the specified parameters

	This operation returns an http response for viewing the new page
	'''
	pass
