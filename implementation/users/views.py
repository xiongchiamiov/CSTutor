'''users/views.py - This is where all the profile pages are rendered'''
# @author John Hartquist

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from home.views import index
from django.forms.fields import email_re

def show_profile(request):
	'''
	Displays the profile of the user that is currently logged in
	'''
	#print 'in show_profile'

	#make sure user is logged in
	if request.user.is_authenticated():
		#check if method was post
		if (request.method=="POST"):
			if (request.POST["form"] == "Change E-mail"):
				email = request.POST["email"]
				if (email_re.match(email)):
					request.user.email = email
					request.user.save()
				else:
					return render_to_response('user/profile.html', 
		                                       {'user': request.user,
											    'emailError': "Invalid E-mail Address"})
				
			if (request.POST["form"] == "Change Password"):
				oldpass = request.POST["oldpass"]
				newpass1 = request.POST["newpass1"]
				newpass2 = request.POST["newpass2"]
				if (request.user.check_password(oldpass) == False):
					return render_to_response('user/profile.html', 
		                                       {'user': request.user,
											    'passError': "Incorrect current password"})
													   
				if (newpass1 != newpass2):
					return render_to_response('user/profile.html', 
		                                       {'user': request.user,
											    'passError': "Password do not match"})
					
				request.user.set_password(newpass1)
				request.user.save()				    
		
		
		
		return render_to_response('user/profile.html', {'user':request.user})
	else:
		return render_to_response('user/notloggedin.html')
		
	
	
	
def show_logout(request):
	#print 'in show_logout'
	
	logout(request)
	return render_to_response('user/logout.html');
	
def show_login(request):
	#print 'in show_login'
	
	if request.method == 'POST':
		#form was submitted
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				# Redirect to a success page.
				#print "successful login"
				#call the index view ... this should be the equivalent of the homepage
				return index(request)
			else:
				# Return a 'disabled account' error message
				#print "account marked as inactive"
				return render_to_response('user/login.html', {'message': "Account marked as inactive, contact System Admins"})
		else:
			# Return an 'invalid login' error message.
			#print "invalid login"
			return render_to_response('user/login.html', {'message': "Please try again, Invalid Username/Password"})
	#else:
		#form has not yet been submitted (first time visiting login page)
		#print 'GET'
	return render_to_response('user/login.html')
