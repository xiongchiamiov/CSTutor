'''
quiz.py file for quiz related operations.

Contains operations for all quizzes.

Author(s): James Pearson

'''

from pages.quiz.models import *

def CreateQuiz():
	'''
		Creates a new quiz object and returns it to the user

		This method is provided to maintain consistent behavior across
		models
	'''
	return Quiz()

def checkAnswers(answers, user = None)
	'''
	Given a set of answers from the user, checks those answers against the 
	solution, returning a list of tuples, where each tuple is of the form
	(boolean, correctanswer), indicating whether or not the user got that
	question right and the correct answer for that question

	If a user is provided, store a stats entry for this user/quiz

	Returning the answers here because we're going to have to pull them from
	the database anyway, and if the caller is going to use them, we can save
	a potentially expensive database operation.
	'''
	pass

def determinePath(quiz, score):
	'''
	Takes in the score of a quiz and then determines the right path for a 
	student.
	
	Returns a Page.
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

