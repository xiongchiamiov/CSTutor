# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.models import User

def show_profile(request):
	print 'in show_profile'

	if request.method == 'POST':
		usr = request.POST['username']

	try:
		user = User.objects.get(username=usr)
			return render_to_response('user/profile.html', {'user':user})
		except User.DoesNotExist:
			return render_to_response('user/notfound.html')
	else:
		return render_to_response('user/lookup.html')
