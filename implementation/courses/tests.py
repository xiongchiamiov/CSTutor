"""
This file contains tests for the courses package. 
All the tests get run by the django test runner.

@author Jon Inloes
@author Mark Gius
@author James Pearson
@author Matthew Tytel
@author John Hartquist
"""

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from courses.models import Course
from courses.models import Enrollment
from courses.course import *
from users.user import registerNewUser
from pages.lesson.lesson import saveNewLesson

class CourseTests(TestCase):
	''' 
		Unit Tests on backend Course functions
		@author Mark Gius
	'''
	def setUp(self):
		'''
			Sets up environment for CourseTests

			@author Mark Gius
		'''
		pass

	def test_CreateCourse(self):
		'''
			Tests CreateCourse function.

			Verifies that course is created, and the specified user is
			enrolled in the course, and the course landing page is created
		Case no.		Inputs								Output
		1.				New Valid Course name and		
						user						

		2.				slug = not-a-class				404

			@author Matthew Tytel
		'''
		name = "newCourse"
		registerNewUser("NewUser", "password", "password", "first", "last", "newuser@email.com")
		user = User.objects.get(username = "NewUser")
		
		course = CreateCourse(name, user, False)
		course2 = Course.objects.get(slug=course.slug)
		
		self.assertEquals(name, course.name)
		self.assertEquals(name, course2.name)
		self.assertEquals(False, course.private)
		self.assertEquals(False, course2.private)
		self.assertEquals(course.slug, course2.slug)
	
	def test_RenameCourse(self):
		'''
			Test renameCourse function

			Verifies that the course is renamed in the database

			@author Matthew Tytel
		'''
		name = "newCourse"
		newname = "newCourse2"
		dupname = "newDupCourse"
		lessname = "lessonName"

		registerNewUser("NewUser", "password", "password", "first", "last", "newuser@email.com")
		user = User.objects.get(username = "NewUser")
		
		course = CreateCourse(name, user, False)
		CreateCourse(dupname, user, False)

		ret = renameCourse(course, "")
		self.assertEquals(ret['message'], "Name change failed: name must be non-empty")

		ret = renameCourse(course, dupname)
		self.assertEquals(ret['message'], "Name change failed. A course with that name already exists")

		saveNewLesson(lessname, "content", course, course.slug)
		ret = renameCourse(course, lessname)
		self.assertEquals(ret['message'], "Name change failed. A page with that name already exists in this course")

		ret = renameCourse(course, newname)
		course2 = Course.objects.get(slug=course.slug)
		
		self.assertEquals(newname, course.name)
		self.assertEquals(newname, course2.name)
		self.assertEquals(False, course.private)
		self.assertEquals(False, course2.private)
		self.assertEquals(course.slug, course2.slug)

	def test_RemoveCourse(self):
		'''
			Test RemoveCourse function (might not be defined yet)

			Verifies that the course is removed from the database
			and all sub pages, enrollments and roster are removed
			as well

			Case			Description
			1				Test removing a page that doesn't exist
			2				Test removing an existing page
			3				Test if the page is gone

			@author Matthew Tytel
		'''
		name = "newCourse"
		
		self.assertEquals(removeCourse(slugify(name)), None)
		
		registerNewUser("NewUser", "password", "password", "first", "last", "newuser@email.com")
		user = User.objects.get(username = "NewUser")
		course = CreateCourse(name, user, False)
		
		self.assertEquals(course.name, removeCourse(slugify(name)).name)

		self.assertEquals(removeCourse(slugify(name)), None)

	def test_setPrivate(self):
		''' 
			Tests setPrivate function

			Tests if the setPrivate function will correctly set the private
			value

			@author Matthew Tytel
		'''
		pass
	
	def test_removeUser(self):
		''' 
			Tests ability to remove users from a course

			@author Mark Gius
		'''
		name = "newCourse"
		registerNewUser("NewUser", "password", "password", "first", "last", "newuser@email.com")
		user = User.objects.get(username = "NewUser")
		course = CreateCourse(name, user, False)
		
		removeUser(course, user)

		self.assertEquals(len(course.roster.all()), 0)

		removeUser(course, user)
	
