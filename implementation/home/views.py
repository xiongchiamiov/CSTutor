''' @author James Pearson, Matt Tytel '''

from django.shortcuts import render_to_response
from courses.models import Course

def master_rtr(request, template, data = {}):
	data['courses'] = [e.course for e in request.user.enrollments.all()]
	print data['courses']
   # commented by mgius.  Breaks test suite!!
   #import pdb; pdb.set_trace()

	return render_to_response(template, data)

def index(request):
	request.session.set_test_cookie()
	return master_rtr(request, 'index.html')
