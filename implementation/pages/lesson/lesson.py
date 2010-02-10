'''
lesson.py fil for lesson related operations.

Contains operations for all lessons

@author Matthew Tytel
@author John Hartquist
'''
from django.template.defaultfilters import slugify
from pages.page import insertChildPage
from models import *

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
		
		lesson.content = request.POST["content"]
		lesson.save()
		return 0
	return -1

def saveNewLesson(request, course, pid):
	'''
	Saves a new lesson's content and name
	
	@author Matthew Tytel
	'''
	if request.method == "POST" and "Save" in request.POST:
		try:
			Lesson.objects.get(slug=slugify(request.POST["lessonname"]))
		except Lesson.DoesNotExist:
			lesson = CreateLesson(slugify(request.POST["lessonname"]))
			lesson.content = request.POST["content"]
			insertChildPage(lesson, Lesson.objects.get(slug='forloops'))
			return 0
	
	return -1

def removeLesson(request, course, pid):
	if (request.method != "POST"):
		return -1
	if "Remove" in request.POST:
	    Lesson.objects.get(slug=pid).delete()
	    return 0