class CourseViewTests(TestCase):
	''' 
		Unit Tests on Course Views.  Tests use an emulated Web Client
		to simulate a user making requests via the web interface

		Test fixtures include three courses, one private and two public, and
		a set of users.  One user, enrollmentTestAdmin, is an admin for courses, which
		allows rosters to be managed. The other users exist to test managing a roster.
		Some of these users are enrolled in courses and some are not.

		@author Jon Inloes
		@author Mark Gius
	'''

	fixtures = ['CourseViewTests']

	def setUp(self):
		'''
		Sets up the tests
		'''
		self.client = Client()
	
	def testCourse(self):
		'''
		Tests that showing a course page works.

		Case no.		Inputs								Expected Output		Remark
		1.				slug = PageViewsPublicCourse	200						

		2.				slug = not-a-class				404

		@author James Pearson
		@author Jon Inloes
		'''
		pass

	def testCourseCase1(self):
		'''
		Test case 1 for test course

		@author Jon Inloes
		'''

		slug = 'PageViewsPublicCourse'
		statusCode = self.client.get('/course/%s/page/%s/' % (slug,slug)).status_code
		self.failUnlessEqual(statusCode, 200, "Oopsie!  We got a status code of %s. :/" % statusCode)
		
	def testCourseCase2(self):
		'''
		Test case 2 for test course

		@author Jon Inloes
		'''

		slug = 'not-a-class'

		statusCode = self.client.get('/course/' + slug + '/').status_code
		self.failUnlessEqual(statusCode, 404, "Oh my!  Our status code was %s." % statusCode)

	def testShowRoster(self):
		'''
		Tests that redirection to the roster page works

		Case no.        	Inputs                                       Expected Output    		Remark
		1						slug = PageViewsPublicCourse						200                		200 is successful redirection
								adminUsername = enrollmentTestAdmin	
								password = password			
	
		2               	url = /course/badclass/roster/	            404            			404 is not found

		3						slug = 'PageViewsPublicCourse'					roster/invalid_permissions.html 
								adminUsername = 'PageViewsPublicUser'			is rendered
								password = 'password'
								template = 'roster/invalid_permissions.html'
		@author Jon Inloes		
		'''

		slug = 'PageViewsPublicCourse'
		adminUsername = 'enrollmentTestAdmin'
		password = 'password'

		#logs in and checks to make sure the login was successful
		self.failUnlessEqual(self.client.login(username=adminUsername, password=password), True)

		#Displays the roster and checks to make sure it was successful		
		response = self.client.get('/course/' + slug + '/roster/')
		self.failUnlessEqual(response.status_code, 200, 'redirection to the roster page failed')


	def testShowRosterCase2(self):
		'''
		Test show roster case 2

		@author Jon Inloes
		'''
		slug = 'PageViewsPublicCourse'
		adminUsername = 'enrollmentTestAdmin'
		password = 'password'

		#logs in and checks to make sure the login was successful
		self.failUnlessEqual(self.client.login(username=adminUsername, password=password), True)

		#Tries to display a roster that does not exist
		slug = 'badclass'

		response = self.client.get('/course/' + slug + '/roster/')
		self.failUnlessEqual(response.status_code, 404, 'URL redirection is broken. This is a bad link and should 404')

	def testShowRosterCase3(self):
		'''
		Test show roster case 3

		@author Jon Inloes
		'''
		slug = 'PageViewsPublicCourse'
		adminUsername = 'PageViewsPublicUser'
		password = 'password'
		template = 'roster/invalid_permissions.html'

		#logs in and checks to make sure the login was successful
		self.failUnlessEqual(self.client.login(username=adminUsername, password=password), True)
		

		#Displays the roster and checks to make sure it was successful		
		response = self.client.get('/course/' + slug + '/roster/')
		self.failUnlessEqual(response.status_code, 200, 'redirection to the roster page failed')

		#asserts that inval_permissions.html page was rendered because the logged in user did not have valid permission
		self.assertTemplateUsed(response, template)

	def testEnrollUser(self):
		'''
		Tests enrolling a user in a course through the view

		Case no.        	Inputs                                     	Expected Output		Remark
		1               	adminUserName = enrollmentTestAdmin				true						true as in the user
								password = password																exists in enrollment list
								username = 'enrollmentTest'
								slug = 'PageViewsPublicCourse'
		
		2						adminUserName = enrollmentTestAdmin				adduser/failed.html 
								password	= password									is rendered
								username = 'fakeUser'
								slug = 'PageViewsPublicCourse'
								template = 'adduser/failed.html'

		3						adminUserName = enrollmentTestAdmin				adduser/index.html	adduser redirects to 
								password	= password									is rendered				the adduser index when
								username = 'fakeUser'															the request method
								slug = 'PageViewsPublicCourse'												is not a POST 
								template = adduser/index.html

		4						slug = 'PageViewsPublicCourse'
								adminUsername = 'PageViewsPublicUser'
								password = 'password'
								template = 'roster/invalid_permissions.html'		

		@author Jon Inloes					                          
		'''
		pass
	
	def testEnrollUserCase1(self):
		'''
		testEnrollUser Case 1

		@author Jon Inloes
		'''

		adminUsername = 'enrollmentTestAdmin'
		password = 'password'
		username = 'enrollmentTest'
		slug = 'PageViewsPublicCourse'

		#logs in and checks to make sure the login was successful
		self.failUnlessEqual(self.client.login(username=adminUsername, password=password), True, 'logging in failed in enrollment test')

		#Test to make sure the user is not enrolled
		userNotExists = True
		try:
			enrollment = Enrollment.objects.get(user__username__exact=username, course__slug__exact=slug)
			userNotExists = False

		except Enrollment.DoesNotExist:
			pass

		self.failUnlessEqual(userNotExists, True, 'user existed when it should not have')
		
		#Enroll the user in the class
		self.client.post('/course/' + slug + '/roster/adduser/', {'username': username, 'command': 'add'})

		#Test to make sure the user is enrolled
		userExists = True				
		try:
			enrollment = Enrollment.objects.get(user__username__exact=username, course__slug__exact=slug)

		except Enrollment.DoesNotExist:
			userExists = False
	
		self.failUnlessEqual(userExists, True,'the user should exist in the database')


	def testEnrollUserCase2(self):
		'''
		testEnrollUser Case 2

		@author Jon Inloes
		'''

		adminUsername = 'enrollmentTestAdmin'
		password = 'password'
		username = 'fakeUser'
		template = 'adduser/failed.html'
		slug = 'PageViewsPublicCourse'

		#logs in and checks to make sure the login was successful
		self.failUnlessEqual(self.client.login(username=adminUsername, password=password), True, 'logging in failed in enrollment test')

		#Test to make sure the user is not enrolled
		userNotExists = True
		try:
			enrollment = Enrollment.objects.get(user__username__exact=username, course__slug__exact=slug)
			userNotExists = False

		except Enrollment.DoesNotExist:
			pass

		self.failUnlessEqual(userNotExists, True, 'user existed when it should not have')

		#tries to add a user that does not exist
		response = self.client.post('/course/' + slug + '/roster/adduser/', {'username': username, 'command': 'add'})

		templates = response.template

		#asserts that failed.html page was rendered because a the username did not exist
		self.assertTemplateUsed(response, template)

	def testEnrollUserCase3(self):
		'''
		testEnrollUser Case 3

		@author Jon Inloes
		'''

		adminUsername = 'enrollmentTestAdmin'
		password = 'password'
		username = 'fakeUser'
		template = 'adduser/index.html'
		slug = 'PageViewsPublicCourse'

		#logs in and checks to make sure the login was successful
		self.failUnlessEqual(self.client.login(username=adminUsername, password=password), True, 'logging in failed in enrollment test')

		#tries to add a user that does not exist with a get
		response = self.client.get('/course/' + slug + '/roster/adduser/', {'username': username, 'command': 'add'})
	
		self.assertTemplateUsed(response, template)

	def testEnrollUserCase4(self):
		'''
		Test enroll user case 4
		
		@author Jon Inloes	
		'''
		slug = 'PageViewsPublicCourse'
		adminUsername = 'PageViewsPublicUser'
		username = 'temp'
		password = 'password'
		template = 'roster/invalid_permissions.html'

		#logs in and checks to make sure the login was successful
		self.failUnlessEqual(self.client.login(username=adminUsername, password=password), True)
		

		#tries to add a user		
		response = self.client.post('/course/' + slug + '/roster/adduser/', {'username': username, 'command': 'add'})
		self.failUnlessEqual(response.status_code, 200, 'redirection to the roster page failed')

		#asserts that invalid_permissions.html page was rendered because the logged in user did not have valid permission to add a user
		self.assertTemplateUsed(response, template)

	def testUpdateRoster(self):
		'''
		Tests the updating the roster
		Case no.       Inputs                  					Expected Output             	Remark
		1.             edit = {username, adminUsername}     	enrollment.edit = True			enrollment is the enrollment of username	
		               manage = {username, adminUsername}		enrollment.manage = True
		               stats = {username, adminUsername}		enrollment.stats = False
							adminUsername = enrollmentTestAdmin
							passwordd = password
							slug = PageViewsPublicCourse
							username = updateTestUser

		2.             edit = {adminUsername}    		 			enrollment.edit = False			enrollment is the enrollment of username
		               manage = {adminUsername}     				enrollment.manage = False
		               stats = {adminUsername}      				enrollment.stats = False
							adminUsername = enrollmentTestAdmin
							password = password
							slug = PageViewsPublicCourse
							username = updateTestUser

		3					slug = 'PageViewsPublicCourse'
							adminUsername = 'PageViewsPublicUser'
							password = 'password'
							template = 'roster/invalid_permissions.html'

		@author Jon Inloes		
		'''
		pass
		
	def testUpdateRosterCase1(self):
		'''
		testUpdateRoster Case 1

		@author Jon Inloes
		'''

		adminUsername = 'enrollmentTestAdmin'
		password = 'password'
		username = 'updateTestUser'
		slug = 'updateTestCourse'

		#logs in and checks to make sure the login was successful
		self.failUnlessEqual(self.client.login(username=adminUsername, password=password), True, 'logging in failed')

		#posts values to be used
		self.client.post('/course/' + slug + '/roster/updateRoster/', {'edit':[username, adminUsername], 'manage':[username, adminUsername], 'stats':[username, adminUsername]})

		enrollment = Enrollment.objects.get(user__username__exact=username, course__slug__exact=slug)

		self.failUnlessEqual(enrollment.view, True, 'view should be true but was ' + str(enrollment.view))
		self.failUnlessEqual(enrollment.stats, True, 'stats should be true but was ' + str(enrollment.stats))
		self.failUnlessEqual(enrollment.manage, True, 'manage should be true but was ' + str(enrollment.manage))
		self.failUnlessEqual(enrollment.edit, True, 'edit should be true but was ' + str(enrollment.edit))

	def testUpdateRosterCase2(self):	
		'''
		testUpdateRoster Case 2

		@author Jon Inloes
		'''

		adminUsername = 'enrollmentTestAdmin'
		password = 'password'
		username = 'updateTestUser'
		slug = 'updateTestCourse'

		#logs in and checks to make sure the login was successful
		self.failUnlessEqual(self.client.login(username=adminUsername, password=password), True, 'logging in failed')

		self.client.post('/course/' + slug + '/roster/updateRoster/', {'edit': [adminUsername], 'manage':[adminUsername], 'stats': [adminUsername]})
		
		enrollment = Enrollment.objects.get(user__username__exact=username, course__slug__exact=slug)

		self.failUnlessEqual(enrollment.view, True, 'view should be false but was ' + str(enrollment.view))
		self.failUnlessEqual(enrollment.stats, False, 'stats should be false but was ' + str(enrollment.stats))
		self.failUnlessEqual(enrollment.manage, False, 'manage should be false but was ' + str(enrollment.manage))
		self.failUnlessEqual(enrollment.edit, False, 'edit should be false but was ' + str(enrollment.edit))

	def testUpdateRosterCase3(self):
		'''
		testUpdateRoster Case 3

		@author Jon Inloes
		'''
	
		slug = 'PageViewsPublicCourse'
		adminUsername = 'PageViewsPublicUser'
		username = 'temp'
		password = 'password'
		template = 'roster/invalid_permissions.html'

		#logs in and checks to make sure the login was successful
		self.failUnlessEqual(self.client.login(username=adminUsername, password=password), True)
		

		#tries to edit a user	but the loggin in user does not have permission 	
		response = self.client.post('/course/' + slug + '/roster/updateRoster/', {'edit': [adminUsername], 'manage':[adminUsername], 'stats': [adminUsername]})

		#asserts that invalid_permissions.html page was rendered because the logged in user did not have valid permission to edit a user's permission
		self.assertTemplateUsed(response, template)

	def testAcceptUser(self):
		'''
		Tests that a user who is enrolled can access a private course, and a 
		student who is not enrolled cannot access a private course

		Case no. 		Inputs											Expected Output 				Remarks
		1. 				adminUsername = 'enrollmentTestAdmin'	enrollment.view = true		enrollment is the enrollment 
							username = 'PrivateUserNotEnrolled'											of username
							slug = 'PageViewsPrivateCourse'
							password = 'password'

		2.					adminUsername = 'enrollmentTestAdmin'	roster/invalid_permissions
							username = 'PrivateUserNotEnrolled'		.html is rendered
							slug = 'PageViewsPrivateCourse'
							password = 'password'

		@author Jon Inloes
		'''
		pass

	def testAccpetUserCase1(self):
		'''
		Test accept user case 1
		
		@author Jon Inloes
		'''

		adminUsername = 'enrollmentTestAdmin'
		username = 'PrivateUserNotEnrolled'
		slug = 'PageViewsPrivateCourse'
		password = 'password'

		#enrollments = Enrollment.objects.filter(course__slug__exact=slug)

		#logs in and checks to make sure the login was successful
		self.failUnlessEqual(self.client.login(username=adminUsername, password=password), True, 'logging in failed')

		#get the enrollment and verify that the user has not been accepted yet
		enrollment = Enrollment.objects.get(user__username__exact=username, course__slug__exact=slug)
		self.failUnlessEqual(enrollment.view, False, 'User has not been enrollmed yet. View permission should be false')

		#accept the user
		self.client.post('/course/' + slug + '/roster/addPendingRequests/', {'accept':[username, 'baduser']})

		#verify that the user has been accepted
		enrollment = Enrollment.objects.get(user__username__exact=username, course__slug__exact=slug)
		self.failUnlessEqual(enrollment.view, True, 'View for user should be true but was' + str(enrollment.view))

	def testAccpetUserCase2(self):
		'''
		Test accept user case 2
			
		@author Jon Inloes
		'''

		slug = 'PageViewsPublicCourse'
		adminUsername = 'PageViewsPublicUser'
		username = 'temp'
		password = 'password'
		template = 'roster/invalid_permissions.html'

		#logs in and checks to make sure the login was successful
		self.failUnlessEqual(self.client.login(username=adminUsername, password=password), True)
		

		#accept the user
		response = self.client.post('/course/' + slug + '/roster/addPendingRequests/', {'accept':[username, 'baduser']})

		#asserts that invalid_permissions.html page was rendered because the logged in user did not have valid permission to accept a user
		self.assertTemplateUsed(response, template)

	def testDenyUser(self):
		'''
		Tests whether or not denying a user from a pending request works.
	
		Case no. 	Inputs											Expected Output	Remarks
		1. 			adminUsername = 'enrollmentTestAdmin'	denied = true		
						username = 'PrivateUserNotEnrolled'
						slug = 'PageViewsPrivateCourse'
						password = 'password'
						denied = False


		@author Jon Inloes
		'''
		
		adminUsername = 'enrollmentTestAdmin'
		username = 'PrivateUserNotEnrolled'
		slug = 'PageViewsPrivateCourse'
		password = 'password'
		denied = False

		#logs in and checks to make sure the login was successful
		self.failUnlessEqual(self.client.login(username=adminUsername, password=password), True, 'logging in failed')

		#checks to make sure the enrollment does not exist
		try:		
			enrollment = Enrollment.objects.get(user__username__exact=username, course__slug__exact=slug)
		except Enrollment.DoesNotExist:
			denied = True

		self.failUnlessEqual(denied, False, 'User does not exist in the enrollment list.')
		self.failUnlessEqual(enrollment.view, False, 'User has not been enrollmed yet. View permission should be false')

		#denies username from the request list
		self.client.post('/course/' + slug + '/roster/addPendingRequests/', {'deny':[username]})

		#checks to see if the user is enrolled	
		try:
			enrollment = Enrollment.objects.get(user__username__exact=username, course__slug__exact=slug)
		except Enrollment.DoesNotExist:
			denied = True

		self.failUnlessEqual(denied, True, 'User should not exist in the enrollment list any more but did')

	def testSearchUser(self):
		'''
		Tests the search user function

		Case no.		Inputs											Expected Output 							Remarks
		1. 			adminUsername = 'enrollmentTestAdmin'	response.contains(username) = true
						username = 'enrollmentTestAdmin'
						firstname = 'Test'
						lastname = 'Admin'
						slug = 'PageViewsPrivateCourse'
						password = 'password'
		
		2.				adminUsername = 'enrollmentTestAdmin'	response.contains(username) = false
						username = 'badUsername'
						firstname = 'badFirstname'
						lastname = 'badLastname'
						slug = 'PageViewsPrivateCourse'
						password = 'password'

		@author Jon Inloes
		'''
		pass
	
	def testSearchUserCase1(self):
		'''
		Test search user case 1

		@author Jon Inloes
		'''

		adminUsername = 'enrollmentTestAdmin'
		username = 'enrollmentTestAdmin'
		firstname = 'Test'
		lastname = 'Admin'
		slug = 'PageViewsPrivateCourse'
		password = 'password'

		#logs in and checks to make sure the login was successful
		self.failUnlessEqual(self.client.login(username=adminUsername, password=password), True, 'logging in failed')
 

		response = self.client.post('/course/' + slug + '/roster/adduser/', {'firstname': firstname, 'lastname': lastname, 'command': 'search'})
		
		self.assertContains(response, username)

	def testSearchUserCase2(self):
		'''
		Test search user case 2

		@author Jon Inloes
		'''

		adminUsername = 'enrollmentTestAdmin'
		username = 'badUsername'
		firstname = 'badFirstname'
		lastname = 'badLastname'
		slug = 'PageViewsPrivateCourse'
		password = 'password'


		#logs in and checks to make sure the login was successful
		self.failUnlessEqual(self.client.login(username=adminUsername, password=password), True, 'logging in failed')
 
		#seraches for a user that does not exist
		response = self.client.post('/course/' + slug + '/roster/adduser/', {'firstname': firstname, 'lastname': lastname, 'command': 'search'})

		#assert that the response does not contain the username
		self.assertNotContains(response, username)

	def testRemoveUser(self):
		'''
		Tests the remove user function

		Case no.		Inputs											Outputs		Remarks
		1				adminUsername = 'enrollmentTestAdmin'
						password = 'password'
						username = 'PrivateUserNotEnrolled'
						slug = 'PageViewsPublicCourse'
		
		@author Jon Inloes
		'''
		adminUsername = 'enrollmentTestAdmin'
		password = 'password'
		username = 'PrivateUserNotEnrolled'
		slug = 'PageViewsPublicCourse'

		#logs in and checks to make sure the login was successful
		self.failUnlessEqual(self.client.login(username=adminUsername, password=password), True, 'logging in failed in enrollment test')

		enrollments = Enrollment.objects.filter(course__slug__exact=slug)

		userExists = True
		try:
			enrollment = Enrollment.objects.get(user__username__exact=username, course__slug__exact=slug)
		except Enrollment.DoesNotExist:
			userExists = False

		self.failUnlessEqual(userExists, True, 'User should exist in the enrollment list')

		self.client.post('/course/' + slug + '/roster/updateRoster/', {'remove': [username], 'command': 'search'})
		

		userExists = True
		try:
			enrollment = Enrollment.objects.get(user__username__exact=username, course__slug__exact=slug)
		except Enrollment.DoesNotExist:
			userExists = False

		self.failUnlessEqual(userExists, False, 'User should not exist in the enrollment list')

	def testAddAnonUser(self):
		'''
		Tests that an anonymous user can join a public course
		
		case#      inputs                                ouputs                            
		-----      ------                                ------                             
		 1          courseid=101                         content includes                   
		            not logged in
		            session['anonCourses'] is empty      "You have been temporarily added"
		                                                 course in session['anonCourses']   
		                              
		 2          courseid=101						 content includes
		            not logged in                        "You are already enrolled in.."
		            session['anonCourses'] includes      no changes are made to session
		            course 101

		@author John Hartquist	            
		'''
		courseslug = "PageViewsPublicCourse" #100 = private, #101 = public
		response = self.client.post('/submit_join_course_request/', {'courseid': 101 })
		self.failIfEqual(response.content.find("You have been temporarily added to"), -1)
		
		response = self.client.post('/submit_join_course_request/', {'courseid':101 })
		 
		self.failIfEqual(response.content.find("You are already enrolled"), -1)

	def testChat(self):
		'''
		Tests that the chat page displays properly

		Case #		Inputs											Outputs							Remark

		1				adminUsername = 'enrollmentTestAdmin'	response.status_code = 200
						password = 'password'
						slug = 'PageViewsPublicCourse'
		
		2				adminUsername = 'enrollmentTestAdmin'	response.status_code = 404
						password = 'password'
						slug = 'badcourse'

		@author Jon Inloes
		'''
		pass
	
	def testChatCase1(self):
		'''
		Test chat case 1

		@author Jon Inloes
		'''

		adminUsername = 'enrollmentTestAdmin'
		password = 'password'
		slug = 'PageViewsPublicCourse'

		#logs in and checks to make sure the login was successful
		self.failUnlessEqual(self.client.login(username=adminUsername, password=password), True, 'logging in failed in enrollment test')

		#Displays the roster and checks to make sure it was successful		
		response = self.client.get('/course/' + slug + '/chat/')
		self.failUnlessEqual(response.status_code, 200, 'redirection to the chat page failed')

	def testChatCase2(self):
		'''
		Test chat case 2
			
		@author Jon Inloes
		'''
		adminUsername = 'enrollmentTestAdmin'
		password = 'password'
		slug = 'badcourse'

		#Displays the roster and checks to make sure it was successful		
		response = self.client.get('/course/' + slug + '/chat/')
		self.failUnlessEqual(response.status_code, 404, 'redirection to the chat page failed')

	def testCancelAdd(self):
		'''
		Test that the cancel_add fucntion redirects to the roster page

		Case #		Inputs											Outputs								Remark

		1				adminUsername = 'enrollmentTestAdmin'	response.status_code = 302		302 is a successful http
						password = 'password'																response redirect
						slug = 'PageViewsPublicCourse'
						template = 'roster/index.html'

		@author Jon Inloes		
		'''

		adminUsername = 'enrollmentTestAdmin'
		password = 'password'
		slug = 'PageViewsPublicCourse'
		template = 'roster/index.html'

		#logs in and checks to make sure the login was successful
		self.failUnlessEqual(self.client.login(username=adminUsername, password=password), True, 'logging in failed in enrollment test')

		#Displays the roster and checks to make sure it was successful		
		response = self.client.get('/course/' + slug + '/roster/adduser/cancel/')
		self.failUnlessEqual(response.status_code, 302, 'redirection to the roster page failed')

	def testAddUsersFromFile(self):
		'''
		Tests the addUsersFromFile of courses.py

		Case #	Inputs											Outputs					Remark
		1			adminUsername = 'enrollmentTestAdmin'	userExists = true		username1, username2, and username 3 exist in the enrollment list
					password = 'password'
					slug = 'PageViewsPublicCourse'
					username1 = 'mgius'
					username2 = 'jinloes'
					username3 = 'pearson'

		2			adminUsername = 'enrollmentTestAdmin'	userExists = true		username1 and username 2 exist in the failed list
					password = 'password'
					slug = 'PageViewsPublicCourse'
					username1 = 'badusername1'
					username2 = 'badusername2'

		3			slug = 'PageViewsPublicCourse'
					adminUsername = 'PageViewsPublicUser'	template is rendered	
					username = 'temp'
					password = 'password'
					template = 'roster/invalid_permissions.html'

		@author Jon Inloes
		'''
		pass

	def testAddUsersFromFileCase1(self):
		'''
		Test addUsersFromFile case 1
		
		@author Jon Inloes
		'''

		adminUsername = 'enrollmentTestAdmin'
		password = 'password'
		slug = 'PageViewsPublicCourse'
		username1 = 'mgius'
		username2 = 'jinloes'
		username3 = 'pearson'

		course = Course.objects.get(slug=slug)

		files = {'key1': file('courses/fixtures/usernames1.txt', 'r'), 'key2': file('courses/fixtures/usernames2.txt')}

		addUsersFromFile(course, files)

		#Test to make sure the user is enrolled
		userExists = True				
		try:
			enrollment = Enrollment.objects.get(user__username__exact=username1, course__slug__exact=slug)

			enrollment2 = Enrollment.objects.get(user__username__exact=username2, course__slug__exact=slug)

			enrollment3 = Enrollment.objects.get(user__username__exact=username3, course__slug__exact=slug)

		except Enrollment.DoesNotExist:
			userExists = False
	
		self.failUnlessEqual(userExists, True, 'the user should exist in the database')

	def testAddUsersFromFileCase2(self):
		'''
		Test addUsersFromFile case 2
		
		@author Jon Inloes
		'''

		adminUsername = 'enrollmentTestAdmin'
		password = 'password'
		slug = 'PageViewsPublicCourse'
		username1 = 'badusername1'
		username2 = 'badusername2'

		course = Course.objects.get(slug=slug)

		files = {'key1': file('courses/fixtures/usernames1.txt', 'r'), 'key2': file('courses/fixtures/usernames2.txt')}

		failedList = addUsersFromFile(course, files)

		self.assertEquals(2, len(failedList), 'List length should be 2')

		#Test to make sure the user is enrolled
		userExists = True				
		try:
			failedList.index(username1)
			failedList.index(username2)

		except Enrollment.DoesNotExist:
			userExists = False
	
		self.failUnlessEqual(userExists, True, 'failed list did not contain a name it should have')

	def testAddUsersFromFileCase3(self):
		'''
		Test add users from file case 3
		
		@author Jon Inloes	
		'''
		slug = 'PageViewsPublicCourse'
		adminUsername = 'PageViewsPublicUser'
		username = 'temp'
		password = 'password'
		template = 'roster/invalid_permissions.html'

		#logs in and checks to make sure the login was successful
		self.failUnlessEqual(self.client.login(username=adminUsername, password=password), True)
		

		#tries to add a user		
		response = self.client.post('/course/' + slug + '/roster/adduser/addFromFile/', {'username': username, 'command': 'add'})
		self.failUnlessEqual(response.status_code, 200, 'redirection to the roster page failed')

		#asserts that invalid_permissions.html page was rendered because the logged in user did not have valid permission to add a user
		self.assertTemplateUsed(response, template)
	
# I don't know why, but for some reason join_course_request is returning a 
# 302.  Why?
#	def testPrivateEnrollment(self):
#		'''
#		Tests that a user who is not enrolled can request access to a 
#		private course
#
#		After the user has enrolled in the course, verify that they cannot view
#		the course.  
#
#		After verifying that they cannot view the course, grant them view 
#		permission and verify that they can view the course
#		'''
#		user = User.objects.get(username='PageViewsEnrollmentUser')
#		privateCourse = Course.objects.get(slug='PageViewsPrivateCourse')
#
#      # attempt to enroll in the course
#		response = self.client.post('/submit_join_course_request', \
#				                      {'courseid':privateCourse.id})
#
#      # check for 200 OK and text pending
#		self.assertContains(response, "pending")
#
#      # verify that the enrollmment exists and that the user has no view 
#      # permission
#		enrollment = Enrollment.objects.get(user=user, course=privateCourse)
#
#		assertEquals(enrollment.view, False)
