''' @author James Pearson, Matt Tytel '''

from django.shortcuts import render_to_response
from django.template import RequestContext
from courses.models import Course

def master_rtr(request, template, data = {}):
	if request.user.is_authenticated():
		data['courses'] = [e.course for e in request.user.enrollments.all()]
	else:
		data['courses'] = []

	return render_to_response(template, data, context_instance=RequestContext(request))

def index(request):
	request.session.set_test_cookie()
	return master_rtr(request, 'index.html')
