from django.utils import simplejson
from django.http import HttpResponse
from codeshell.pythoncode import evalPythonString

def execute(request):
	'''
		Executes python code
	'''
	try:
		result = evalPythonString(request.GET['code'])[0]
	except SyntaxError, e:
		result = str(e)
	# so... there are some things that we currently aren't dealing with,
	# as far as handlers for things in RestrictedPython
	# better not send a 500, as that'll just produce no result
	except Exception as e:
		#import pdb; pdb.set_trace()
		result = "Oops!  We weren't able to process your request, so please let your instructor know so we can fix it, mmk?"
	return HttpResponse(simplejson.dumps({'result': result}),
	                    mimetype='application/json')
