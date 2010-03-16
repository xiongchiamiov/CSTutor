'''
This file contains tests for the users package. 

@author John Hartquist
@author Russell Mezzetta
@author James Pearson
'''

#import unittest
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from users.user import registerNewUser, loginWrapper
from django.core.urlresolvers import reverse
from courses.models import Course


class UserTests(TestCase):
	'''
	This class deals with all of the test cases regarding 'users'
	We will be using 'Client()' objects to simulate client requests
	for logging in and out, editing and viewing user profiles.
	
	CLASS TEST PLAN
	Phase 0: Load test fixtures (UserTests.xml)
		This fixture consists of two courses:
		testcourseprivate has none.
		testcoursepublic has a lesson and a quiz.
		Two users:
		Testuser1 has full permissions in both courses. 
		Testuser2 has no enrollments. 
	Phase 1: Test logging in, logging out, viewing profile, updating email, updating name,
	         deleting account, registering a new user

	@author John Hartquist
	@author Russell Mezzetta
	'''
	
	fixtures = ['UserTests']

	user1 = "usertestuser1"
	user1email = "testuser1email"
	password = "password"
	user2 = "usertestuser2"
	user2email = "testuser2email"
	disabledUser = "disabledUser"
	private_course = "testcourseprivate"
	public_course = "testcoursepublic"

	
	def setUp(self):
		'''
		Called before each test

		@author Russell Mezzetta
		'''
		self.client = Client()
		users = User.objects.all()

	def testLogin(self):
		'''
		Tests that a user can login successfully
		
		case#            input        expected         output    remark
		-----            -----        --------         ------    ------
		1                status_code  200              200       posts a login request

		@author John Hartquist
		'''		
		response = self.client.post("/login/", {'username': self.user1, \
		                                        'password': self.password})
		self.failUnlessEqual(response.status_code, 302)

	def testLogout(self):
		'''
		Tests that a user can logout successfully
		
		case#            input        expected         output    remark
		-----            -----        --------         ------    ------
		2                status_code  200              200       posts a logout request

		@author John Hartquist
		'''
		response = self.client.post("/logout/") 
		self.failUnlessEqual(response.status_code, 200)

	def testShowProfile(self):
		'''
		Tests that a user can view their profile
		
		case#            input           expected             output              remark
		-----            -----           --------             ------              ------
		1                not logged in   "not logged in"      "not logged in"     anon user not logged in
		
		2                logged in       shows the profile    shows the profile   
		
		@author John Hartquist
		'''
		
		#try viewing profile while not logged in
		response = self.client.get("/profile/")
		self.failIfEqual(response.content.find("You are not currently logged in"), -1)
		
		
		#log in
		self.client.post("/login/", {'username': self.user1,
		                             'password': self.password})
		
		#try to view profile again
		response = self.client.get("/profile/")
		self.failUnlessEqual(response.status_code, 200)
		
	def testUpdateEmail(self):
		'''
		Tests that a user can change their e-mail address
		
		case#            input             expected      output   remark
		-----            -----             --------      ------   ------
		1                email=badEmail    1             1        valid e-mail check
		2                email=user1email  0             0        success
		
		@author John Hartquist
		'''
		badEmail = "anemail@nothing"
		user1email = "john@abc.com"
		
		self.client.post("/login/", {'username': self.user1,
		                             'password': self.password})
	
		#test changing to a bad malformed email	
		response = self.client.post("/profile/", {'form': "Change E-mail", 'email': badEmail })
		self.failIfEqual(response.content.find("Invalid E-mail Address"), -1)

        #test changing to a valid email 	
		response = self.client.post("/profile/", {'form': "Change E-mail", 'email': user1email })
		self.failIfEqual(response.content.find("E-mail : " + user1email), -1)
		

	def testChangePassword(self):
		'''
		Tests that a user can change their password
		
		case#    input                  expected                     output                     remark
		-----    -----                  --------                     ------                     ------
		1        user='jhartqui'        invalid current password     invalid current password   user must provide valid password
		         currentpw='x'
		         newpass1='a'
		         newpass2='a'
		         
		2        user='jhartqui'		password don't match         password don't match       user must provide matching passwords
		         currentpw='password'
		         newpass1='a'
		         newpass2='b'
		      
		3        user='jhartqui'		succcess                     success                    user successfully changes password
		         currentpw='password'
		         newpass1='new111'
		         newpass2='new111'

		@author John Hartquist
		'''
		
		
		self.client.post("/login/", {'username': self.user1,
		                             'password': self.password})
	
		#test providing invalid current password
		response = self.client.post("/profile/", {'form': "Change Password", 'oldpass': "x", 'newpass1':"a", 'newpass2':"a" })
		self.failIfEqual(response.content.find("Incorrect current password"), -1)

        #test mismatching passwords	
		response = self.client.post("/profile/", {'form': "Change Password", 'oldpass': self.password, 'newpass1':"a", 'newpass2':"b" })
		self.failIfEqual(response.content.find("Passwords do not match"), -1)
		
		#test a valid password change
		response = self.client.post("/profile/", {'form': "Change Password", 'oldpass': self.password, 'newpass1':"a", 'newpass2':"a" })
		self.failUnlessEqual(response.status_code, 200)

	def testChangeName(self):
		'''
		Tests that the user can update their name
		
		case#    input                  expected                     output                     remark
		-----    -----                  --------                     ------                     ------
		1        first_name=""          status_code=200              200                         name does not change
		         last_name=""           
		
		2        first_name=""          status_code=200              200                         name does not change
		         last_name="Last" 
		        
		3        first_name="First"     status_code=200              200                         name does not change
		         last_name="" 
		         
		4        first_name="First"     response contains            response contains           name changes
		         last_name="Last"       "First" and "Last"           "First" and "Last"
		
		@author John Hartquist
		'''
		
		self.client.post("/login/", {'username': self.user1,
		                             'password': self.password})
	
		#test providing blank name
		response = self.client.post("/profile/", {'form': "Update Name", 'first_name': "", 'last_name':"" })
		self.failUnlessEqual(response.status_code, 200)
		
		#test providing blank first name
		response = self.client.post("/profile/", {'form': "Update Name", 'first_name': "", 'last_name':"Last" })
		self.failUnlessEqual(response.status_code, 200)
		
		#test providing blank last name
		response = self.client.post("/profile/", {'form': "Update Name", 'first_name': "First", 'last_name':"" })
		self.failUnlessEqual(response.status_code, 200)
		
		#test that password changes
		response = self.client.post("/profile/", {'form': "Update Name", 'first_name': "First", 'last_name':"Last" })
		self.failIfEqual(response.content.find("First"), -1)
		self.failIfEqual(response.content.find("Last"), -1)
		
		
	def testDeleteUser(self):
		'''
		Tests that a user can delete himself
		
		case#            input                      expected                output                   remark
		-----            -----                      --------                ------                   ------
		1                user clicks delete         user account exists     user account exists      user must confirm delete account
		                 selects 'No' at confirm
		   
		2                user clicks delete         user account deleted    user account deleted     user confirms delete account
		                 selects 'Yes' at confirm

		@author John Hartquist
		'''
		
		#test user clicking yes
		registerNewUser("NewUser", "password", "password", "first", "last", "newuser@email.com")
		self.client.post("/login/", {'username': "NewUser",
		                             'password': "password"})
		
		response = self.client.post("/profile/", {'form': "Delete Account"})
		response = self.client.post("/profile/", {'form': "Yes"})
		self.failUnlessEqual(response.status_code, 302)
		
	def testRegisterNewUser(self):
		'''
		Tests the registerNewUser helper function
		
		case#    input                 expected output     remark
		-----    -----                 ---------------     ------
		1        username=""           3                   "all empty string params"
		         pass=""
		         pass2=""
		         first=""
		         last=""
		         email=""
		
		2        username="NewUser"    4                   "password missing"
		         pass=""
		         pass2=""
		         first=""
		         last=""
		         email=""
		
		3        username="NewUser"    5                   "firstname missing"
		         pass="pass1"
		         pass2="pass1"
		         first=""
		         last="lastname"
		         email=""
		
		4        username="NewUser"    5                   "lastname missing"
		         pass="pass1"
		         pass2="pass1"
		         first="firstname"
		         last=""
		         email=""
		
		5        username="NewUser"    2                   "mismatched passwords"
		         pass="pass1"
		         pass2="pass2"
		         first="john"
		         last="smith"
		         email=""
		
		6        username="NewUser"    0                   "valid user registration"
		         pass="password"
		         pass2="password"
		         first="john"
		         last="smith"
		         email="newuser@email.com"
		
		7        username="NewUser"    1                   "try to add an already-existing username"
		         pass="something"
		         pass2="something"
		         first="johnny"
		         last="smithy"
		         email="other@email.com"
		
		@author Russell Mezzetta
		'''
		#pass in all empty strings
		r = registerNewUser("","","","","","")
		self.failUnlessEqual(r,3)
		#try a username no password
		r = registerNewUser("NewUser", "", "", "","","")
		self.failUnlessEqual(r, 4)
		#try a user/pass/last with no first name
		r = registerNewUser("NewUser", "pass1", "pass1", "","lastname","")
		self.failUnlessEqual(r, 5)
		#try a user/pass/first with no last name
		r = registerNewUser("NewUser", "pass1", "pass1", "firstname","","")
		self.failUnlessEqual(r, 5)
		#try mismatched passwords
		r = registerNewUser("NewUser", "pass1", "pass2", "first", "last", "")
		self.failUnlessEqual(r, 2)
		#add a user
		r = registerNewUser("NewUser", "password", "password", "first", "last", "newuser@email.com")
		self.failUnlessEqual(r, 0)
		#check that user is in the Users list
		
		#try to add a user with the same name as another user(from previous successful test)
		r = registerNewUser("NewUser", "something", "something", "first", "last", "other@email.com")
		self.failUnlessEqual(r, 1)

	def testLoginWrapper(self):
		'''
		Tests the login view and implicitly the wrapper for full functionality.

		case#    input                	expected output   remark
		-----    -----                	---------------   ------
		1			username = user1			status_code 302	successful login
					password = password
		
		2			username = invalidUser 	status_code 200	invalid username
					password = password
		
		3			username = user1 			status_code 200	invalid password
					password = password+"x"
		
		4			username = "" 				status_code 200   empty username
					password = password
		
		5			username = user1 			status_code 200   empty password
					password = ""
		
		6			username = disabledUser	status_code 200	user marked not active
					password = password

		@author Russell Mezzetta
		'''
		
		invalidUser = "nonexistantuser"
		
		#valid login
		response = self.client.post('/login/', {'username': self.user1, 'password': self.password})
		self.failUnlessEqual(response.content.find("CSTutor Login"), -1)
		self.failUnlessEqual(response.status_code, 302)
		self.client.logout()
		
		#invalid username
		response = self.client.post('/login/', {'username': invalidUser, "password": self.password})
		self.failIfEqual(response.content.find("CSTutor Login"), -1)
		self.failUnlessEqual(response.status_code, 200)
		
		#invalid password
		response = self.client.post('/login/', {'username': self.user1, "password": self.password+"x"})
		self.failIfEqual(response.content.find("CSTutor Login"), -1)
		self.failUnlessEqual(response.status_code, 200)
		
		#empty username
		response = self.client.post('/login/', {'username': "", "password": "pass"})
		self.failIfEqual(response.content.find("CSTutor Login"), -1)
		self.failUnlessEqual(response.status_code, 200)
		
		#empty password
		response = self.client.post('/login/', {'username': self.user1, "password": ""})
		self.failIfEqual(response.content.find("CSTutor Login"), -1)
		self.failUnlessEqual(response.status_code, 200)

		#disabled user (is_active=false)
		response = self.client.post('/login/', {'username': self.disabledUser, 'password': self.password})
		self.failIfEqual(response.content.find("Account marked as inactive"), -1)
		self.failUnlessEqual(response.status_code, 200)

	def testLoggedInUserAutoLogin(self):
		'''
		Tests the login view when the user has already logged in using the autologin checkbox.

		case#    input                				expected output   remark
		-----    -----                				---------------   ------
		1			username = user1						status_code 302	successful login
					password = password
																						request.session['autologin']=True

		2			visit login page no input			status_code 302	user is immediately redirected
					request.session['autologin']=True

		@author Russell Mezzetta
		'''
		
		#valid login
		response = self.client.post('/login/', {'username': self.user1, 'password': self.password, 'autologin': 'autologin'})
		self.failUnlessEqual(response.content.find("CSTutor Login"), -1)
		self.failUnlessEqual(response.status_code, 302)
		self.failUnlessEqual(self.client.session['autologin'], True)
		
		#revisit the login page without supplying any username/pass
		response = self.client.get('/login/')
		self.failUnlessEqual(response.content.find("CSTutor Login"), -1)
		self.failUnlessEqual(response.status_code, 302)

	def testLoggingInWithAllCheckboxesChecked(self):
		'''
		Tests the login view when user checks all checkboxes. Should count as anonymous login.

		case#    input                				expected output   remark
		-----    -----                				---------------   ------
		1			username = ""							status_code 302	successful login
					password = ""

		@author Russell Mezzetta
		'''
		
		#valid anonymous login
		response = self.client.post('/login/', {'username': "", 'password': "", 'anonymous': 'anonymous', 'autologin': 'autologin', 'rememberme': 'rememberme'})
		self.failUnlessEqual(response.content.find("CSTutor Login"), -1)
		self.failUnlessEqual(response.status_code, 302)
		
	def testLoginRememberMe(self):
		'''
		Tests the login view when user checks rememberMe.

		case#    input                	expected output   				remark
		-----    -----                	---------------   				------
		1			username = user1			status_code 302					successful login
					password = password		session contains 					session modified
													rememberme and
													username = user1

		2			none							username field contains user1	username field pre-filled
		@author Russell Mezzetta
		'''
		
		#valid login
		response = self.client.post('/login/', {'username': self.user1, 'password': self.password, 'rememberme': 'rememberme'})
		self.failUnlessEqual(response.content.find("CSTutor Login"), -1)
		self.failUnlessEqual(response.status_code, 302)
		
		#verify that session is in proper state
		self.failUnlessEqual(self.client.session['rememberme'], True)
		self.failUnlessEqual(self.client.session['username'], self.user1)
		
		#logout, then check that login page prefills the username
		self.client.get('/logout/')
		response = self.client.get('/login')
		self.failUnlessEqual(response.status_code, 200)
		#note: response.context is a list, response.context[0] is a dictionary
		self.failUnlessEqual(response.context[0]['loginusername'], self.user1)

	def testMostBasicLoginView(self):
		'''
		Tests the login view for user with no session data. Just for coverage purposes really.

		case#    input          expected output   remark
		-----    -----          ---------------   ------
		1			none				status_code 200	login page displayed
		@author Russell Mezzetta
		'''
		
		response = self.client.get('/login/')
		self.assertContains(response, "CSTutor Login", status_code=200)

	#I'd really like to be able to test this but i don't think it is possible in
	# django 1.0 to craft request with get and post data.
	#def testLoginThenRedirect(self):
	#	'''
	#	Tests the @login_required decorator.
	#	The decorator forces a get request to login with a 'next' key in the dictionary that has a value of the destination url to redirect to.
	#	This test is mainly for coverage, it's actually an awkward test.
	#	
	#	case#    input          	expected output   remark
	#	-----    -----          	---------------   ------
	#	1			user=user1			status_code 302	redirected to profile page after sucessful login
	#				password=password
	#				next='/profile/'

	#	@author Russell Mezzetta
	#	'''
		#response = self.client.get('/create-course')
		#import pdb; pdb.set_trace()
		#print "\n" + response.request.GET['next']
		#response = self.client.post('/login/', {'username': self.user1, 'password': self.password} 'next': '/profile/'})
		#self.assertEqual(response.status_code, 302)
	def testViewHistorySavedAfterLogout(self):
		'''
		After viewing a page, data about the page is saved in the session.
		When the user logs out this data should be saved for next time they log in.
		This test makes sure that the data is saved.

		case#    input          						expected output   								remark
		-----    -----          						---------------   								------
		1			'/login/'								status_code 302									successful login
					user = user1
					password = password

		2			'/course/%s/page/%s/'				status_code 200									visit public_course's index page
					(public_course, public_course)	session['lastCourseSlug']=public_course
																session['lastPageSlug']=public_course
																session['lastPageEdit']=False

		3			'/logout/'								status_code 200									after log out session still good
																session['lastCourseSlug']=public_course
																session['lastPageSlug']=public_course
																session['lastPageEdit']=False

		@Russell Mezzetta
		'''
		#valid login
		response = self.client.post('/login/', {'username': self.user1, 'password': self.password})
		self.failUnlessEqual(response.content.find("CSTutor Login"), -1)
		self.failUnlessEqual(response.status_code, 302)
		
		#visit a page so the view history gets saved to session
		response = self.client.get('/course/%s/page/%s/' % (self.public_course,self.public_course))
		self.failUnlessEqual(response.status_code, 200)
		#print client.session
		#verify session content
		self.failUnlessEqual(self.client.session['lastCourseSlug'], self.public_course)
		self.failUnlessEqual(self.client.session['lastPageSlug'], self.public_course)
		self.failUnlessEqual(self.client.session['lastPageEdit'], False)
		
		#log user out and verify the contents of session still remain
		self.client.get('/logout/')
		self.failUnlessEqual(self.client.session['lastCourseSlug'], self.public_course)
		self.failUnlessEqual(self.client.session['lastPageSlug'], self.public_course)
		self.failUnlessEqual(self.client.session['lastPageEdit'], False)

	def testRegisterNewUserView(self):
		'''
		Tests the registerNewUser view
		
		case#    input                 expected output     											remark
		-----    -----                 ---------------     											------
		1        username=""           errormsg="The username field is empty"   				"all empty string params"
		         pass=""
		         pass2=""
		         first=""
		         last=""
		         email=""
		
		2        username="NewUser"    errormsg="The password field is empty"					"password missing"
		         pass=""
		         pass2=""
		         first=""
		         last=""
		         email=""
		
		3        username="NewUser"    errormsg="Either first or last name field is empty	"firstname missing"
		         pass="pass1"
		         pass2="pass1"
		         first=""
		         last="lastname"
		         email=""
		
		4        username="NewUser"    errormsg="Either first or last name field is empty	"lastname missing"
		         pass="pass1"
		         pass2="pass1"
		         first="firstname"
		         last=""
		         email=""
		
		5        username="NewUser"    errormsg="Passwords do not match"							"mismatched passwords"
		         pass="pass1"
		         pass2="pass2"
		         first="john"
		         last="smith"
		         email=""
		
		6        username="NewUser"    user added, redirect to login page							"valid user registration"
		         pass="password"
		         pass2="password"
		         first="john"
		         last="smith"
		         email="newuser@email.com"
		
		7        username="NewUser"    errormsg="That username is already taken"				"try to add an already-existing username"
		         pass="something"
		         pass2="something"
		         first="johnny"
		         last="smithy"
		         email="other@email.com"
		8			none						status_code 200													"GET view"
		
		@author Russell Mezzetta
		'''
		#pass in all empty strings
		data = {'username': '', 'password': '', 'verifypassword': '',\
					'firstname': '', 'lastname': '', 'email': ''}
		response = self.client.post('/login/register-new-account/', data)
		self.assertContains(response, "The username field is empty")

		#try a username no password
		data = {'username': 'NewUser', 'password': '', 'verifypassword': '',\
					'firstname': '', 'lastname': '', 'email': ''}
		response = self.client.post('/login/register-new-account/', data)
		self.assertContains(response, "The password field is empty")
		
		#try a user/pass/last with no first name
		data = {'username': 'NewUser', 'password': 'pass1', 'verifypassword': 'pass1',\
					'firstname': '', 'lastname': 'lastname', 'email': ''}
		response = self.client.post('/login/register-new-account/', data)
		self.assertContains(response, "Either first name or last name field is empty")
		
		#try a user/pass/first with no last name
		data = {'username': 'NewUser', 'password': 'pass1', 'verifypassword': 'pass1',\
					'firstname': 'firstname', 'lastname': '', 'email': ''}
		response = self.client.post('/login/register-new-account/', data)
		self.assertContains(response, "Either first name or last name field is empty")
		
		#try mismatched passwords
		data = {'username': 'NewUser', 'password': 'pass1', 'verifypassword': 'pass2',\
					'firstname': 'first', 'lastname': 'last', 'email': ''}
		response = self.client.post('/login/register-new-account/', data)
		self.assertContains(response, "Passwords do not match")

		#add a user
		data = {'username': 'NewUser', 'password': 'password', 'verifypassword': 'password',\
					'firstname': 'first', 'lastname': 'last', 'email': 'newuser@email.com'}
		response = self.client.post('/login/register-new-account/', data, follow=False)
		self.assertRedirects(response, reverse('users.views.show_login'))
		#check that user is in the Users list
		self.assertEqual(User.objects.filter(username = 'NewUser').count(), 1)
		
		#try to add a user with the same name as another user(from previous successful test)
		data = {'username': 'NewUser', 'password': 'password', 'verifypassword': 'password',\
					'firstname': 'first', 'lastname': 'last', 'email': 'newuser@email.com'}
		response = self.client.post('/login/register-new-account/', data, follow=False)
		self.assertContains(response, "That username is already taken")
		
		#Just view the page
		response = self.client.get('/login/register-new-account/')
		self.assertEqual(response.status_code, 200)

	def testRegisterNewUserViewAnonCourses(self):
		'''
		Tests to make sure that the courses joined by an anonymous user are added to the user's
		course list when the anonymous user registers
		
		case#    input                expected output     											remark
		-----    -----                ---------------     											------
		1			'/join-course/'		status_code = 200
					public_course			contains 'You have been temporarily added to"

		2        username=""				errormsg="The username field is empty"   				"all empty string params"
		         pass=""
		         pass2=""
		         first=""
		         last=""
		         email=""
	
		@author Russell Mezzetta
		'''
		pubCourse = Course.objects.get(slug = self.public_course)
		#anonymous user joins public_course
		response = self.client.post('/submit_join_course_request', {'courseid':pubCourse.id})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "You have been temporarily added to %s" % (pubCourse.name))

		#register the anonymous user
		data = {'username': 'NewUser', 'password': 'password', 'verifypassword': 'password',\
					'firstname': 'first', 'lastname': 'last', 'email': 'newuser@email.com'}
		response = self.client.post('/login/register-new-account/', data, follow=False)
		self.assertRedirects(response, reverse('users.views.show_login'))
		#check that user is in the Users list
		self.assertEqual(User.objects.filter(username = 'NewUser').count(), 1)
		#check that user has an enrollment to the course
		self.assertEqual(User.objects.get(username='NewUser').enrollments.all()[0].course, pubCourse)

