'''The profile section of the CSTutor - name and functions subject to change as we are going to use the build-in Django user management

@author John Hartquist	
@author Russell Mezzetta
'''
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.forms.fields import email_re

def editProfile(oldUser, newUser):
   '''
   This operation takes a users profile and any modifications and 
   merges them together, returning an updated profile
   '''
   pass

def logout(request):
   '''
   Logs a user out.
   '''
   
   pass

def updateEmail(request):
	'''
	Updates a users e-mail address
	@author John Hartquist
	@pre request.POST["form"] == "Change E-mail"
	@post request.user.email = email
	'''
        email = request.POST["email"]
	if (email_re.match(email)):
		request.user.email = email
		request.user.save()
                #success 
		return 0
	else:
		#failure
		return 1


def removeUser(username, userDB):
   '''
   Removes the given user from the user database
   '''
   pass


def setInstructor(user, instructor):
   '''
   Grants a user permission to create a course
   '''
   pass

def registerNewUser(username, password, vpassword, email):
	'''
	@author Russell Mezzetta
	Registers a new user. 

	pre: username not empty return 3
	     username not already taken return 1
	     password not empty return 4
	     password and vpassword match return 2
	post: none

	Tests:
	inputs                              outputs
	("", "", "", "")	                  3
	("blah", "", "", "")                4
	("blah", "pass", "some", "")        2
	("blah", "pass", "pass", "myemail") 0
	("blah", "xyx", "xyx", "mailxyx")   1
	
	First checks for valid username.
	Returns 0 on success, 1 if username already exists, 2 if passwords don't match
	3 if the username is empty, 4 if the password(s) is/are empty.
	'''

	#TODO do we need to do anything special with username/password characters or length?

	print "in users.user.registerNewUser"
	#check that username isn't empty
	if len(username) <= 0:
		print "username is empty"
		return 3
	#check that password isn't empty
	if len(password) <= 0:
		print "password is empty"
		return 4
	#check that passwords match
	if password != vpassword:
		print "passwords don't match"
		return 2
	#check that the username does not already exist
	try:
		User.objects.get(username = username)
		print "username already exists"
		return 1
	except User.DoesNotExist:
		print "username is not taken, hurrah!"
		
	#no errors, create and save user, return 0
	user = User.objects.create_user(username, email, password)
	user.save()
	return 0

def loginWrapper(request, username, password):
	'''
	@author Russell Mezzetta
	This login wrapper logs the user in.
	pre: none
	post: username and password match a username/password in the system
	      username denotes an active account
	returns 0 on success, 1 invalid login, 2 inactive account
	'''
	user = authenticate(username=username, password=password)
	if user is not None:
		if user.is_active:
			login(request, user)
			# Redirect to a success page.
			print "successful login"
			return 0
		else:
			# Return a 'disabled account' error message
			print "account marked as inactive"
			return 2
	else:
		# Return an 'invalid login' error message.
		print "invalid login"
		return 1

