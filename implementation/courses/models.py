'''
Models file for course related classes

Contains the Overall "Course" class, plus the Classes that are primarily
contained within a Course, such as Page, Quiz, Lesson, and Roster.

@author Andrew Mussellman
@author Jon Inloes
@author Mark Gius
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
	private = models.BooleanField(default = False)
	
	def __unicode__(self):
		''' Returns the Course's name.'''
		return self.name
	
	@models.permalink
	def get_absolute_url(self):
		return ('courses.views.view_course', [str(self.slug)])

class Enrollment(models.Model):
	''' Model for an Enrollment in a Course

		 An enrollment ties a User to a Course and manages their permissions
		 on that course.

		 In the case of a Public Course, enrollments should only be made when
		 a user needs permission beyond view.  

		 In the case of a Private course, an enrollment relationship is necessary
		 to allow the user to view the course.
	'''
	user = models.ForeignKey(User, related_name='enrollments')
	course = models.ForeignKey(Course, related_name='roster')

	#User can view the course contents 
	view = models.BooleanField(default = False)

	#Can edit the contents of the course
	edit = models.BooleanField(default = False)

	#Can view stats for all users in the givne course
	stats = models.BooleanField(default = False)
	
	#Can grant premissions on a given course
	manage = models.BooleanField(default = False)
	
	def __unicode__(self):
		return unicode(self.user) + u' in ' + unicode(self.course)
