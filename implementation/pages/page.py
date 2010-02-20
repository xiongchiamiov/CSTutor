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
	except KeyError:
		p = None
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

	#print "debug 2.0" + Page.objects.filter(course__exact=self.course).get(slug=self.slug).lesson.content	

	return self

def insertPage(self, insertAfter):
	''' Inserts the page self after the page insertAfter in the course course

		 This creates the page as the next sibling of the insertAfter page

		 Returns the inserted page after committing it
		 @author Mark Gius

		 @post: ValidateTree(self.course) == True

		 case no.    inputs         expected output       remark
		 1           page,page      ValidateTree == True
	'''
	return insertPageAfterNum(self, insertAfter.course, insertAfter.right)

def insertChildPage(self, parentPage):
	''' Inserts the page self as the first child of the parentPage

		 Returns the inserted page after committing it
		 @post: ValidateTree(self.course) == True
		 @author Mark Gius

		 case no.    inputs         expected output       remark
		 1           page,page      ValidateTree == True
	'''
	return insertPageAfterNum(self, parentPage.course, parentPage.left)

def removePage(self):
	''' Removes the given page from its course

		 Returns the page deleted

		 @post: ValidateTree(self.course) == True
		 @author Mark Gius

		 case no.    inputs         expected output       remark
		 1           page,page      ValidateTree == True
	'''
	coursePages = Page.objects.filter(course__exact=self.course)
	removeNumber = self.left

   # have to use list to force evaluation, otherwise the numbers won't work out
	updateLeft = list(coursePages.filter(left__gt=removeNumber))
	updateRight = list(coursePages.filter(right__gt=removeNumber)\
	                         .exclude(left__gt=removeNumber))

	# These pages are later in the tree, both left and right need to be dec by 2
	for page in updateLeft:
		page.left -= 2
		page.right -= 2
		page.save()
	
	# these pages are previous in the tree, but need their "right" updated
	for page in updateRight:
		page.right -= 2
		page.save()
	
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

	case no.    inputs         expected output       remark
	1           page,page      ValidateTree == True
	'''

	#print "debug1.0 "+Page.objects.get(slug=self.slug).lesson.content
	deletedpage = removePage(self)
	#print "debug1.1 "+Page.objects.get(slug=self.slug).lesson.content
	insertPage(self, insertAfter)
	#print "debug1.2 "+Page.objects.get(slug=self.slug).lesson.content
	return self

def movePageToParent(self, newParent):
	'''
	Moves the page to a new location.

	Moves the page from its current location to be the first child of the 
	supplied page

	returns the page moved
	@post: ValidateTree(self.course) == True
	@author Mark Gius

	case no.    inputs         expected output       remark
	1           page,page      ValidateTree == True
	'''

	deletedpage = removePage(self)
	insertChildPage(self, newParent)

	return self
