'''
Models file for course related classes

Contains the Overall "Course" class, plus the Classes that are primarily
contained within a Course, such as Page, Quiz, Lesson, and Roster.

@author Andrew Mussellman
@author Jon Inloes
@author Mark Gius
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

	@author Mark Gius
	'''
	slug = models.SlugField(unique = True)
	name = models.CharField(max_length = 255)
	private = models.BooleanField(default = False)
	
	def tableOfContents(self):
		'''
		Returns a list of tuples, representing the table of contents for this course,
		and the indentation level for each item.
	
		Violates code standard because template tags can only call arg-less
		functions

		@author Mark Gius
		'''
#		toc = []
#		pages = [p for p in self.pages.order_by('left')]
#		curPage = pages.pop(0)
#		toc.append(curPage)
#		prevPage = curPage
#		while len(pages) > 0:
#			curPage = pages.pop(0)
#			if (curPage.left == prevPage.left + 1):
#				# This page is one level down.  Append "in"
#				toc.append("in")
#				toc.append(curPage)
#			elif (curPage.left == prevPage
#
		#by new convention ignore pages with left <= 0
		pages = [p for p in self.pages.exclude(left__lte=0).order_by('left')]
		return self.tableOfContentsBuilder(pages)
	
	def tableOfContentsBuilder(self, pages):
		'''
		Recursive helper function for tableOfContents.
	
		Takes in a list of pages, an indentation level, 
		and the left and right bounds for this indentation level.
	
		This function is ganky. Improvement ideas are welcome

		Violates code standard because template tags can only call arg-less
		functions

		@author Mark Gius
		'''
		toc =	[]
	
		while len(pages) > 0:
			page = pages.pop(0)
			toc.append(page)
			if page.left != (page.right - 1):
				#print str(page) + " has children "
				# This page has children.  Get them
				childPages = []
				while len(pages) > 0 and pages[0].left < page.right:
					childPages.append(pages.pop(0))
				# now that I have the list of papes, recursive call on it
				toc.append("in")
				toc.extend(self.tableOfContentsBuilder(childPages))
				toc.append("out")
	
		return toc

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

		@author Mark Gius
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

	lastAction = models.DateTimeField(auto_now=True)
	
	def __unicode__(self):
		return unicode(self.user) + u' in ' + unicode(self.course)
