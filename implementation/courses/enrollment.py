'''
course.py file for page related operations.

Contains operations for Courses

@author: Matthew Tytel

'''
from courses.models import *

def CreateEnrollment(user, course, \
                     edit=False, stats=False, manage=False):
	''' Creates a new Enrollment in a course

	    Takes in a user, course, and the three permission bits and
	    sets returns an unsaved enrollment object.
	'''
	return Enrollment(user=user, course=course, \
	                  edit=edit, stats=stats, manage=manage)
