from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from courses.models import Course
from pages.lesson.models import Lesson
from home.views import master_rtr
from pages.lesson.lesson import *
from pages.page import getNextPage, getPrevPage
import urlparse
import re

'''
@author Matthew Tytel
@author Russell Mezzetta
@author Evan Kleist
@author John Hartquist
'''

def create_lesson(request, course_slug, page_slug):
	'''
	@author Matthew Tytel

	Creates a new lesson and shows the user the edit page but
	does not save the lesson to the database
	'''
	if request.method == "POST" and "Save" in request.POST:
		name = request.POST["lessonname"].strip()
		lesson = CreateLesson(name)
		lesson.content = request.POST["content"]

		if len(name) < 3:
			return master_rtr(request, 'page/lesson/edit_lesson.html', \
				            {'course_slug':course_slug,
								 'page_slug': page_slug,
								 'course':course_slug,
								 'message':'Lesson names must be at least 3 characters',
								 'lesson':lesson, 'new':True})
	
		if saveNewLesson(request, course_slug, page_slug) == 0:
			return master_rtr(request, 'page/lesson/save_lesson.html', \
				            {'course_slug':course_slug, 
								 'page_slug': page_slug, 
								 'course':course_slug, 'pid':page_slug})
		else:
			return master_rtr(request, 'page/lesson/edit_lesson.html', \
				            {'course_slug':course_slug,
								 'page_slug': page_slug,
								 'course':course_slug,
								 'message':'A lesson with that name already exists',
								 'lesson':lesson, 'new':True})
	
	lesson = CreateLesson('')
	return master_rtr(request, 'page/lesson/edit_lesson.html', \
			{'course_slug':course_slug, \
			 'course':course_slug, \
			 'page_slug':page_slug, \
			 'pid':lesson.name, 'new':True})

def show_lesson(request, course_slug, page_slug, lessonPage):
	'''
	@author Russell Mezzetta
	This view displays a lesson to the user
	'''
  # To get lessonConent now, you need to retreieve the page from the database, cast it to a lesson, and get the "text" attribute
	#shouldn't have to try/except because previous calls should guarentee the page exists	
	
	#check request method for prev/next button
	if request.method == "POST":
		if "goToNextPage" in request.POST:
			#redirect to the next page
			nextPage = getNextPage(lessonPage)
			if nextPage != None:
				#args = [course_slug, nextPage.slug]
				return HttpResponseRedirect(reverse('pages.views.show_page', args=[course_slug, nextPage.slug]))
		if "goToPrevPage" in request.POST:
			#redirect to the prev page
			prevPage = getPrevPage(lessonPage)
			if prevPage != None:
				#args = [course_slug, prevPage.slug]
				return HttpResponseRedirect(reverse('pages.views.show_page', args=[course_slug, prevPage.slug]))
	
	content = lessonPage.content
	title = lessonPage.name
	
	return master_rtr(request, 'page/lesson/index.html', \
			{'course_slug':course_slug, 'page_slug':page_slug, 
			 'content':content, 'lesson_title':title, 'create_enabled':True})

def edit_lesson(request, course_slug, page_slug):
	'''
	@author Russell Mezzetta
	@author John Hartquist
	This view displays the lesson editing page
	'''
	print "EDIT"
	if request.method == "POST":
		if "Save" in request.POST:
			saveLesson(request, course_slug, page_slug)
			return master_rtr(request, 'page/lesson/save_lesson.html', \
					{'course':course_slug, 'course_slug':course_slug, \
					 'page_slug':page_slug, 'pid':page_slug})
		elif "Remove" in request.POST:
			removeLesson(request, course_slug, page_slug)
			return master_rtr(request, 'page/lesson/remove_lesson.html', \
					{'course': course_slug, 'course_slug':course_slug, \
					 'page_slug':page_slug, 'pid':page_slug})
		elif "Move" in request.POST:
			return HttpResponseRedirect(reverse('pages.views.move_page', args=[course_slug, page_slug]))
	
	lesson = Lesson.objects.get(slug=page_slug)
	return master_rtr(request, 'page/lesson/edit_lesson.html', \
			{'course':course_slug, 'course_slug':course_slug, \
			 'page_slug':page_slug, 'lesson':lesson})
