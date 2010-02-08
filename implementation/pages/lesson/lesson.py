'''
lesson.py fil for lesson related operations.

Contains operations for all lessons

@author Matthew Tytel
@author John Hartquist
'''
from django.template.defaultfilters import slugify
from models import *

def CreateLesson(name):
	return Lesson(slug=slugify(name), name=name)

def saveLesson(request, course, pid):
	if (request.method != "POST"):
		return -1
	if "Save" in request.POST:
		lesson = Lesson.objects.get(slug=pid)
		lesson.content = request.POST["content"]
		lesson.save()
		return 0
	return -1