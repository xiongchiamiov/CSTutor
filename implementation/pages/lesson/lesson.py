'''
This file contains lesson related operations.

Contains helpful wrapper operations for all lessons such as saveLesson, or
saveLessonName. These are used mainly by the views for convenience and processing of user input.

@author Matthew Tytel
@author John Hartquist
@author Russell Mezzetta
'''
from django.template.defaultfilters import slugify
from pages.page import insertChildPage
from models import *
from pages.models import Page
from pages.page import removePage

def CreateLesson(name):
	'''
	Convenience function to create a lesson 
	
	Creates a lesson whose slug is a "slugified" version of the passed name.
	Does not commit the created lesson to the database

	@author Mark Gius
	'''
	return Lesson(slug=slugify(name), name=name)

def saveNewLesson(lesson_name, content, course, parent_slug):
	'''
	Saves a new lesson's content and name
	
	@author Matthew Tytel
	'''
	try:
		Lesson.objects.get(slug=slugify(lesson_name))
	except Lesson.DoesNotExist:
		lesson = CreateLesson(lesson_name)
		lesson.content = content
		lesson.workingCopy = lesson.content
		insertChildPage(lesson, Lesson.objects.get(slug=parent_slug))
		return 0
	
	return -1

def removeLesson(request, course, pid):
	'''
	Removes a lesson from the database.  Except it fucking does it wrong.

	TODO: This needs to not return 0 or -1, and it needs to use removePage
	@author John Hartquist
	'''
	if (request.method != "POST"):
		return -1
	if "confirmRemove" in request.POST:
		
		#Lesson.objects.get(slug=pid).delete()
		page = Page.objects.get(slug=pid)
		removePage(page)
		return 0

def revertLessonChanges(lesson):
	'''
	@author Russell Mezzetta
	This reverts the working copy to the published copy
	@pre lesson is a Lesson
	@post lesson'.workingCopy = lesson.content
	'''
	lesson.workingCopy = lesson.content
	lesson.save()
	return lesson

def publishLessonChanges(lesson):
	'''
	@author Russell Mezzetta
	This saves the working copy to the published copy
	@pre lesson is a Lesson
	@post lesson'.content = lesson.workingCopy
	'''
	lesson.content = lesson.workingCopy
	lesson.save()
	return lesson

def saveLessonName(lesson, newLessonName):
	'''
	@author Russell Mezzetta
	This saves the name of the lesson.
	Returns none on failure, lesson on success, 1 on invalid name
	@pre lesson is a Lesson, newLessonName is a string
	@post if newLessonName is non empty and slugify(newLessonName) is not already taken by a page in this course then: lesson.name = newLessonName and lesson.slug = slugify(newLessonName)
	'''
	#check that newLessonName has 1 or more characters
	if len(newLessonName) < 1:
		return {'message':"Name change failed: name must be non-empty"}

	#check that the newLessonName doesn't already exist in this course
	newSlug = slugify(newLessonName)

	#search the pages in the course to see if the slug is unique
	notUnique = Page.objects.filter(course=lesson.course).filter(slug=newSlug).count()
	if notUnique:
		return {'message':"Name change failed. A page with that name already exists in this course"}

	lesson.name = newLessonName
	lesson.slug = newSlug
	lesson.save()
	return {'lesson':lesson}

def saveLessonWorkingCopy(lesson, workingCopy):
	'''
	@author Russell Mezzetta
	This saves the working copy content of the lesson.
	returns the lesson
	@pre valid lesson is a Lesson, workingCopy is string
	@post input page.workingCopy = workingCopy
	'''
	lesson.workingCopy = workingCopy
	lesson.save()
	return lesson

