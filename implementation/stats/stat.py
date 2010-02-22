'''
stats.py

Contains a number of functions that manage and calculate user statistics. 
@author Andrew J. Musselman
'''
from models import Stat
from courses.models import Enrollment
from courses.models import Course
from django.db.models import Avg, Max, Min, Count
from django.db import connection, transaction


def getAllCourseStats(course):
	'''
	Get the a list of all user statistics in from a given course. A user 
	may have many stats for each quiz, since a user may take a quiz
	many times
	'''
	statsList = Stats.object.get(course=course)
	return statsList

def getBestCourseStats(course):
	'''
	Get the list of the best statistics for every quiz in a given course.
	There will be at most ONE stat per quiz per user.  
	'''
	cursor = connection.cursor()
	cursor.execute('''SELECT id, course_id, user_id, page_id, score, 
	                   maxScore, date  
                   FROM stats_stat 
                   INNER JOIN (select MAX(Cast(Score as FLOAT) 
				       /cast (maxScore as Float)) as inner_maxScore,
                       user_id as inner_user_id, page_id as inner_page_id,
				       course_id as inner_course_id
                   FROM stats_stat 
	               WHERE course_ID=%s 
		           GROUP BY user_id, page_id, course_id)
                   ON (Cast(score as FLOAT) / cast (maxScore as FLOAT)) = 
				       inner_maxScore and
                       user_id = inner_user_id AND 
					   page_id = inner_page_id and 
                       course_id = inner_course_id
                   WHERE course_id = %s;
	               ''',[course.id,course.id] )
	rawList = cursor.fetchall()
	return rawList
	
def getQuizBestAggregates(course):
	'''	
	Gets the aggrigate data for each quiz in a course. This should return
	a list of dictionaries, one for each quiz in the course. Each dictionary
	contains the 'page_slug', and the 'page_name' for the quiz, along with the quiz's 
	'result_count', 'result_min', 'result_max' and 'result_avg'.
	'''
	cursor = connection.cursor()
	cursor.execute('''SELECT pages_page.slug,
	                    pages_page.name,
						count(*),
	                    max(Cast(score as FLOAT)/cast(maxScore as Float)),
	                    min(Cast(score as FLOAT)/cast(maxScore as Float)),
	                    avg(Cast(score as FLOAT)/cast(maxScore as Float))
                   FROM (stats_stat 
                         INNER JOIN (select MAX(Cast(Score as FLOAT) 
				              /cast (maxScore as Float)) as inner_maxScore,
                              user_id as inner_user_id, 
							  page_id as inner_page_id,
				              innerStats.course_id as inner_course_id
                              FROM stats_stat as innerStats 
	                          WHERE inner_course_ID=%s 
		                      GROUP BY user_id, page_id, course_id)
                         ON (Cast(score as FLOAT) / cast (maxScore as FLOAT)) = 
				         inner_maxScore and
                         user_id = inner_user_id AND 
					     page_id = inner_page_id and 
                         course_id = inner_course_id ) as best_stats
				        INNER JOIN pages_page ON
						pages_page.id = page_id
                   WHERE best_stats.course_id = %s
				   GROUP BY page_id;
	               ''',[course.id,course.id] )
	rawList = cursor.fetchall()
	aggrigateList = []
	for listItem in rawList:
		aggrigateDict = {'page_slug':listItem[0],
		                 'page_name':listItem[1],
		                 'result_count':listItem[2],
		                 'result_max':listItem[3],
		                 'result_min':listItem[4],
		                 'result_avg':listItem[5]}
		aggrigateList.append(aggrigateDict)
	return aggrigateList; 

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

def getUserAverageScore(user,quiz):
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

