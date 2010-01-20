'''
Models file for course related classes

Contains the Overall "Course" class, plus the Classes that are primarily
contained within a Course, such as Page, Quiz, Lesson, and Roster.

SVN Commit Info:
$Id$
'''
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Course(models.Model):
	''' 
	Top level model for sets of lessons

	A course is a set of zero or more pages.  A course is either public or
	private, and contains a roster of authorized users.  Every course has a
	landing page. 
	'''
	slug = models.SlugField(unique = True)
	name = models.CharField(max_length = 255)

# commented out by mgius.  I think that what I've done with enrollment
# especially in connection with "related_name='roster'" will cover
# the "roster" functionality we're looking for
#class Roster(models.Model):
#	'''
#	A roster keeps track of the permissions and statistics for all associated 
#	users. A user is linked to stats and permissions.
#	'''
#	roster = models.OneToOneField()

class Enrollment(models.Model):
	''' Model for an Enrollment in a Course

		 An enrollment ties a User to a Course and manages their permissions
		 on that course.

		 In the case of a Public Course, enrollments should only be made when
		 a user needs permission beyond view.  

		 In the case of a Private course, an enrollment relationship is necessary
		 to allow the user to view the course.
	'''
	user = models.ForeignKey(User)
	course = models.ForeignKey(Course, related_name='roster')
   # removed by mgius.  I believe we were going for implied view?
   #view = models.BooleanField
	edit = models.BooleanField(default = False)
	stats = models.BooleanField(default = False)
	manage = models.BooleanField(default = False)

# remove by mgius.  This makes no sense from a database point of view to
# be a separate model.  See what I did with the enrollment model above
#class Permissions:
#	'''
#	Model for Permissions for an Enrollment
#
#	Permissions are a set of booleans that map the permissions for users. 
#	The view permission allows the user to view the course material. 
#	The edit permission allows the user to edit the course material. 
#	The stats permission allows the user to view class-wide statistics and 
#	roster. 
#	The manage permission allows the user to modify the roster and all 
#	associated permissions.
#	'''
