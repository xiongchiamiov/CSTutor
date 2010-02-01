"""
This file contains tests for the users package. 

@author John Hartquist
"""

import unittest
from django.test.client import Client
from django.contrib.auth.models import User

class UserTests(unittest.TestCase):
	username = 'jhartquist'
	password = 'password'
	
	def setUp(self):
		'''
		Sets up the tests
		'''
		self.client = Client()
		users = User.objects.all()

	def testLogin(self):
		'''
		Tests that a user can login successfully
		'''
		username = 'jhartquist'
		password = 'password'
		response = self.client.post("/login/", {'username': username,
                                                'password': password})
		self.failUnlessEqual(response.status_code, 200)

	def testLogout(self):
		'''
		Tests that a user can logout successfully
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
		print(response.content)
		self.failIfEqual(response.content.find("Invalid E-mail Address"), -1)