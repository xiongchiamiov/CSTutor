'''
lesson.py fil for lesson related operations.

Contains operations for all lessons

@author Matthew Tytel
@author John Hartquist
'''
from django.template.defaultfilters import slugify
from pages.page import insertChildPage
from models import *
from pages.models import Page

def CreateLesson(name):
	return Lesson(slug=slugify(name), name=name)

def saveLesson(request, course, pid):
	'''
	Saves an existing lesson's content and new name

	@author John Hartquist
	@author Matthew Tytel
	'''
	if request.method == "POST" and "Save" in request.POST:
		lesson = Lesson.objects.get(slug=pid)
		
		if pid != request.POST["lessonname"]:
			try:
				Lesson.objects.get(slug=slugify(request.POST["lessonname"]))
				return -1
			except Lesson.DoesNotExist:
				lesson.slug = slugify(request.POST["lessonname"])
		
		lesson.workingCopy = request.POST["content"]
		lesson.save()
		return 0
	return -1

def saveNewLesson(request, course, parent_slug):
	'''
	Saves a new lesson's content and name
	
	@author Matthew Tytel
	'''
	if request.method == "POST" and "Save" in request.POST:
		try:
			Lesson.objects.get(slug=slugify(request.POST["lessonname"]))
		except Lesson.DoesNotExist:
			lesson = CreateLesson(request.POST["lessonname"])
			lesson.content = request.POST["content"]
			insertChildPage(lesson, Lesson.objects.get(slug=parent_slug))
			return 0
	
	return -1

def removeLesson(request, course, pid):
	if (request.method != "POST"):
		return -1
	if "Remove" in request.POST:
	    Lesson.objects.get(slug=pid).delete()
	    return 0

def revertLessonChanges(lesson):
	'''
	@author Russell Mezzetta
	This reverts the working copy to the published copy
	'''
	lesson.workingCopy = lesson.content
	lesson.save()
	return lesson

def publishLessonChanges(lesson):
	'''
	@author Russell Mezzetta
	This saves the working copy to the published copy
	'''
	lesson.content = lesson.workingCopy
	lesson.save()
	return lesson

def saveLessonName(lesson, newLessonName):
	'''
	@author Russell Mezzetta
	This saves the name of the lesson.
	Returns none on failure, lesson on success, 1 on invalid name
	'''
	#check that newLessonName has 3 or more characters
	if len(newLessonName) < 3:
		return 1

	#check that the newLessonName doesn't already exist in this course
	newSlug = slugify(newLessonName)

	#search the pages in the course to see if the slug is unique
	notUnique = Page.objects.filter(course=lesson.course).filter(slug=newSlug).count()
	if notUnique:
		return None

	lesson.name = newLessonName
	lesson.slug = newSlug
	lesson.save()
	return lesson

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

