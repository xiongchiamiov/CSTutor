'''
Functions that are useful for executing python.

This could be as simple as an "eval," but it is sometimes handy to do something
like sanitize code or capture output, etc, so we have a special execute
function that will abstract all that garbage out

POTENTIAL SECURITY RISK: These functions do not currently protect against 
importing python modules.

@author Mark Gius
@author James Pearson
'''


from RestrictedPython import compile_restricted
from RestrictedPython.PrintCollector import PrintCollector

def evalPythonString(string):
	'''
	Executes strings of python code

	Takes in a string and evaluates it. 

	Returns a tuple of the print output and a dictionary of the variables as
	they existed at the end of the code execution
	'''
	string += "\ncodeShellOutput_ = printed\n"

	code = compile_restricted(string, '<string>', 'exec')

	restrictedScope = {'_print_':PrintCollector, 'codeShellOutput_':''}
	exec(code, restrictedScope)
	
	codeOutput = restrictedScope['codeShellOutput_']
	del restrictedScope['codeShellOutput_']
	del restrictedScope['_print_']
	# These are apparently created by exec or something
	del restrictedScope['__builtins__']
	del restrictedScope['_print']

	return (codeOutput, restrictedScope)
