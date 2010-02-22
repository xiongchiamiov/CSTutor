''' @author James Pearson, Matt Tytel, John Hartquist, Jon Inloes '''

from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from courses.models import Course, Enrollment

def master_rtr(request, template, data = {}):
	if request.user.is_authenticated():
		# Since we're only grabbing the enrollments to get at the courses, 
		# doing select_related() will save us from having to hit database for
		# every course the user is enrolled in
		data['courses'] = \
			[e.course for e in \
			 Enrollment.objects.select_related().filter(user=request.user) \
			 if e.view]
	else:
		if "anonCourses" in request.session:
			data['courses'] = request.session['anonCourses']
		else:
			data['courses'] = []
	
	data['THEME'] = settings.THEME

	return render_to_response(template, data, context_instance=RequestContext(request))

def index(request):
	request.session.set_test_cookie()
	return master_rtr(request, 'index.html')

def show_help(request):
	'''
	Displays the help page
	'''
	return master_rtr(request, 'help/index.html')

def custom_404(request):
	response = master_rtr(request, '404.html')
	response.status_code = 404
	return response
