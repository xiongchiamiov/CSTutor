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

		@author Russell Mezzetta
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
