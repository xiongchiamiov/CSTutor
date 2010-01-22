'''
Models file for course related classes

Contains the Overall "Course" class, plus the Classes that are primarily
contained within a Course, such as Page, Quiz, Lesson, and Roster.

SVN Commit Info:
$Id$
'''
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

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
	
	def __unicode__(self):
		''' Returns the Course's name.'''
		return self.name

	@staticmethod
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

	@staticmethod
	def CreateEnrollment(user, course, \
	                     edit=False, stats=False, manage=False):
		''' Creates a new Enrollment in a course

			 Takes in a user, course, and the three permission bits and
			 sets returns an unsaved enrollment object.
		'''
		return Enrollment(user=user, course=course, \
		                  edit=edit, stats=stats, manage=manage)
