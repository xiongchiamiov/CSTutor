'''
Contains operations for Courses

@author: Matthew Tytel
@author: Mark Gius

'''
from courses.models import *
from courses.enrollment import *
from pages.lesson.models import Lesson

def CreateCourse(name, user, private, slug=None):
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

	newcourse = Course(name=name, slug=slug, private=private)
	newcourse.save()

	addUser(newcourse, user, True, True, True, True)

	# Create the new landing page

	newpage = Lesson(course=newcourse, slug=slug, name=name, left=1, right=2,\
			           content="Landing page for " + slug +\
						          "<br />Your content here")
	newpage.save()

	return newcourse
		
def addUser(self, user, view = True, edit=False, stats=False, manage=False):
	''' Adds a User to a course 
	
	    Takes in a user, and optional boolean values for edit, stats, and
	    manage permission, in that order. Creates a new enrollment for that
	    user and permission level and adds it to the Course.  

		 Returns the  enrollment after saving it to the database, 
		 or None if the user was already enrolled

		 @author Mark Gius
	'''
   # test for user/course enrollment already
	try:
		Enrollment.objects.get(user=user, course=self)
	except Enrollment.DoesNotExist:
		enrollment = CreateEnrollment(user, self, \
		                              view, edit, stats, manage)
		enrollment.save()
		return enrollment
	# Enrollment already exists
	return None

def removeUser(self, user):
	'''
		Removes the specified user from the course

		@author ?
	'''
	#print 'removing a user'
	try:
		Enrollment.objects.get(user=user, course=self).delete()
	except:
		print 'remove failed'	
	return None

def remove(self):
	'''
		Removes this course and all of its pages, statistics, and enrollments
		from the database (TODO: or doesn't remove them from the database?)
	'''
	pass

def setPrivate(self):
	self.private = True
	self.save()


# Everything below here is probably supposed to be in views.py -mgius
# commented out by mgius on 2/16/10
#def removeCourse(request):
#	'''
#	Removes a specified course from existence
#
#	This operation returns an http response for viewing the deletion of the course
#	'''
#	pass
#
#
#def setPrivate(request):
#	'''
#	Set's the class to public/private depending on what is specified
#
#	This operation returns an http response for viewing the privacy change
#	'''
#	pass
#
#def search(request):
#	'''
#	Searches a specified class for a page
#
#	This operation returns an http response for viewing the search results
#	'''
#	pass
#
#def importCourse(request):
#	'''
#	Imports specified information into a Course
#
#	This operation returns an http response for viewing the import
#	'''
#	pass
#
#def exportCourse(request):
#	'''
#	Exports the specified Course
#
#	This operation returns an http response with the export data
#	'''
#	pass
