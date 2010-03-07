'''
Functions that are useful for executing python.

This could be as simple as an "eval," but it is sometimes handy to do something
like sanitize code or capture output, etc, so we have a special execute
function that will abstract all that garbage out

SECURITY RISK: NONE OF THESE FUNCTIONS DO ANY KIND OF SANITIZING!!!!
'''

import compiler

def evalPythonCode(code):
	'''
	Executes compiled python code

	Takes in a code object and evaluates it. Returns the result
	'''

def evalPythonString(string):
	'''
	Executes strings of python code

	Takes in a string and evaluates it.  returns the result
	'''
	return eval(string, {}, {})
