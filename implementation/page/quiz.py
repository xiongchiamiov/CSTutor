'''
quiz.py file for quiz related operations.

Contains operations for all quizzes.

Author(s): James Pearson

'''

def createQuiz(request):
	'''
	Takes a course as well as the form submitted containing the new quiz and creates a new Course page containing the quiz.

	Returns an http response for viewing the created quiz.
	'''
	pass

def deleteQuiz(request):
	'''
	Takes a course and a specified quiz and deletes the quiz from the course. It also deletes any corresponding statistics.
	
	Returns an http response for viewing the main course page.
	'''
	pass

def editQuiz(request):
	'''
	Takes an old Quiz, the Quiz containing the changes, as well as the course containing the quiz and merges the changes in the modified quiz into the old Quiz.
	
	Returns an http response for viewing the edited quiz.
	'''
	pass

def addQuestion(request):
	'''
	Takes the quiz being worked on and the question being added, and adds the question to the quiz.
	
	Returns an http response for viewing the edited quiz.
	'''
	pass

def removeQuestion(request):
	'''
	Takes the quiz being worked on and the question being removed, and removes the question from the quiz.
	
	Returns an http response for viewing the edited quiz.
	'''
	pass

def determinePath(quiz, score):
	'''
	Takes in the score of a quiz and then determines the right path for a student.
	
	Returns a Page.
	'''
	pass
