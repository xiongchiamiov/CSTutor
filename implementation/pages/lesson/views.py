
from django.shortcuts import render_to_response
from courses.models import Course
from pages.lesson.models import Lesson
from home.views import master_rtr
from pages.lesson.lesson import *
from pages.page import insertChildPage
import urlparse
import re

'''
@author Matthew Tytel
@author Russell Mezzetta
@author Evan Kleist
'''

def create_lesson(request):
	ref_url = urlparse.urlparse(request.META.get('HTTP_REFERER', ''))
	page_slug = re.search(r"/((\w|-)+)/$", ref_url.path)
	
	if page_slug is None:
		return master_rtr(request, 'lesson/create-lesson.html')
	
	parent = Lesson.objects.filter(slug=page_slug.group(1))
	if not parent:
		return master_rtr(request, 'lesson/create-lesson.html')
	#new = CreateLesson("Test")
	#insertChildPage(new, parent[0])
	return master_rtr(request, 'lesson/create-lesson.html')

def show_lesson(request, course, pid):
  # To get lessonConent now, you need to retreieve the page from the database, cast it to a lesson, and get the "text" attribute
	#shouldn't have to try/except because previous calls should guarentee the page exists	
	content = Lesson.objects.get(slug=pid).content
	return master_rtr(request, 'page/lesson/index.html', {'course':course, 'pid':pid, 'content':content})

def edit_lesson(request, course, pid):
	return master_rtr(request, 'page/lesson/edit_lesson.html', {'course':course, 'pid':pid})

