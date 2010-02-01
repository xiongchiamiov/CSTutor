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
		'''
		username = 'jhartquist'
                password = 'password'
                response = self.client.post("/login/", {'username'=username,
                                                        'password'=password})
                self.failUnlessEqual(response.status_code, 200)
