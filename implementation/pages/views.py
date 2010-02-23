from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
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
@author James Pearson
'''

def show_page(request, course_slug, page_slug):
	'''
	This "view" does error checking to verify that the input course/page exist
	Then it checks that the user has view permissions if they are required
	Finally it invokes the lesson or quiz view depending on the type of page
	'''
	#check if the course is a real course in the database	
	try: 
		course = Course.objects.get(slug=course_slug)
	except Course.DoesNotExist:
		#return HttpResponse("ERROR: BAD URL: The course: %s does not exist" % (course_slug))
		raise Http404
	
	#check if the page is a real page in the database
	try:
		page = Page.objects.get(slug=page_slug)
	except Page.DoesNotExist:
		#return HttpResponse("ERROR: BAD URL: The course: %s does not contain the page: %s." % (course_slug, page_slug))
		raise Http404
	
	#if the course is private then check that the user is enrolled and has view permissions
	if course.private:
		try:#try to get the enrollment for this user and check view permission
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

	#cast the page to a lesson or quiz then call show on it
	try:
		page = page.lesson
	except Lesson.DoesNotExist:
		try:
			page = page.quiz
		except Quiz.DoesNotExist:
			raise Http404
		return show_quiz(request, course_slug, page_slug)
	return show_lesson(request, course_slug, page_slug, page)

def edit_page(request, course_slug, page_slug):
	'''
	This view verifies that a valid course/page pair is given, then verifies that the user has edit permissions,
	finally it calls the quiz/lesson edit view depending on what kind of page is given.
	'''
	#check if the course is a real course in the database	
	try: 
		c = Course.objects.get(slug=course_slug)
	except Course.DoesNotExist:
		raise Http404
	#check if the page is a real page in the database
	try:
		page = c.pages.get(slug=page_slug)
	except Page.DoesNotExist:
		raise Http404

	#check that user has permissions (edit)
	if not request.user.is_authenticated():
		return HttpResponse("ERROR: User must be logged in to edit")
	try:
		#get user's enrollment to check permissions
		e = request.user.enrollments.get(course = c)
	except Enrollment.DoesNotExist:
		return HttpResponse("Error: User: %s is not enrolled in course: %s" % (request.user.username, c.name))
	if not e.edit:
		return HttpResponse("Error: User: %s does not have edit permissions on course: %s" % (request.user.username, c.name))

	#cast the page to a lesson or quiz then call show on it
	try:
		page = page.lesson
	except Lesson.DoesNotExist:
		try:
			page = page.quiz
		except Quiz.DoesNotExist:
			return Http404
		return edit_quiz(request, course_slug, page_slug)
	return edit_lesson(request, course_slug, page_slug)


def move_page(request, course_slug, page_slug):
	'''
	@author Russell Mezzetta
	This view allows instructors to move pages around	in a course.
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
	data['pagelist'] = data['course'].pages.all().exclude(slug=page_slug).order_by('left')

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
			
			#movePage should be passed lessons or quizzes, 
			#cast refPage and data['page'] appropriately
			p1 = data['page']
			try: #to cast to a lesson
				p1 = p1.lesson
			except Lesson.DoesNotExist:
				try: #to cast to a quiz 
					p1 = p1.quiz
				except Quiz.DoesNotExist:
					print "warning -- move_page view, page neither quiz nor lesson"

			p2 = refPage
			try: #to cast to a lesson
				p2 = p2.lesson
			except Lesson.DoesNotExist:
				try: #to cast to a quiz 
					p2 = p2.quiz
				except Quiz.DoesNotExist:
					print "warning -- move_page view, page neither quiz nor lesson"

			if request.POST['siblingOrChild'] == "sibling":
				#from pdb import set_trace; set_trace()
				#move page to be the first sibling of refPage
				movePage(p1, p2)
			else:
				#move the page to be the first child of refPage
				movePageToParent(p1, p2)

			data['redirectUrl'] = "/"
			data['redirectText'] = "the home page"
			return master_rtr(request, 'redirect.html', data)
			#return master_rtr(request, 'page/move_page_success.html')

	return master_rtr(request, 'page/move_page.html', data)
