'''
users.py handles all necessary user related functions not explicitly handled by the built in django user module.

Example functions include, login, registerNewUser, logout, profiles....

@author John Hartquist	
@author Russell Mezzetta
'''
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.forms.fields import email_re
from users.models import UserLastViewed

def updateEmail(request):
	'''
	Updates a users e-mail address

	@pre request.POST["form"] == "Change E-mail"
	@post request.user.email = email

	@author John Hartquist
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
	
def updateName(request):
	'''
	Updates a users name

	@pre request.POST["form"] == "Change Name"
	@post request.user.first_name = request.POST["first_name"]
	@post request.user.last_name = request.POST["last_name"]

	@author John Hartquist
 	'''
 	user = request.user
 	if (request.POST["first_name"] == ""):
 		return 1
 	elif (request.POST["last_name"] == ""):
 		return 1
  	else:
 		user.first_name = request.POST["first_name"]
 		user.last_name = request.POST["last_name"]
 		user.save()
 		return 0
 	
def deleteUser(request):
	'''
	Deletes a user account

	@pre request.POST["form"] == "Yes"
	@post user not in User.objects.all()

	@author John Hartquist
	'''
	request.user.delete()
	return 0


def changePassword(request):
	'''
	Changes a user's password

	@author John Hartquist
	'''
	oldpass = request.POST["oldpass"]
	newpass1 = request.POST["newpass1"]
	newpass2 = request.POST["newpass2"]
	if (request.user.check_password(oldpass) == False):
	  #invalid password
	  return 1
		                                              
	if (newpass1 != newpass2):
	  #passwords don't match
	  return 2

	request.user.set_password(newpass1)
	request.user.save()
	return 0


def registerNewUser(username, password, vpassword, firstName, lastName, email):
	'''
	Registers a new user. 

	@pre: all inputs are strings

	@post: if return == 0: added user=username to the database 

   returns:
	   username not empty return 3
	   username not already taken return 1
	   password not empty return 4
	   password and vpassword match return 2
		First or last name empty return 5

	@author Russell Mezzetta
	'''
	#check that username isn't empty
	if len(username) <= 0:
		#print "username is empty"
		return 3
	#check that password isn't empty
	if len(password) <= 0:
		#print "password is empty"
		return 4
	#check that first/last name aren't empty
	if (len(firstName) <= 0) or (len(lastName) <= 0):
		return 5
	#check that passwords match
	if password != vpassword:
		#print "passwords don't match"
		return 2
	#check that the username does not already exist
	try:
		User.objects.get(username = username)
		#print "username already exists"
		return 1
	except User.DoesNotExist:
		#print "username is not taken, hurrah!"
		
		#no errors, create and save user, return 0
		user = User.objects.create_user(username, email, password)
		user.first_name = firstName
		user.last_name = lastName
		user.save()
		return 0

def loginWrapper(request, username, password):
	'''
	This login wrapper logs the user in.
	pre: 	request is a request object
			username is a string
			password is a string

	post: if username and password match a username/password in the system
	      and username denotes an active account then user is "logged in"
	returns 0 on success, 1 invalid login, 2 inactive account

	@author Russell Mezzetta
	'''
	user = authenticate(username=username, password=password)
	if user is not None:
		if user.is_active:
			login(request, user)
			# Redirect to a success page.
			#print "successful login"
			return 0
		else:
			# Return a 'disabled account' error message
			#print "account marked as inactive"
			return 2
	else:
		# Return an 'invalid login' error message.
		#print "invalid login"
		return 1

def saveLastViewed(user, courseSlug, pageSlug, editBool=False):
	'''
	This login wrapper logs the user in.
	pre: 	user is a User object
			courseSlug is a string
			pageSlug is a string
			editBool is a boolean

	returns a tuple (courseSlug, pageSlug, editBool)

	@author Russell Mezzetta
	'''

	if user.lastviewed.all().count() == 0:
		#user doesn't have a last viewed yet
		UserLastViewed(user=user,\
							courseSlug=courseSlug,\
							pageSlug=pageSlug,\
							editBool=editBool).save()
	else:
		lv = user.lastviewed.all()[0]
		lv.courseSlug=courseSlug
		lv.pageSlug=pageSlug
		lv.editBool=editBool
		lv.save()

	return (courseSlug, pageSlug, editBool)

def getLastViewed(user):
	'''
	This login wrapper logs the user in.
	pre: 	user is a User object

	returns a tuple (courseSlug, pageSlug, editBool) on success
						 (none, none, none) on failure

	@author Russell Mezzetta
	'''

	if user.lastviewed.all().count() == 0:
		#user doesn't have a last viewed yet
		return (None, None, None)
	else:
		lv = user.lastviewed.all()[0]
		return (lv.courseSlug, lv.pageSlug, lv.editBool)
