"""
This file contains tests for the users package. 

@author John Hartquist
@author Russell Mezzetta
@author James Pearson
"""

import unittest
from django.test.client import Client
from django.contrib.auth.models import User
from users.user import registerNewUser, loginWrapper

class UserTests(unittest.TestCase):
	'''
	@author John Hartquist
	@author Russell Mezzetta
	This class deals with all of the test cases regarding 'users'
	We will be using 'Client()' objects to simulate client requests
	for logging in and out, editing and viewing user profiles.
	
	CLASS TEST PLAN
	Phase 0: Load test fixtures (initial-data.xml)
	Phase 1: Unit test login, logout, register new user, show profile, updateEmail
	'''
	def setUp(self):
		'''
		Sets up the tests
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
		username = 'jhartquist'
		password = 'password'
		response = self.client.post("/login/", {'username': username,
		                                        'password': password})
		self.failUnlessEqual(response.status_code, 302)

	def testLogout(self):
		'''
		@author John Hartquist
		Tests that a user can logout successfully
		
		case#            input        expected         output    remark
		-----            -----        --------         ------    ------
		2                status_code  200              200       posts a logout request
		'''
		username = 'jhartquist'
		password = 'password'
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
		username = 'jhartquist'
		password = 'password'
		self.client.post("/login/", {'username': username,
		                             'password': password})
		response = self.client.get("/profile/")
		self.failUnlessEqual(response.status_code, 200)
		
	def testUpdateEmail(self):
		'''
		Tests that a user can change their e-mail address
		
		case#            input                         expected      output   remark
		-----            -----                         --------      ------   ------
		1                email='anemail@nothing'       1             1        valid e-mail check
		2                email='jhartqui@calpoly.edu'  0             0        success
		
		'''
		badEmail = "anemail@nothing"
		goodEmail = "jhartqui@calpoly.edu"
		username = 'jhartquist'
		password = 'password'
		
		self.client.post("/login/", {'username': username,
		                             'password': password})
		
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
		Tests the login wrapper for valid functionality.

		Couldn't figure out how to get the test suite to directly test the loginWrapper b/c
		The loginWrapper takes a request object, which needs a valid session/sessionid for login
		The solution: use less elegant testing method of searching the login response for text
		'''
		testUser = "testuserLW"
		testPass = "password"
		registerNewUser(testUser, testPass, testPass, "first", "last", "email")

		#valid login
		response = self.client.post('/login/', {'username': testUser, 'password': testPass})
		self.failUnlessEqual(response.content.find("CSTutor Login"), -1)
		self.failUnlessEqual(response.status_code, 302)
		
		#invalid username
		response = self.client.post('/login/', {'username': "defnotauser", "password": "pass"})
		self.failIfEqual(response.content.find("CSTutor Login"), -1)
		self.failUnlessEqual(response.status_code, 200)
		
		#invalid password
		response = self.client.post('/login/', {'username': testUser, "password": testPass+"x"})
		self.failIfEqual(response.content.find("CSTutor Login"), -1)
		self.failUnlessEqual(response.status_code, 200)
		
		#empty username
		response = self.client.post('/login/', {'username': "", "password": "pass"})
		self.failIfEqual(response.content.find("CSTutor Login"), -1)
		self.failUnlessEqual(response.status_code, 200)
		
		#empty password
		response = self.client.post('/login/', {'username': testUser, "password": ""})
		self.failIfEqual(response.content.find("CSTutor Login"), -1)
		self.failUnlessEqual(response.status_code, 200)
