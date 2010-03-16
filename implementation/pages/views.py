'''
Views file for page related view

Contains the show_page function

@author Evan Kleist
@author Russell Mezzetta
@author James Pearson
'''

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
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
from django.contrib.auth.decorators import login_required
from home.views import master_rtr, custom_403, custom_404
from pages.page import movePage, movePageToParent

@login_required
def show_page_preview(request, course_slug, page_slug):
	'''
	This view allows the instructor to view the working copy as a student would 
	view the published copy.
	NOTE: only used by lesson currently, quiz could me modified to work like 
	this as well

	@author Russell Mezzetta
	'''
	return show_page(request, course_slug, page_slug, preview=True)

def show_page(request, course_slug, page_slug, preview=False):
	'''
	This "view" does error checking to verify that the input course/page exist
	Then it checks that the user has view permissions if they are required
	Finally it invokes the lesson or quiz view depending on the type of page

	@author Russell Mezzetta
	@author Evan Kleist
	'''
	#check if the course is a real course in the database	
	try: 
		course = Course.objects.get(slug=course_slug)
	except Course.DoesNotExist:
		#return HttpResponse("ERROR: BAD URL: The course: %s does not exist" % (course_slug))
		raise Http404
	
	#check if the page is a real page in the database
	try:
		page = Page.objects.get(slug=page_slug, course=course)
	except Page.DoesNotExist:
		#return HttpResponse("ERROR: BAD URL: The course: %s does not contain the page: %s." % (course_slug, page_slug))
		raise Http404
	
	#if the course is private then check that the user is enrolled and has view permissions
	if course.private:
		if not request.user.is_authenticated():
			return master_rtr(request, 'page/denied.html', {'course':course, 'enrolled':False, 'edit':False, 'loggedIn':False})
		try:#try to get the enrollment for this user and check view permission
			e = page.course.roster.get(user=request.user)
			if not e.view:
				return master_rtr(request, 'page/denied.html', {'course':course, 'enrolled':True, 'edit':False, 'loggedIn':True})
		except ObjectDoesNotExist:
			# user is not enrolled in this course
			return master_rtr(request, 'page/denied.html', {'course':course, 'enrolled':False, 'edit':False, 'loggedIn':True})

	#if preview is set to true then the user MUST have edit permissions to view
	#b/c this is viewing the working copy, also user must be logged in
	if preview == True:
		try:
			e = course.roster.get(user=request.user)
		except ObjectDoesNotExist:
			return master_rtr(request, 'page/denied.html', {'course':course_slug, 'enrolled':False, 'edit':False, 'loggedIn':True})
		#make sure user has view and edit permissions
		if not e.view or not e.edit:
			return master_rtr(request, 'page/denied.html', {'course':course_slug, 'enrolled':True, 'edit':False, 'loggedIn':True})

	#cast the page to a lesson or quiz then call show on it
	try:
		page = page.lesson
		if request.user.is_authenticated():
			#save this data to session
			request.session['lastCourseSlug'] = course_slug
			request.session['lastPageSlug'] = page_slug
			request.session['lastPageEdit'] = False
		return show_lesson(request, course_slug, page_slug, page, preview)
	except Lesson.DoesNotExist:
		try:
			page = page.quiz
			if request.user.is_authenticated():
				#save this data to session
				request.session['lastCourseSlug'] = course_slug
				request.session['lastPageSlug'] = page_slug
				request.session['lastPageEdit'] = False
			return show_quiz(request, course_slug, page_slug)
		except Quiz.DoesNotExist:
			raise Http404

