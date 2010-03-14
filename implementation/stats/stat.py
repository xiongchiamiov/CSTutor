# vim: set noet:
'''
stats.py

Contains a number of functions that manage and calculate user statistics. 
@author Andrew J. Musselman
'''
from models import Stat
from courses.models import Enrollment
from courses.models import Course
from django.db import connection, transaction

def dropAllUserStats(user):
	'''Drops all statistics assoicated with a user, reguardless of what course 
	the user is in.
	@precondition The User must exist
	@precondition User.models.get(user.id) = user
	@postcondition There should be no stats assoicated with the user in the DB
	@postcondition Stat.models.filter(user=user) = null set
	'''
	Stat.objects.filter(user=user).delete();


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
	                   maxscore, date  
                   FROM stats_stat 
                   INNER JOIN (select MAX(Cast(Score as FLOAT) 
				       / cast(maxscore as Float)) as inner_maxScore,
                       user_id as inner_user_id, page_id as inner_page_id,
				       course_id as inner_course_id
                       FROM stats_stat 
	                   WHERE course_ID=%s 
		               GROUP BY user_id, page_id, course_id) as best_scores
                   ON (Cast(score as FLOAT) / cast (maxscore as FLOAT)) = 
				       inner_maxscore and
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
	contains the 'page_slug', and the 'page_name' for the quiz, along with
	the quiz's 'result_count', 'result_min', 'result_max' and 'result_avg'.
	
	@postcondition Returns aggrigates for the best scores in each 
	@postcondition for quiz in course.enrollmet:
						aggrigateDist['page_name'] = (page_name)
	                    aggrigateDict['result_avg'] = 
						     (sum(best scores)/count(best scores)
	                    aggrigateDict['result_max'] =  max(best scores)
	                    aggrigateDict['result_min'] =  min(best scores)
	                    aggrigateDict['result_count'] = count(best scores)
	'''
	cursor = connection.cursor()
	cursor.execute('''SELECT pages_page.slug,
	                    pages_page.name,
						count(*),
	                    max(Cast(score as FLOAT)/cast(maxscore as Float)),
	                    min(Cast(score as FLOAT)/cast(maxscore as Float)),
	                    avg(Cast(score as FLOAT)/cast(maxscore as Float))
                   FROM (stats_stat 
                         INNER JOIN (select MAX(Cast(Score as FLOAT) 
	                /cast (maxscore as Float)) as inner_maxscore,
                              user_id as inner_user_id, 
	                      page_id as inner_page_id,
		              innerStats.course_id as inner_course_id
                              FROM stats_stat as innerStats 
	                          WHERE innerStats.course_id=%s 
	                          GROUP BY user_id, page_id, course_id) as
							      best_score
	                          ON (Cast(score as FLOAT) / cast (maxscore as FLOAT)) = 
				         inner_maxscore and
	                         user_id = inner_user_id AND 
	                         page_id = inner_page_id and 
	                         course_id = inner_course_id ) as best_stats
	                INNER JOIN pages_page ON
	                    pages_page.id = page_id
	                    WHERE best_stats.inner_course_id = %s
	                    GROUP BY page_id,pages_page.slug,pages_page.name ;
	               ''',[course.id,course.id] )
	rawList = cursor.fetchall()
	aggrigateList = []
	for listItem in rawList:
		aggrigateDict = {'page_slug':listItem[0],
		                 'page_name':listItem[1],
		                 'result_count':listItem[2],
		                 'result_max':listItem[3]*100,
		                 'result_min':listItem[4]*100,
		                 'result_avg':listItem[5]*100}
		aggrigateList.append(aggrigateDict)
	return aggrigateList; 

def getUserBestAggregates(course):
	'''
	Calculates the aggregate stats for the best results for each user
	in a course. This will run even if there are no stats.
	@precondition Course exists
	@precondition Course.objects.get(course) != null
	@postcondition For each user in the course, return a dictionary of their
	               aggregates
	@postcondition for user in course.enrollmet:
						aggrigateDist['user_id'] = (user.id)
	                    aggrigateDict['result_avg'] = 
						     (sum(best scores)/count(best scores)
	                    aggrigateDict['result_max'] =  max(best scores)
	                    aggrigateDict['result_min'] =  min(best scores)
	                    aggrigateDict['result_count'] = count(best scores)
	'''

	cursor = connection.cursor()
	cursor.execute('''SELECT user_id, username,
						count(),
	                    max(Cast(score as FLOAT)/cast(maxscore as Float)),
	                    min(Cast(score as FLOAT)/cast(maxscore as Float)),
	                    avg(Cast(score as FLOAT)/cast(maxscore as Float))
                   FROM (stats_stat 
                         INNER JOIN (select MAX(Cast(Score as FLOAT) 
	                /cast (maxscore as Float)) as inner_maxscore,
                              user_id as inner_user_id, 
	                      page_id as inner_page_id,
		              innerStats.course_id as inner_course_id
                              FROM stats_stat as innerStats 
	                          WHERE innerStats.course_id=%s 
	                          GROUP BY user_id, page_id, course_id) as
							      best_score
	                          ON (Cast(score as FLOAT) / cast (maxscore as FLOAT)) = 
				         inner_maxscore and
	                         user_id = inner_user_id AND 
	                         page_id = inner_page_id and 
	                         course_id = inner_course_id ) as best_stats
	                INNER JOIN auth_user ON
					    user_id = auth_user.id    
	                WHERE best_stats.inner_course_id = %s
	                    GROUP BY user_id,username ;
	               ''',[course.id,course.id] )
	rawList = cursor.fetchall()
	aggrigateList = []
	for listItem in rawList:
		aggrigateDict = {'user_id':listItem[0],
		                 'user_name':listItem[1],
		                 'result_count':listItem[2],
		                 'result_max':listItem[3]*100,
		                 'result_min':listItem[4]*100,
		                 'result_avg':listItem[5]*100}
		aggrigateList.append(aggrigateDict)
	return aggrigateList; 


def getUserBestScore(user, quiz):
	'''
	Gets the best score for a given user on a given quiz. Takes a user and 
    the page where a quiz is located. Returns the percentage of the best
    score.
	'''
	stat = Stats.objects.filter(page=quiz, user=user).sort("-score")[0]
	return (stat.score/stat.maxScore)



