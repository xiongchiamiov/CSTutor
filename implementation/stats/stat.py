'''
stats.py

Contains a number of functions that manage and calculate user statistics. 
@author Andrew J. Musselman
'''
from models import Stat
from courses import Enrollment
from courses import Course

def clearStats(stats):
	'''
	Clear a set of statistics.
	'''
	pass

def getStats(roster):
	'''
	Get the statistics for a class from the roster
	'''
	#TODO/FIXME: What is a roster?
	pass

def getAllUserStats(course):
	'''
	Get the a list of all user statistics in from a givne course
	'''
	statsList = Stats.object.get(course=course)
	return statsList
	

def insertStat(course, page, score, user, date):
	'''
	Creates a new stat from the given information and inserts it into
	the database.
	'''
	stat = Stat(course=course, page=page, score=score, user=user, date=date)
	stat.save()

def getUserAggregate(user, course):
	'''
	Calculates aggregate stats for a single user in a particular
	course
	'''
	pass

def getUserLatestWeightedAverage(user, couse):
	'''
	Calculates the weighted average of the users latest scores that the
	user has posted for each quiz. This does not count quizzes the user 
	hasn't taken yet.
	'''
	pass

def getUserBestWeightedAverage(user, course):
	'''
	Calculates the weighted average of the best scores that the user has posted
	for each quiz. This does not count quizzes the user hasn't taken yet
	'''
	pass

def getUserBestScore(user, quiz):
	'''
	Gets the best score for a given user on a given quiz
	'''
	pass

def getUserLatestScore(user,quiz):
	'''
	Gets the latest score for a given user on a given quiz.
	'''
	pass

def getUserAverageScore(user,quiz)
	'''
	Gets the average score for a given user on a given quiz.
	Note that weighting makes no sense for this use case, as the max score for a
	quiz should be the same each time you take it.
	'''
	pass

def getCourseLatestAverage(course, quiz):
	'''
	Gets the average score for the the latest quiz results for a given quiz.
	Note that weighting makes no sense for this use case, as the max score for a
	quiz should be the same each time you take it.
	'''
	pass

def getCourseBestAverage(course, quiz):
	'''
	Gets the average score of the best quiz results for a given quiz.
	Note that weighting makes no sense for this use case, as the max score for a
	quiz should be the same each time you take it.
	'''
	pass

def getCourseAggregates(course):
	'''
	Calculate aggragte stats for all users in a particular course
	'''
	pass


def removeStat(stat, user):
	'''
	Removes a stat from a user
	'''
	pass

def purgeDeadStats():
	'''
	Removes stats that have no associated Page/User
	'''
	pass 

