"""
Tests for the home view.

@author James Pearson
"""

import unittest
from django.test.client import Client

class SimpleTest(unittest.TestCase):
	def test_home(self):
		'''
		Does the home page not fail horribly?
		
		Case no.    Inputs     Expected
		1           url = /    status code of 200
		'''
		response = Client().get('/').status_code
		self.failUnlessEqual(response, 200, "Hmm, that's not good; we got a status code of %s instead." % response)
