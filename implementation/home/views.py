from django.shortcuts import render_to_response
from courses.models import Course

def index(request):
	data = {}
	data['courses'] = Course.objects.all()
	request.session.set_test_cookie()
	return render_to_response('index.html', data)
