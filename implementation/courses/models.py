'''
Models file for course related classes

Contains the Overall "Course" class, plus the Classes that are primarily
contained within a Course, such as Page, Quiz, Lesson, and Roster.

SVN Commit Info:
$Id$
'''
from django.db import models
from users.model import User

# Create your models here.

class Course(models.Model):
	''' 
	Top level model for sets of lessons

	A course is a set of zero or more pages.  A course is either public or
	private, and contains a roster of authorized users.  Every course has a
	landing page. 
	'''
	slug = models.SlugField(unique = True)
	name = models.CharField(maxlength = 255)

class Roster(models.Model):
	'''
	A roster keeps track of the permissions and statistics for all associated users. A user is linked to stats and permissions.
	'''
	roster = models.OneToOneField()

class Enrollment(models.Model):
	user = models.ManyToMany(User)
	permission = models.ManyToMany(Permissions)
	course = models.ForeignKey(Roster)

class Permissions:
	'''
	Model for Permissions for an Enrollment

	Permissions are a set of booleans that map the permissions for users. 
	The view permission allows the user to view the course material. 
	The edit permission allows the user to edit the course material. 
	The stats permission allows the user to view class-wide statistics and 
	roster. 
	The manage permission allows the user to modify the roster and all 
	associated permissions.
	'''
	view = models.BooleanField
	edit = models.BooleanField
	stats = models.BooleanField
	manage = models.BooleanField
