'''users/views.py - This is where all the profile pages are rendered
@author John Hartquist
@author Russell Mezzetta
'''
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from home.views import index
from user import registerNewUser, loginWrapper
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
	'''
	Logs out the current user
	@author John Hartquist
	@author Russell Mezzetta
	@pre
	@post request.user.is_authenticated() == false
	'''
	#russ--making logout not really log people out in certain cases
	if request.user.is_authenticated() == True:
		if 'rememberme' in request.session:
			if request.session['rememberme'] == True:
				#the user set remember me to true so don't log them out
				#logging a user out deletes session info
				print "rememberme"
				return render_to_response('user/logout.html')
		#decided to comment this out...if the user logs out it will at most remember their username
		#if they have set autologin then they shouldn't use logout!
		#if 'autologin' in request.session:
		#	if request.session['autologin'] == True:
		#		#the user set autologin to true so don't log them out
		#		return render_to_response('user/logout.html')
	print "blah"	
	logout(request)
	return render_to_response('user/logout.html')
	
def show_login(request):
	'''
	@author Russell Mezzetta
	This shows the login page and displays any errors.
	'''
	print 'in show_login'
	
	#before processing check if user's session has autologin/rememberme set
	#based on assumption that if we don't log the user out then they will stay authenticated
	if request.user.is_authenticated():
		print "user authenticated"
		if 'autologin' in request.session:
			if request.session['autologin'] == True:
				return index(request)

	if request.method == 'POST':
		#form was submitted
		username = request.POST['username']
		password = request.POST['password']
		#checkboxes don't put anything in post if they are unchecked so we have to do a little
		#extra work. This involves making a list of the possible checkboxes.
		checkboxList = request.POST.getlist('anonymous')
		checkboxList += request.POST.getlist('autologin')
		checkboxList += request.POST.getlist('rememberme')

		if "anonymous" in checkboxList:
			#bypass login
			#if the session has data in it, set it to false, set cookie to expire when browser closes
			request.session.set_expiry(0)
			if 'autologin' in request.session:
				request.session['autologin'] = False
			if 'rememberme' in request.session:
				request.session['rememberme'] = False
			return index(request)

		if "autologin" in checkboxList:
			print "autologin checked"
			#set cookie/session to expire in 2 weeks (1209600 is # of seconds in 2 weeks)
			request.session.set_expiry(1209600)
			request.session['autologin'] = True
			#request.session['password'] = password
		else:
			request.session['autologin'] = False

		if "rememberme" in checkboxList and "autologin" not in checkboxList:
			print "rememberme checked"
			#save this in their session(auto fill username)
			#set cookie/session to expire in 2 weeks (1209600 is # of seconds in 2 weeks)
			request.session.set_expiry(1209600)
			request.session['rememberme'] = True
			request.session['username'] = username
		else:
			request.session['rememberme'] = False
			request.session['username'] = ""
		
		ret = loginWrapper(request, username, password)
		if ret == 0:
			print "successful login"
			#call the index view ... this should be the equivalent of the homepage
			return index(request)
		elif ret == 1:
			# Return an 'invalid login' error message.
			print "invalid login"
			return render_to_response('user/login.html', {'message': "Please try again, Invalid Username/Password"})
		else:#ret == 2:
			# Return a 'disabled account' error message
			print "account marked as inactive"
			return render_to_response('user/login.html', {'message': "Account marked as inactive, contact System Admins"})
	else:
		#form has not yet been submitted (first time visiting login page)
		print 'GET'
		if 'username' in request.session:
			return render_to_response('user/login.html', {'loginusername':request.session['username']})
		else:
			return render_to_response('user/login.html')

def show_register_new_user(request):
	'''
	@author Russell Mezzetta
	This def shows the register new user page and registers the user
	'''
	print "in show_register_new_user"
	if request.method == 'POST':
		#form was submitted
		username = request.POST['username']
		password = request.POST['password']
		vpassword = request.POST['verifypassword']
		email = request.POST['email']
		#send form data to registerNewUser function
		ret = registerNewUser(username, password, vpassword, email)
		if ret == 0:
			#successful registration
			#return render_to_response('user/login.html', {'message': "User Registration Successful"})
			#TODO create a response like "success!"
			return HttpResponseRedirect('/login/')
		elif ret == 1:
			errorMsg = "That username is already taken"
		elif ret == 2:
			errorMsg = "Passwords do not match"
		elif ret == 3:
			errorMsg = "The username field is empty"
		else:#ret == 4
			errorMsg = "The password field is empty"
		return render_to_response('user/register-new-user.html', {'message': errorMsg})
	else:
		return render_to_response('user/register-new-user.html')

