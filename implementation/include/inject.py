'''
Definition for Class Injection Decorator

@author: Mark Gius

'''
def inject(Class):
	''' Decorator to Inject the function into the provided class

		 For info on how this works, consider reading 
		 http://www.linuxtopia.org/online_books/programming_books/python_programming/python_ch26.html

		 @author: Mark Gius

	'''
	def injectInner(function):
		try:
			Class.__dict__[function.__name__]
		except KeyError:
			print "Attaching " + function.__name__
			setattr(Class, function.__name__, function)
		return function
	return injectInner

def injectstatic(Class):
	''' Decorator to Inject the function into the provided class as a static 
		 method instead of an instance method
	'''

	def injectInner(function):
		try:
			Class.__dict__[function.__name__]
		except KeyError:
			print "Attaching " + function.__name__
			setattr(Class, function.__name__, staticmethod(function))
		return staticmethod(function)
	return injectInner
