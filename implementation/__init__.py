''' 
	CSTutor implementation in Python 2.5 with Django 1.0 web framework

	Packages used in the CSTutor are:
	codeshell
	courses
	home
	pages
	stats
	tinymce
	users

	Folder hierarchy defines packages.  
	Each package contains:
	<b>models.py<b>: Class definitions for persistent data structures
	<b>views.py<b>: functions called by the user by hitting various site URLs
	<b>classname.py<b>: methods for each class defined in models.py

	CSTutor uses the DJango testing suite for unit testing. This provides framework to write
	function unit tests, class-level inter-function testing, 
	system-level integration testing, and supports regression testing. 
	In other words, it can simluate front-end user interaction as well as back-end function testing.

	Our integration test plan is to run the websever and if any code is broken it will display an 
	error. 

@author Russell Mezzetta
@author Jon Inloes
@author Mark Gius
'''
