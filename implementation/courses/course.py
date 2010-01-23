'''
course.py file for page related operations.

Contains operations for Courses

@author: Matthew Tytel

'''
from courses.models import *

def inject(Class):
	''' Decorator to Inject the function into the provided class

		 For info on how this works, consider reading 
		 http://www.linuxtopia.org/online_books/programming_books/python_programming/python_ch26.html

		 @author: Mark Gius

	'''
	def injectInner(function):
		try:
			Class.__dict__[function.__name__]
		except KeyError:
			print "Attaching " + function.__name__
			setattr(Class, function.__name__, function)
		return function
	return injectInner

@staticmethod
@inject(Course)
def CreateCourse(name, user, slug=None):
	''' Creates a new course

		 Takes in the name of the course and a user object, and an optional
		 slug string. Creates a new course, enrolls the user in the course and 
		 assigns all permissions to them.  Returns the course after saving it
		 it.  Have to save it so that enrollment gets an id to link to

		 TODO: Also needs to create a "default" landing page
	'''
	# check for empty string (or default value)
	if not slug:
		slug = slugify(name)

	newcourse = Course(name=name, slug=slug)
	newcourse.save()

	newcourse.addUser(user, True, True, True)

	return newcourse
		

@inject(Course)
def addUser(self, user, edit=False, stats=False, manage=False):
	''' Adds a User to a course 
	
	    Takes in a user, and optional boolean values for edit, stats, and
	    manage permission, in that order. Creates a new enrollment for that
	    user and permission level and adds it to the Course.  Returns the 
	    enrollment after saving it to the database
	'''
  	enrollment = Enrollment.CreateEnrollment(user, self, \
                                            edit, stats, manage)
	enrollment.save()
	return enrollment

def removePage(request):
	'''
	Removes the specified page from the specified course

	This operation returns an http response for viewing the deletion
	'''
	pass

def getPrevPage(request):
	'''
	Creates a new course with the specified parameters

	This operation returns an http response for viewing the new course
	'''
	pass

def removeCourse(request):
	'''
	Removes a specified course from existence

	This operation returns an http response for viewing the deletion of the course
	'''
	pass

def addPage(request):
	'''
	Adds a page to an existing specified Course

	This operation returns an http response for viewing the addition
	'''
	pass

def setPrivate(request):
	'''
	Set's the class to public/private depending on what is specified

	This operation returns an http response for viewing the privacy change
	'''
	pass

def search(request):
	'''
	Searches a specified class for a page

	This operation returns an http response for viewing the search results
	'''
	pass

def importCourse(request):
	'''
	Imports specified information into a Course

	This operation returns an http response for viewing the import
	'''
	pass

def exportCourse(request):
	'''
	Exports the specified Course

	This operation returns an http response with the export data
	'''
	pass