@login_required
def edit_page(request, course_slug, page_slug):
	'''
	This view verifies that a valid course/page pair is given, then verifies that the user has edit permissions,
	finally it calls the quiz/lesson edit view depending on what kind of page is given.

	@author Russell Mezzetta
	@author Evan Kleist
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
		return master_rtr(request, 'page/denied.html', {'course':course_slug, 'enrolled':False, 'edit':True, 'loggedIn':False})
	try:
		#get user's enrollment to check permissions
		e = request.user.enrollments.get(course = c)
	except ObjectDoesNotExist:
		return master_rtr(request, 'page/denied.html', {'course':course_slug, 'enrolled':False, 'edit':True, 'loggedIn':True})
	if not e.edit:
		return master_rtr(request, 'page/denied.html', {'course':course_slug, 'enrolled':True, 'edit':True, 'loggedIn':True})
	#cast the page to a lesson or quiz then call show on it
	try:
		page = page.lesson
		#save this data to session
		request.session['lastCourseSlug'] = course_slug
		request.session['lastPageSlug'] = page_slug
		request.session['lastPageEdit'] = True
		return edit_lesson(request, course_slug, page_slug)
	except Lesson.DoesNotExist:
		try:
			page = page.quiz
			#save this data to session
			request.session['lastCourseSlug'] = course_slug
			request.session['lastPageSlug'] = page_slug
			request.session['lastPageEdit'] = True
			return edit_quiz(request, course_slug, page_slug)
		except Quiz.DoesNotExist:
			return Http404

@login_required
def move_page(request, course_slug, page_slug):
	'''
	This view allows instructors to move pages around	in a course.
	@pre request is a Request object, other two args are strings, request.user.is_authenticated()

	@author Russell Mezzetta
	'''

	#check if the course is a real course in the database 
	data = {}
	data['course_slug'] = course_slug
	data['page_slug'] = page_slug
	try:
		data['course'] = Course.objects.get(slug=course_slug)
	except Course.DoesNotExist:
		return custom_404(request, "BAD URL: The course: %s does not exist" % (course_slug))
	
	#check that user has edit permissions on the course
	try:
		e = request.user.enrollments.get(course = data['course'])
		if not e.edit:
			return custom_403(request, "User does not have edit permissions on the course")
	except ObjectDoesNotExist:
		return custom_403(request, "User is not enrolled in the course")
	
	#check if the page is a real page in the database
	try:
		data['page'] = Page.objects.get(slug=page_slug)
	except Page.DoesNotExist:
		return custom_404(request, "ERROR: BAD URL: The course: %s does not contain the page: %s." % (course_slug, page_slug))

	#check to make sure that we are not trying to move a course-page
	if data['page'].left == 1:
		return custom_404(request, "You may not move the home page of a course")

	#save a list of all pages in the course EXCEPT the given page and exclude 
	#ignored page values (left<=0 or right<=0)
	data['pagelist'] = data['course'].pages.all().exclude(slug=page_slug).exclude(left__lte=0).exclude(right__lte=0).order_by('left')

	if request.method == "POST":
		if "referencePageID" in request.POST and "siblingOrChild" in request.POST:
			#get the page specified by refPageID from the data['pagelist']
			refPage = None
			for p in data['pagelist']:
				if p.slug == request.POST['referencePageID']:
					refPage = p
					break
			#refPage should never be none....
			#if refPage == None:
			#	return HttpResponse("error, the previously selected page somehow is no longer in the list of pages in this course")
			
			#movePage should be passed lessons or quizzes, 
			#cast refPage and data['page'] appropriately
			p1 = data['page']
			try: #to cast to a lesson
				p1 = p1.lesson
			except Lesson.DoesNotExist:
				#try: #to cast to a quiz 
					p1 = p1.quiz
				#except Quiz.DoesNotExist:
				#	print "warning -- move_page view, page neither quiz nor lesson"

			p2 = refPage
			try: #to cast to a lesson
				p2 = p2.lesson
			except Lesson.DoesNotExist:
				#try: #to cast to a quiz 
					p2 = p2.quiz
				#except Quiz.DoesNotExist:
					#print "warning -- move_page view, page neither quiz nor lesson"

			if request.POST['siblingOrChild'] == "sibling":
				#move page to be the first sibling of refPage
				movePage(p1, p2)
			else:
				#move the page to be the first child of refPage
				movePageToParent(p1, p2)
			#after moving the page, redirect them to the edit view of the page
			return HttpResponseRedirect(reverse('pages.views.edit_page', args=[p1.course.slug, p1.slug]))

	return master_rtr(request, 'page/move_page.html', data)
