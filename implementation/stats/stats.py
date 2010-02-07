'''
stats.py

Contains a number of functions that manage and calculate user statistics. 
@author Andrew J. Musselman
'''
from models import Stat

def clearStats(stats):
	'''
	Clear a set of statistics.
	'''
	pass

def getStats(roster):
	'''
	Get the statistics for a class from the roster
	'''
	pass 

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

