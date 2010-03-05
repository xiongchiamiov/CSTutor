'''
users.py handles all necessary user related functions not explicitly handled by the built in django user module.

Example functions include, login, registerNewUser, logout, profiles....

@author John Hartquist	
@author Russell Mezzetta
'''
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.forms.fields import email_re

# commented out by mgius on 2/16/10
#def editProfile(oldUser, newUser):
#   '''
#   This operation takes a users profile and any modifications and 
#   merges them together, returning an updated profile
#   '''
#   pass
#
#def logout(request):
#   '''
#   Logs a user out.
#   '''
#   
#   pass

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
	
def updateName(request):
	'''
	Updates a users name
	@author John Hartquist
	@pre request.POST["form"] == "Change Name"
	@post request.user.first_name = request.POST["first_name"]
	@post request.user.last_name = request.POST["last_name"]
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
	@author John Hartquist
	@pre request.POST["form"] == "Yes"
	@post user not in User.objects.all()
	'''
	request.user.delete()
	return 0


def changePassword(request):
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

def setInstructor(user, instructor):
   '''
   Grants a user permission to create a course
	TODO:
   '''
   pass

def registerNewUser(username, password, vpassword, firstName, lastName, email):
	'''
	@author Russell Mezzetta
	Registers a new user. 

	@pre: all inputs are strings

	@post: if return == 0: added user=username to the database 

   returns:
	   username not empty return 3
	   username not already taken return 1
	   password not empty return 4
	   password and vpassword match return 2
		First or last name empty return 5
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
	@author Russell Mezzetta
	This login wrapper logs the user in.
	pre: 	request is a request object
			username is a string
			password is a string

	post: username and password match a username/password in the system
	      username denotes an active account
	returns 0 on success, 1 invalid login, 2 inactive account
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

