"""
Tests for the codeshells

@author James Pearson, Mark Gius
"""

from django.test import TestCase
from django.test.client import Client
from codeshell.pythoncode import evalPythonString

class PythonCodeTests(TestCase):
	'''
	This class tests the "pythoncode" shell.

	@author James Pearson, Mark Gius
	'''

	def test_hello_world(self):
		'''
		Tests that a simple "Hello World" program successfully executes via
		the codeshell

		Case no.    Inputs                    Expected
		1				print "Hello World"       "Hello World"

		@author James Pearson, Mark Gius
		'''
		(codeOutput, scope) = evalPythonString('print "Hello World"')
		self.assertEquals("Hello World\n", codeOutput)

	def test_import_failure(self):
		'''
		Users shouldn't not be allowed to import arbitrary modules

		Verify that they can't

		Case no.    Inputs                    Expected
		1				from math import fabs     "Importing is disallowed"
		            print abs(-1)

		@author James Pearson, Mark Gius
		'''
		code = "from math import fabs\n" + "print abs(-1)"
		(codeOutput, scope) = evalPythonString(code)
		self.assertEquals("ImportError.  Importing is disallowed", codeOutput)

	def test_for_loops(self):
		'''
		Forloops require calling iter() on something, so it's a decent test

		Case no.    Inputs                    Expected
		1				for x in range(2):        0 \\n 1
						print x

		@author James Pearson, Mark Gius
		'''
		code = "for x in range(2):\n" + " print x"
		(codeOutput, scope) = evalPythonString(code)
		self.assertEquals("0\n1\n", codeOutput)

	def test_assignment(self):
		'''
		Test simple assignment of variables.

		@author James Pearson, Mark Gius
		'''
		code = "x = 5\n" + "print x"
		(codeOutput, scope) = evalPythonString(code)
		self.assertEquals("5\n", codeOutput)
		self.assertEquals(5, scope['x'])

	def test_simple_class(self):
		'''
		Test creating a simple class with a single attribute

		@author James Pearson, Mark Gius
		'''

		code = "class foo():\n" + \
				 " x = 5\n" + \
				 "fooInstance = foo()\n" + \
				 "print fooInstance.x\n" + \
				 "fooInstance.x = 4\n" + \
				 "print fooInstance.x"

		(codeOutput, scope) = evalPythonString(code)
		self.assertEquals("5\n4\n", codeOutput)
