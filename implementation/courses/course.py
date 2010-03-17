'''
Contains operations for Courses

@author: Matthew Tytel
@author: Mark Gius

'''
from courses.models import *
from courses.enrollment import *
from pages.lesson.models import Lesson
from pages.lesson.lesson import saveLessonName
from pages.models import Page
import StringIO

def CreateCourse(name, user, private, slug=None):
	''' Creates a new course

		 Takes in the name of the course and a user object, and an optional
		 slug string. Creates a new course, enrolls the user in the course and 
		 assigns all permissions to them.  Returns the course after saving it
		 it.  Have to save it so that enrollment gets an id to link to

		 @author Mark Gius
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

def renameCourse(course, newName):
	''' 
	Renames a course

	@author Matt Tytel
	'''
	if len(newName.strip()) < 1:
		return {'message':"Name change failed: name must be non-empty"}

	#check that the newLessonName doesn't already exist in this course
	newSlug = slugify(newName)

	#search the pages in the course to see if the slug is unique
	courseExists = Course.objects.filter(slug=newSlug).count()
	if courseExists:
		return {'message':"Name change failed. A course with that name already exists"}

	pageExists = Page.objects.filter(course=course).filter(slug=newSlug).count()
	if pageExists:
		return {'message':"Name change failed. A page with that name already exists in this course"}
	
	course.name = newName
	course.slug = newSlug
	course.save()
	#also change the 'index' lesson to reflect name change
	indexPage = Lesson.objects.get(course = course, left = 1)
	ret = saveLessonName(indexPage, newName)
	if 'message' in ret:#indicates failure SHOULD NOT HAPPEN EVER
		return ret
	if 'lesson' in ret:#indicates success, should always happen
		return {'course':course, 'lesson': ret['lesson']}
	#left this in case a bozo changes saveLessonName
	return {'course':course}

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

		@author Mark Gius
		@author Jon Inloes
	'''
	#print 'removing a user'
	try:
		Enrollment.objects.get(user=user, course=self).delete()
	except:
		print 'remove failed'	
	return None

def removeCourse(course_slug):
	'''
	Removes this course and all of its pages, statistics, and enrollments
	from the database
	@pre course_slug is a string
	@post if course_slug points to a valid course, it will be removed from the database along with all related objects.

	@author Russell Mezzetta
	'''
	try:
		c = Course.objects.get(slug=course_slug)
		c.delete()
		return c
	except Course.DoesNotExist:
		return None

def setPrivate(self):
	'''
	Sets the private bit for a course

	@author Mark Gius
	'''
	self.private = True
	self.save()

def addUsersFromFile(course, files):
	'''
	Adds users from a text file to a course

	pre: none
	post: for each username in files
				enrollment.username.view = true

	@author Jon Inloes
	'''

	failedList = []
	for k,v, in files.iteritems():#request.FILES.iteritems():
		#print k, v
		infile = files[k]#request.FILES[k]

		output = StringIO.StringIO(infile.read())

		for line in output:
			name = line.strip()
			#print line.strip()
			try:
				#if the user exists add it
				user = User.objects.get(username=name)
				addUser(course, user)

			except User.DoesNotExist:
				#if the user does not exist add it to the failed list
				failedList.append(name);
				#return master_rtr(request, 'adduser/failed.html', \
				#		               {'course_slug':course_slug, \
				#		                'course': course})
					
	#print failedList

	return failedList

