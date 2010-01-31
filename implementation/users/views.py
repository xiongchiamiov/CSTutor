'''users/views.py - This is where all the profile pages are rendered'''
# @author John Hartquist

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from home.views import index


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
def show_login(request):
	print 'in show_login'
	
	if request.method == 'POST':
		#form was submitted
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				# Redirect to a success page.
				print "successful login"
				#call the index view ... this should be the equivalent of the homepage
				return index(request)
			else:
				# Return a 'disabled account' error message
				print "account marked as inactive"
				return render_to_response('user/login.html', {'message': "Account marked as inactive, contact System Admins"})
		else:
			# Return an 'invalid login' error message.
			print "invalid login"
			return render_to_response('user/login.html', {'message': "Please try again, Invalid Username/Password"})
	else:
		#form has not yet been submitted (first time visiting login page)
		print 'GET'
	return render_to_response('user/login.html')


