from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from courses.models import Course
from courses.course import renameCourse
from pages.lesson.models import Lesson
from home.views import master_rtr
from pages.lesson.lesson import *
from pages.page import getNextPage, getPrevPage
from django.contrib.auth.decorators import login_required
import urlparse
import re

'''
@author Matthew Tytel
@author Russell Mezzetta
@author Evan Kleist
@author John Hartquist
'''

@login_required
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

		if len(name) < 1:
			return master_rtr(request, 'page/lesson/edit_lesson.html', \
				            {'course_slug':course_slug,
								 'page_slug': page_slug,
								 'course':course_slug,
								 'message':'Lesson names must be non-empty',
								 'lesson':lesson, 'new':True})
	
		if saveNewLesson(request, course_slug, page_slug) == 0:
			return HttpResponseRedirect(reverse('pages.views.show_page', args=[course_slug, lesson.slug]))
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

@login_required
def edit_lesson(request, course_slug, page_slug):
	'''
	@author Russell Mezzetta
	@author John Hartquist
	This view displays the lesson editing page
	'''
	
	#common dictionary fields
	data={'course_slug':course_slug, 'page_slug':page_slug}
	lesson = Course.objects.get(slug=course_slug).pages.get(slug=page_slug)
	
	try:
		lesson = lesson.lesson
	except Lesson.DoesNotExist:
		print "OH MY! page is not a lesson???"
	data['lesson'] = lesson	

	if request.method == "POST":
		#Saves the working copy of the lesson
		if "Save" in request.POST:
			#save the content of the lesson
			data['lesson'] = saveLessonWorkingCopy(lesson, request.POST['content'])

			#check if the name changed
			if lesson.name != request.POST['lessonname']:
				ret = {}

				if page_slug == course_slug:
					ret = renameCourse(Course.objects.get(slug=course_slug), request.POST['lessonname'])
					if 'course' in ret:
						course_slug = ret['course'].slug
						saveLessonName(lesson, request.POST['lessonname'])
				else:
					ret = saveLessonName(lesson, request.POST['lessonname'])
				
				if 'message' in ret:
					data['message'] = ret['message']
				else:
					return HttpResponseRedirect(reverse('pages.views.edit_page', args=[course_slug, lesson.slug]))

			return master_rtr(request, 'page/lesson/edit_lesson.html', data)
			#return master_rtr(request, 'page/lesson/save_lesson.html', \
			#		{'course':course_slug, 'course_slug':course_slug, \
			#		 'page_slug':page_slug, 'pid':page_slug})

		#removes the lesson from the course
		elif "Remove" in request.POST:
			removeLesson(request, course_slug, page_slug)
			return master_rtr(request, 'page/lesson/remove_lesson.html', \
					{'course': course_slug, 'course_slug':course_slug, \
					 'page_slug':page_slug, 'pid':page_slug})
		
		#redirects to the move_page view
		elif "Move" in request.POST:
			return HttpResponseRedirect(reverse('pages.views.move_page', args=[course_slug, page_slug]))
		
		#Publishes the workingCopy
		elif "Publish" in request.POST:
			data['lesson'] = publishLessonChanges(lesson)
			return master_rtr(request, 'page/lesson/edit_lesson.html', data)

		#Revert the workingCopy to the published copy
		elif "Revert" in request.POST:
			data['lesson'] = revertLessonChanges(lesson)
			return master_rtr(request, 'page/lesson/edit_lesson.html', data)

	return master_rtr(request, 'page/lesson/edit_lesson.html', data)
