from django.shortcuts import render_to_response
from django.http import HttpResponse
#from page.models import Page
from models import Page
#from page.lesson.views import show_lesson
from lesson.views import show_lesson
from quiz.views import show_quiz
from lesson.views import edit_lesson
from quiz.views import edit_quiz
from quiz.models import Quiz
from lesson.models import Lesson
from models import Course
from django.core.exceptions import ObjectDoesNotExist
from home.views import master_rtr
from pages.page import movePage, movePageToParent

'''
Views file for page related view

Contains the show_page function

@author Evan Kleist
@author Russell Mezzetta
'''

def show_page(request, course_slug, page_slug):
	#check if the course is a real course in the database	
	try: 
		course = Course.objects.get(slug=course_slug)
	except Course.DoesNotExist:
		return HttpResponse("ERROR: BAD URL: The course: %s does not exist" % (course_slug))
	#check if the page is a real page in the database
	try:
		page = Page.objects.get(slug=page_slug)
	except Page.DoesNotExist:
		return HttpResponse("ERROR: BAD URL: The course: %s does not contain the page: %s." % (course_slug, page_slug))
	# if the course is private, I shouldn't be able to see it
	if course.private:
		try:
			e = page.course.roster.get(user=request.user)
			if not e.view:
				return master_rtr(request, 'page/lesson/denied.html', \
						            {'course':course,
										 'enrolled':True})
		except ObjectDoesNotExist:
			# user is not enrolled in this course
			return master_rtr(request, 'page/lesson/denied.html', \
					            {'course':course,
									 'enrolled':False})
	#case the page to a lesson or quiz then call show on it
	try:
		page = page.lesson
	except Lesson.DoesNotExist:
		try:
			page = page.quiz
		except Quiz.DoesNotExist:
			print "Page is neither quiz or lesson"
		return show_quiz(request, course_slug, page_slug)
	return show_lesson(request, course_slug, page_slug, page)

def edit_page(request, course_slug, page_slug):
	#check if the course is a real course in the database	
	try: 
		Course.objects.get(slug=course_slug)
	except Course.DoesNotExist:
		return HttpResponse("ERROR: BAD URL: The course: %s does not exist" % (course_slug))
	#check if the page is a real page in the database
	try:
		page = Page.objects.get(slug=page_slug)
	except Page.DoesNotExist:
		return HttpResponse("ERROR: BAD URL: The course: %s does not contain the page: %s." % (course_slug, page_slug))
	#cast the page to a lesson or quiz then call show on it
	try:
		page = page.lesson
	except Lesson.DoesNotExist:
		try:
			page = page.quiz
		except Quiz.DoesNotExist:
			return HttpResponse("ERROR: Page is neither quiz or lesson")
		return edit_quiz(request, course_slug, page_slug)
	return edit_lesson(request, course_slug, page_slug)


def move_page(request, course_slug, page_slug):
	'''
	@author Russell Mezzetta
	This view allows instructors (perms not yet enforced) to move pages around
	in a course.
	'''
	#check if the course is a real course in the database 
	data = {}
	data['course_slug'] = course_slug
	data['page_slug'] = page_slug
	try:
		data['course'] = Course.objects.get(slug=course_slug)
	except Course.DoesNotExist:
		return HttpResponse("ERROR: BAD URL: The course: %s does not exist" % (course_slug))
	#check if the page is a real page in the database
	try:
		data['page'] = Page.objects.get(slug=page_slug)
	except Page.DoesNotExist:
		return HttpResponse("ERROR: BAD URL: The course: %s does not contain the page: %s." % (course_slug, page_slug))
	#TODO CHECK USER FOR EDIT PERMISSIONS, redirect to error page if invalid user

	#save a list of all pages in the course EXCEPT the given page
	data['pagelist'] = data['course'].pages.all().exclude(slug=page_slug)

	if request.method == "POST":
		if "referencePageID" in request.POST and "siblingOrChild" in request.POST:
			#get the page specified by refPageID from the data['pagelist']
			refPage = None
			for p in data['pagelist']:
				if p.slug == request.POST['referencePageID']:
					refPage = p
					break
			#verify that the refPage was found
			if refPage == None:
				return HttpResponse("error, the previously selected page somehow is no longer in the list of pages in this course")

			if request.POST['siblingOrChild'] == "sibling":
				#from pdb import set_trace; set_trace()
				#move page to be the first sibling of refPage
				movePage(data['page'], refPage)
			else:
				#move the page to be the first child of refPage
				movePageToParent(data['page'], refPage)
			data['redirectUrl'] = "/"
			data['redirectText'] = "the home page"
			return master_rtr(request, 'redirect.html', data)
			#return master_rtr(request, 'page/move_page_success.html')

	return master_rtr(request, 'page/move_page.html', data)

