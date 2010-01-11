'''
Models file for course related classes

Contains the Overall "Course" class, plus the Classes that are primarily
contained within a Course, such as Page, Quiz, Lesson, and Roster.

SVN Commit Info:
$Id$
'''
from django.db import models

# Create your models here.

class Course(models.Model):
	''' 
	Top level model for sets of lessons

	A course is a set of zero or more pages.  A course is either public or
	private, and contains a roster of authorized users.  Every course has a
	landing page. 
	'''
	pass

class Page(models.Model):
	'''
	A single unit of a course

	A page contains links to other pages based on the Course flow.
	'''
	pass

class Lesson(Page):
	'''
	Model for a Lesson.

	A lesson is a specific type of Page.  It represents a single Topic that
	is represent on a single "Page."  Lessons can include executable code
	segments and images.
	'''
	pass

class Quiz(Page):
	'''
	Model for a Quiz.

	A quiz is a specific type of Page.  It contains a number of questions of
	various types.
	'''
	pass
