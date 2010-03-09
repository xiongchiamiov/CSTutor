'''
page.py file for page related operations.

Contains operations for all pages
The operations on page involve representing a linked structure (the page heirarchy) in a database. In order to accomplish this, we give each page a left and right integer value. These two numbers help us to create a sibling/child relationship between pages in order to construct the proper organization as seen in the navigation bar.

@author Matthew Tytel
@author Mark Gius

'''
from models import *

def getNextPage(self):
	'''
	Gets the next page in the preorder traversal of the page hierarchy

	Returns the page object that is the "next" page

	@author Mark Gius
	'''
   # This returns the first object whose left is greater than mine, in my course
   # however it does this at the database level
	try:
		p = Page.objects.filter(course__exact=self.course)\
		                .filter(left__gt=self.left).order_by('left')[0]
	except IndexError:
		p = None
	return p

def getPrevPage(self):
	'''
	Gets the previous page in the preorder traversal of the page heirarchy

	Returns the page object that is the "previous" page
	
	@author Mark Gius
	'''
   # returns the first object whose left is less than mine
	try:
  		p = Page.objects.filter(course__exact=self.course)\
	                   .filter(left__lt=self.left).order_by('-left')[0]
	# how could this happen?
	#except KeyError:
	#	p = None
	except IndexError:
		#happens if filter returns no objects which happens when called on the
		#top-most page of a course
		p = None
	return p

def insertPageAfterNum(self, course, insertAfterNum):
	''' 
	Inserts a page after "num"

	Inserting a page at "0" makes this page the "first" page

	Inserting a page after a pages "left" makes this page the first child
	of the insertAfterNum page.

	Inserting a page after a pages "right" makes this page the next sibling
	of the insertAfterNum page.

	Those who don't want to deal with the structure of the pages should use
	insertPage instead of this

	@post: ValidateTree(self.course) == True
	@author Mark Gius
   '''
	self.left = insertAfterNum + 1
	self.right = insertAfterNum + 2
	self.course = course
	coursePages = Page.objects.filter(course__exact=self.course)
	#by our new convention pages with left <= 0 will be ignored
	coursePages = coursePages.exclude(left__lte=0).exclude(right__lte=0)
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

def insertPage(self, insertAfter):
	''' Inserts the page self after the page insertAfter in the course course

		 This creates the page as the next sibling of the insertAfter page

		 Returns the inserted page after committing it
		 @author Mark Gius

		 @post: ValidateTree(self.course) == True

	'''
	return insertPageAfterNum(self, insertAfter.course, insertAfter.right)

def insertChildPage(self, parentPage):
	''' Inserts the page self as the first child of the parentPage

		 Returns the inserted page after committing it
		 @post: ValidateTree(self.course) == True
		 @author Mark Gius

	'''
	return insertPageAfterNum(self, parentPage.course, parentPage.left)

def removePage(self, actuallyDelete=True):
	''' Removes the given page from its course

		 Returns the page deleted

		 @post: ValidateTree(self.course) == True
		 @author Mark Gius

	'''
	coursePages = Page.objects.filter(course__exact=self.course)
	#by our new convention pages with left <= 0 will be ignored
	coursePages = coursePages.exclude(left__lte=0).exclude(right__lte=0)
	removeNumber = self.left

	# have to use list to force evaluation, otherwise the numbers won't work out
	children = list(coursePages.filter(left__gt=self.left).filter(right__lt=self.right))
	updateLeft = list(coursePages.filter(left__gt=removeNumber).exclude(right__lt=self.right))
	updateRight = list(coursePages.filter(right__gt=removeNumber)\
	                         .exclude(left__gt=removeNumber))

	# These are the children.  They need left and right decremented by 1
	for page in children:
		page.left -= 1
		page.right -= 1
		page.save()

	# These pages are later in the tree, both left and right need to be dec by 2
	for page in updateLeft:
		page.left -= 2
		page.right -= 2
		page.save()
	
	# these pages are previous in the tree, but need their "right" updated
	for page in updateRight:
		page.right -= 2
		page.save()
	
	if actuallyDelete == True:
		self.delete()
	return self

def movePage(self, insertAfter):
	'''
	Moves the page to a new location. 

	Moves the page from its current location to be the next sibling of the
	supplied page

	returns the page moved
	@post: ValidateTree(self.course) == True
	@author Mark Gius

	'''

	removePage(self, actuallyDelete=False)
	#set left to 0 makes this page be ignored by the insert function
	self.left = 0
	self.right = 0
	self.save()
	# force a reload of insertAfter, because it's changed in the database
	insertAfter = Page.objects.get(id=insertAfter.id)
	insertPage(self, insertAfter)
	return self

def movePageToParent(self, newParent):
	'''
	Moves the page to a new location.

	Moves the page from its current location to be the first child of the 
	supplied page

	returns the page moved
	@post: ValidateTree(self.course) == True
	@author Mark Gius

	'''

	removePage(self, actuallyDelete=False)
	#set left to 0 makes this page be ignored by the insert function
	self.left = 0
	self.right = 0
	self.save()
	# force a reload of insertAfter, because it's changed in the database
	newParent = Page.objects.get(id=newParent.id)
	insertChildPage(self, newParent)

	return self
