"""
This file contains tests for the users package. 

@author John Hartquist
@author Russell Mezzetta
@author James Pearson
"""

#import unittest
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from users.user import registerNewUser, loginWrapper

class UserTests(TestCase):
	'''
	@author John Hartquist
	@author Russell Mezzetta
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
	Phase 1: Test logging in, logging out, viewing profile, updating email, registering a new user
	'''
	
	fixtures = ['UserTests']

	user1 = "usertestuser1"
	user1email = "testuser1email"
	password = "password"
	user2 = "usertestuser2"
	user2email = "testuser2email"
	private_course = "testcourseprivate"
	public_course = "testcoursepublic"

	
	def setUp(self):
		'''
		Called before each test
		'''
		self.client = Client()
		users = User.objects.all()

	def testLogin(self):
		'''
		@author John Hartquist
		Tests that a user can login successfully
		
		case#            input        expected         output    remark
		-----            -----        --------         ------    ------
		1                status_code  200              200       posts a login request
		'''		
		response = self.client.post("/login/", {'username': self.user1, \
		                                        'password': self.password})
		self.failUnlessEqual(response.status_code, 302)

	def testLogout(self):
		'''
		@author John Hartquist
		Tests that a user can logout successfully
		
		case#            input        expected         output    remark
		-----            -----        --------         ------    ------
		2                status_code  200              200       posts a logout request
		'''
		response = self.client.post("/logout/") 
		self.failUnlessEqual(response.status_code, 200)

	def testShowProfile(self):
		'''
		@author John Hartquist
		Tests that a user can view their profile
		
		case#            input        expected         output    remark
		-----            -----        --------         ------    ------
		1                status_code  200              200       shows a users profile
		
		'''
		self.client.post("/login/", {'username': self.user1,
		                             'password': self.password})
		response = self.client.get("/profile/")
		self.failUnlessEqual(response.status_code, 200)
		
	def testUpdateEmail(self):
		'''
		Tests that a user can change their e-mail address
		
		case#            input             expected      output   remark
		-----            -----             --------      ------   ------
		1                email=badEmail    1             1        valid e-mail check
		2                email=user1email  0             0        success
		
		'''
		badEmail = "anemail@nothing"
		
		self.client.post("/login/", {'username': self.user1,
		                             'password': self.password})
	
		#test changing to a bad malformed email	
		response = self.client.post("/profile/", {'form': "Change E-mail", 'email': badEmail })
		self.failIfEqual(response.content.find("Invalid E-mail Address"), -1)

	def testRegisterNewUser(self):
		'''
		@author Russell Mezzetta
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
		@author Russell Mezzetta
		Tests the login view and wrapper for full functionality.

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
		'''
		
		invalidUser = "nonexistantuser"
		
		#valid login
		response = self.client.post('/login/', {'username': self.user1, 'password': self.password})
		self.failUnlessEqual(response.content.find("CSTutor Login"), -1)
		self.failUnlessEqual(response.status_code, 302)
		
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
