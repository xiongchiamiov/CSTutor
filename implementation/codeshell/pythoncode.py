'''
Functions that are useful for executing python.

This could be as simple as an "eval," but it is sometimes handy to do something
like sanitize code or capture output, etc, so we have a special execute
function that will abstract all that garbage out

Currently no checks on long-running code.

@author Mark Gius
@author James Pearson
'''


from RestrictedPython import compile_restricted
from RestrictedPython.PrintCollector import PrintCollector
from RestrictedPython.Guards import safe_builtins

def evalPythonString(string):
	'''
	Executes strings of python code

	Takes in a string and evaluates it. 

	Returns a tuple of the print output and a dictionary of the variables as
	they existed at the end of the code execution
	'''
	string += "\ncodeShellOutput_ = printed\n"

	code = compile_restricted(string, '<string>', 'exec')

	restrictedScope = {'_print_':PrintCollector, '__builtins__':safe_builtins, \
		                'codeShellOutput_':''}
	restrictedScope['_getiter_'] = iter
	restrictedScope['__name__'] = '<string>'
	restrictedScope['_getattr_'] = getattr
	restrictedScope['_write_'] = lambda obj: obj
	codeOutput = ""
	try:
		exec(code, restrictedScope)
	
		codeOutput = restrictedScope['codeShellOutput_']
		del restrictedScope['codeShellOutput_']
		del restrictedScope['_print_']
		# These are apparently created by exec or something
		del restrictedScope['__builtins__']
		del restrictedScope['_print']
	except ImportError:
		codeOutput = "ImportError.  Importing is disallowed"

	return (codeOutput, restrictedScope)
