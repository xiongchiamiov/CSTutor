''' @author James Pearson, Matt Tytel '''

from django.shortcuts import render_to_response
from django.template import RequestContext
from courses.models import Course, Enrollment

def master_rtr(request, template, data = {}):
	if request.user.is_authenticated():
      # Since we're only grabbing the enrollments to get at the courses, 
      # doing select_related() will save us from having to hit database for
      # every course the user is enrolled in
		data['courses'] = \
			[e.course for e in Enrollment.objects.select_related().filter(user=request.user)]
			#[e.course for e in request.user.enrollments.select_related().all()]
	else:
		data['courses'] = []

	return render_to_response(template, data, context_instance=RequestContext(request))

def index(request):
	request.session.set_test_cookie()
	return master_rtr(request, 'index.html')
