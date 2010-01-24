'''
page.py file for page related operations.

Contains operations for all pages

Author(s): Matthew Tytel

'''
from include.inject import inject, injectstatic
from Page import *

@inject(Page)
def getNextPage(self):
	'''
	Gets the next page in the preorder traversal of the page hierarchy

	Returns the page object that is the "next" page
	'''
	return Page.objects.get(prevPage=self)

@inject(Page)
def getPrevPage(self):
	'''
	Gets the previous page in the preorder traversal of the page heirarchy

	Returns the page object that is the "previous" page
	'''
	return Page.objects.get(nextPage=self)

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

