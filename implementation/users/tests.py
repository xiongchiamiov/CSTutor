"""
This file contains tests for the users package. 

@author John Hartquist
"""

import unittest
from django.test.client import Client
from django.contrib.auth.models import User

class UserTests(unittest.TestCase):
	def setUp(self):
		'''
		Sets up the tests
		'''
		self.client = Client()
		users = User.objects.all()

	def testLogin(self):
		'''
		Tests that a user can login successfully
                
                case#            input        expected         output    remark
                -----            -----        --------         ------    ------
                1                status_code  200              200       posts a login request
		'''
		username = 'jhartquist'
		password = 'password'
		response = self.client.post("/login/", {'username': username,
                                                'password': password})
		self.failUnlessEqual(response.status_code, 200)

	def testLogout(self):
		'''
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
		Tests that a user can view their profile
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
		'''
		badEmail = "anemail@nothing"
		goodEmail = "jhartqui@calpoly.edu"
		username = 'jhartquist'
		password = 'password'
		
		self.client.post("/login/", {'username': username,
                                     'password': password})
		
		response = self.client.post("/profile/", {'form': "Change E-mail", 'email': badEmail })
		self.failIfEqual(response.content.find("Invalid E-mail Address"), -1)
