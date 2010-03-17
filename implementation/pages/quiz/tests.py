'''
This file contains tests for the Quiz package. 

@author Evan Kleist
'''

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.contrib.auth.models import AnonymousUser
from pages.quiz.models import *
from pages.quiz.quiz import *
from pages.quiz.question.models import *
from django.core.handlers.wsgi import WSGIRequest
from users.models import *
from django.core.urlresolvers import reverse

class QuizUnitTests(TestCase):
	'''
		Unit Tests on backend quiz operations.

		@author Evan Kleist
	'''
	fixtures = ['QuizUnitTests']

	def setUp(self):
		'''
			Set up the tests
	
			@author Evan Kleist
		'''
		self.courseSlug = 'quizunittest_course'
		self.quizSlug1 = 'quizunittests_quiz1'
		self.quizSlug2 = 'quizunittests_quiz2'
		self.quizSlug3 = 'quizunittests_quiz3'

	def test_addCodeQuestion(self):
		'''
			Test that adding a code question to a quiz works as expected

			Case no.    Input                                     Expected Output                           Remark
			1           questionCount, newQuestionCount           questionCount + 1 == questionCount        Ensure that 1 new question has been added
			2           newQuestion.order, newQuestionCount       newQuestion.order == newQuestionCount     Ensure that the new question is the last question
			3           newQuestion.text                          newQuestion.text == "Blank Question"      Ensure that the new question is indeed a new question       
			@author Evan Kleist        
		'''
		quiz = Quiz.objects.get(slug=self.quizSlug1)
		questionCount = len(quiz.questions.all())

		# Add a question to the quiz
		newQuestion = addCodeQuestion(quiz)

		# Case 1
		newQuestionCount = len(quiz.questions.all())
		self.failUnlessEqual(questionCount + 1, newQuestionCount)

		# Case 2
		self.failUnlessEqual(newQuestion.order, newQuestionCount)

		# Case 3
		self.failUnlessEqual(newQuestion.text, "")

	def test_addMultipleChoiceQuestion(self):
		'''
			Test that adding a multiple choice question to a quiz works as expected

			Case no.    Input                                     Expected Output                           Remark
			1           questionCount, newQuestionCount           questionCount + 1 == questionCount        Ensure that 1 new question has been added
			2           newQuestion.order, newQuestionCount       newQuestion.order == newQuestionCount     Ensure that the new question is the last question
			3           newQuestion.text                          newQuestion.text == "Blank Question"      Ensure that the new question is indeed a new question  

			@author Evan Kleist             
		'''
		quiz = Quiz.objects.get(slug=self.quizSlug1)
		questionCount = len(quiz.questions.all())

		# Add a question to the quiz
		newQuestion = addMultipleChoiceQuestion(quiz)

		# Case 1
		newQuestionCount = len(quiz.questions.all())
		self.failUnlessEqual(questionCount + 1, newQuestionCount)

		# Case 2
		self.failUnlessEqual(newQuestion.order, newQuestionCount)

		# Case 3
		self.failUnlessEqual(newQuestion.text, "")

	def test_addPath(self):
		'''
			Test that addPath successfulyl adds a path
			or returns the appropriate errors

			Case no.    Input               Expected Output                                    Remark
			1           lowscore = -1       errors = ["Low Score must be between 0 and 100"]   Low Score < 0
			2           lowscore = 101      errors = ["Low Score must be between 0 and 100",   Low Score > 100
			                                          "Low Score must be less than or equal 
			                                           to High Score"]
			3           lowscore = "a"      errors = ["Low Score must be an integer"]          Low Score invalid
			4           highscore = -1      errors = ["High Score must be between 0 and 100"   High Score < 0
			                                         , "Low Score must be less than or equal
			                                            to High Score"]
			5           highscore = 101     errors = ["High Score must be between 0 and 100"]  High Score > 100
			6           lowscore = 50       errors = ["Low Score must be less than or equal    High Score < Low Score
			            highscore = 0                  to High Score"]
			7           highscore = "abc"   errors = ["High Score must be an integer"]         High Score invalid
			8           lowscore = 0        errors = []                                        Successfully add path
			            highscore = 100     quiz.paths.contains(newPath)
			            toPage = quiz1
			            dialogue = "test"
			            passing = True
			9           lowscore = 0        errors = ["A path that matches this range          Duplicate path
			            highscore = 100                exists already"]
			            toPage = quiz1
			            dialogue = "test"
			            passing = True

			@author Evan Kleist
		'''
		quiz = Quiz.objects.get(slug = self.quizSlug3 + "_workingCopy")
		environ = {
			'HTTP_COOKIE': self.client.cookies,
			'PATH_INFO': '/',
			'QUERY_STRING': '',
			'REQUEST_METHOD': 'GET',
			'SCRIPT_NAME': '',
			'SERVER_NAME': 'testserver',
			'SERVER_PORT': 80,
			'SERVER_PROTOCOL': 'HTTP/1.1',
		}
		environ.update(self.client.defaults)

		customRequest = WSGIRequest(environ)
		
		# Case 1
		customRequest.POST = {'LowScore':-1, 'HighScore':100, 'pathPage':self.quizSlug1, 'passing':'on', 'dialogue':'test'}
		errors = addPath(quiz, customRequest, self.courseSlug)
		self.failUnlessEqual(errors, ["Low Score must be between 0 and 100"])

		# Case 2
		customRequest.POST = {'LowScore':101, 'HighScore':100, 'pathPage':self.quizSlug1, 'passing':'on', 'dialogue':'test'}
		errors = addPath(quiz, customRequest, self.courseSlug)
		self.failUnlessEqual(errors, ["Low Score must be between 0 and 100", "Low Score must be less than or equal to High Score"])

		# Case 3
		customRequest.POST = {'LowScore':"a", 'HighScore':100, 'pathPage':self.quizSlug1, 'passing':'on', 'dialogue':'test'}
		errors = addPath(quiz, customRequest, self.courseSlug)
		self.failUnlessEqual(errors, ["Low Score must be an integer"])

		# Case 4
		customRequest.POST = {'LowScore':0, 'HighScore':-1, 'pathPage':self.quizSlug1, 'passing':'on', 'dialogue':'test'}
		errors = addPath(quiz, customRequest, self.courseSlug)
		self.failUnlessEqual(errors, ["High Score must be between 0 and 100", "Low Score must be less than or equal to High Score"])

		# Case 5
		customRequest.POST = {'LowScore':0, 'HighScore':101, 'pathPage':self.quizSlug1, 'passing':'on', 'dialogue':'test'}
		errors = addPath(quiz, customRequest, self.courseSlug)
		self.failUnlessEqual(errors, ["High Score must be between 0 and 100"])

		# Case 6
		customRequest.POST = {'LowScore':50, 'HighScore':0, 'pathPage':self.quizSlug1, 'passing':'on', 'dialogue':'test'}
		errors = addPath(quiz, customRequest, self.courseSlug)
		self.failUnlessEqual(errors, ["Low Score must be less than or equal to High Score"])

		# Case 7
		customRequest.POST = {'LowScore':0, 'HighScore':"abc", 'pathPage':self.quizSlug1, 'passing':'on', 'dialogue':'test'}
		errors = addPath(quiz, customRequest, self.courseSlug)
		self.failUnlessEqual(errors, ["High Score must be an integer"])

		# Case 8
		customRequest.POST = {'LowScore':0, 'HighScore':100, 'pathPage':self.quizSlug1, 'passing':'on', 'dialogue':'test'}
		errors = addPath(quiz, customRequest, self.courseSlug)
		self.failUnlessEqual(errors, [])
		try:
			path = quiz.paths.get(lowscore = 0)
			self.failUnlessEqual(1,1)
		except Path.DoesNotExist:
			self.failUnlessEqual(0,1, "The path didnt get added")
		self.failUnlessEqual(path.lowscore, 0)
		self.failUnlessEqual(path.highscore, 100)
		self.failUnlessEqual(path.text, "test")
		self.failUnlessEqual(path.passed, True)
		self.failUnlessEqual(path.toPage, Page.objects.get(slug=self.quizSlug1))

		# Case 9
		customRequest.POST = {'LowScore':0, 'HighScore':100, 'pathPage':self.quizSlug1, 'passing':'on', 'dialogue':'test'}
		errors = addPath(quiz, customRequest, self.courseSlug)
		self.failUnlessEqual(errors, ["A path that matches this range exists already"])

	def test_checkPrerequisites(self):
		'''
			Test that 

			Case no.  Input                                        Expected Output   Remark
			1         quiz = quiz1                                 True              No prerequisites
			2         quiz = checkPrerequisites_quiz               False             User not logged in, quiz has prereqs
			          user = anonymous
			3         quiz = checkPrerequisites_quiz               False             User logged in, hasnt submitted quiz
			          user = testuser
			4         quiz = checkPrerequisites_quiz               False             User logged in, failed quiz
			          user = testuser
			5         quiz = checkPrerequisites_quiz               True              User logged in, passed quiz
			          user = testuser

			@author Evan Kleist
		'''
		self.client.login(username="testuser", password="password")
		url = "/course/" + self.courseSlug + "/page/" + self.quizSlug1 + "/submitQuiz/"
		
		# Case 1
		quiz = Quiz.objects.get(slug=self.quizSlug2)
		user = AnonymousUser()
		result = checkPrerequisites(quiz, user)
		self.failUnlessEqual(result, True)

		# Case 2
		quiz = Quiz.objects.get(slug="checkprerequisites_quiz")
		user = AnonymousUser()
		result = checkPrerequisites(quiz, user)
		self.failUnlessEqual(result, False)

		# Case 3
		quiz = Quiz.objects.get(slug="checkprerequisites_quiz")
		user = User.objects.get(username="testuser")
		result = checkPrerequisites(quiz, user)
		self.failUnlessEqual(result, False)

		# Case 4
		quiz = Quiz.objects.get(slug="checkprerequisites_quiz")
		user = User.objects.get(username="testuser")
		response = self.client.post(reverse('pages.quiz.views.submitQuiz', args=[self.courseSlug, self.quizSlug1]), {})
		result = checkPrerequisites(quiz, user)
		self.failUnlessEqual(result, False)

		# Case 5
		quiz = Quiz.objects.get(slug="checkprerequisites_quiz")
		user = User.objects.get(username="testuser")
		response = self.client.post(reverse('pages.quiz.views.submitQuiz', args=[self.courseSlug, self.quizSlug1]), {'mcq1':1, 'mcq2':1, 'mcq3':1})
		result = checkPrerequisites(quiz, user)
		self.failUnlessEqual(result, True)

	def test_copyQuiz(self):
		'''
			Test that copyQuiz actually copies over all the 
			quizzes contents to the published version and doesnt
			leave any fragments in database

			Case no.    Input          Expected Output   Remark
			1           quiz1, quiz3   quiz1 == quiz3    Copy the contents of quiz1 to quiz3  

			@author Evan Kleist
		'''
		quiz1 = Quiz.objects.get(slug=self.quizSlug1)
		quiz3 = Quiz.objects.get(slug="quizunittests_quiz3")

		# Case 1
		copyQuiz(quiz1, quiz3)
		self.failUnlessEqual(quiz1.text, quiz3.text)
		self.failUnlessEqual(quiz1.name, quiz3.name)
		self.failUnlessEqual(quiz1.hidden, quiz3.hidden)
		self.failUnlessEqual(quiz1.prerequisites.all().count(), quiz3.prerequisites.all().count())
		prereqs2 = iter(quiz3.prerequisites.all())
		for prereq in quiz1.prerequisites.all():
			prereq2 = prereqs2.next()
			self.failUnlessEqual(prereq2.containingQuiz, quiz3)
			self.failUnlessEqual(prereq.containingQuiz, quiz1)
			self.failUnlessEqual(prereq.requiredQuiz, prereq2.requiredQuiz)
		self.failUnlessEqual(quiz1.paths.all().count(), quiz3.paths.all().count())
		paths2 = iter(quiz3.paths.all())
		for path in quiz1.paths.all():
			path2 = paths2.next()
			self.failUnlessEqual(path.lowscore, path2.lowscore)
			self.failUnlessEqual(path.highscore, path2.highscore)
			self.failUnlessEqual(path.text, path2.text)
			self.failUnlessEqual(path.passed, path2.passed)
			self.failUnlessEqual(path.toPage, path2.toPage)
		self.failUnlessEqual(quiz1.questions.all().count(), quiz3.questions.all().count())
		questions2 = iter(quiz3.questions.all())
		for question in quiz1.questions.all():
			question2 = questions2.next()
			self.failUnlessEqual(question.text, question2.text)
			self.failUnlessEqual(question.order, question2.order)
			if (isMultipleChoiceQuestion(question)):
				question = question.multiplechoicequestion
				question2 = question2.multiplechoicequestion
				self.failUnlessEqual(question.answers.all().count(), question2.answers.all().count())
				answers2 = iter(question2.answers.all())
				for answer in question.answers.all():
					answer2 = answers2.next()
					self.failUnlessEqual(answer.text, answer2.text)
					self.failUnlessEqual(answer.correct, answer2.correct)
					self.failUnlessEqual(answer.order, answer2.order)
			else:
				question = question.codequestion
				question2 = question2.codequestion
				self.failUnlessEqual(question.beforeCode, question2.beforeCode)
				self.failUnlessEqual(question.showBeforeCode, question2.showBeforeCode)
				self.failUnlessEqual(question.editableCode, question2.editableCode)
				self.failUnlessEqual(question.afterCode, question2.afterCode)
				self.failUnlessEqual(question.showAfterCode, question2.showAfterCode)
				self.failUnlessEqual(question.expectedOutput, question2.expectedOutput)

	def test_matchPath(self):
		'''
			Test that matchPath returns the matching path
			or raises NoMatchingPath if no path is found

			Case no.    Input          Expected Output   Remark
			1           quiz, 49       path              A score that falls within a specified path
			2           quiz, 75       NoMatchingPath    A score that doesnt fall on a path
			3           quiz, 100      path              A score that falls within a specified path, with special case 100 

			@author Evan Kleist
		'''
		quiz = Quiz.objects.get(slug=self.quizSlug1)

		# Case 1
		try:
			path = matchPath(quiz, 49)
		except NoMatchingPath:
			self.failUnlessEqual(0,1, "A matching path should have been found")

		# Case 2
		try:
			path = matchPath(quiz, 75)
			self.failUnlessEqual(0,1, "No mathching path should have been found")
		except NoMatchingPath:
			pass

		# Case 3
		try:
			path = matchPath(quiz, 100)
		except NoMatchingPatch:
			self.failUnlessEqual(0,1, "A matching path should have been found")

	def test_editPath(self):
		'''
			Test that editing a path works as expected

			Case no.    Input                       Expected Output                                     Remark
			1           lowscore = -1               errors = ["Low Score must be between 0 and 100"]    Negative low score
			            highscore = 100

			2           lowscore = 101              errors = ["Low Score must be between 0 and 100",    >100 low score, highscore < lowscore
			            highscore = 100             "Low Score must be less than or equal too High 
			                                         Score"]

			3           lowscore = 100              errors = ["A path that matches this range           Duplicate path
			            highscore = 100              exists already "]

			4           lowscore = "abc"            errors = ["Low Score must be an integer"]           String for lowscore
			            highscore = 100

			5           lowscore = ""               errors = ["Low Score must be an integer"]           Low Score not specified
			            highscore = 100

			6           highscore = -1              errors = ["High Score must be between 0 and 100",   High Score negative, highscore < lowscore
			            lowscore = 70               "Low Score must be less than or equal too 
			                                         High Score"]

			7           highscore = 101             errors = ["High Score must be between 0 and 100"]   High Score > 100
			            lowscore = 70

			8           highscore = "abc"           errors = ["High Score must be an integer"]          High Score is a string
			            lowscore = 70

			9           lowscore = 1                errors = [], path.lowscore = 1                      Successfully edited path
			            highscore = 49              path.highscore = 49
			            dialogue = "test"           path.dialogue = "test"
			            passing = False             path.passed = False
			10          passing = False             errors = []                                         Other quizzes require this quiz as a prerequisite and other passing path exists
			11          passing = False             len(errors) == 2                                    Other quizzes require this quiz as a prerequisite and no other passing path exists

			@author Evan Kleist
		'''
		quiz = Quiz.objects.get(slug = self.quizSlug1)
		numPaths = quiz.paths.all().count()
		path = quiz.paths.get(lowscore=0)
		environ = {
			'HTTP_COOKIE': self.client.cookies,
			'PATH_INFO': '/',
			'QUERY_STRING': '',
			'REQUEST_METHOD': 'GET',
			'SCRIPT_NAME': '',
			'SERVER_NAME': 'testserver',
			'SERVER_PORT': 80,
			'SERVER_PROTOCOL': 'HTTP/1.1',
		}
		environ.update(self.client.defaults)

		customRequest = WSGIRequest(environ)

		# Case 1
		customRequest.POST = {'path':0, 'LowScore':-1, 'HighScore':100, 'pathPage':quiz.slug, 'dialogue':""}
		errors = editPath(quiz, customRequest, self.courseSlug)
		self.failUnlessEqual(errors, ["Low Score must be between 0 and 100"])

		# Case 2
		customRequest.POST = {'path':0, 'LowScore':101, 'HighScore':100, 'pathPage':quiz.slug, 'dialogue':""}
		errors = editPath(quiz, customRequest, self.courseSlug)
		self.failUnlessEqual(errors, ["Low Score must be between 0 and 100", "Low Score must be less than or equal too High Score"])

		# Case 3
		customRequest.POST = {'path':0, 'LowScore':100, 'HighScore':100, 'pathPage':quiz.slug, 'dialogue':""}
		errors = editPath(quiz, customRequest, self.courseSlug)
		self.failUnlessEqual(errors, ["A path that matches this range exists already"])

		# Case 4
		customRequest.POST = {'path':0, 'LowScore':"abc", 'HighScore':100, 'pathPage':quiz.slug, 'dialogue':""}
		errors = editPath(quiz, customRequest, self.courseSlug)
		self.failUnlessEqual(errors, ["Low Score must be an integer"])

		# Case 5
		customRequest.POST = {'path':0, 'LowScore':"", 'HighScore':100, 'pathPage':quiz.slug, 'dialogue':""}
		errors = editPath(quiz, customRequest, self.courseSlug)
		self.failUnlessEqual(errors, ["Low Score must be an integer"])

		# Case 6
		customRequest.POST = {'path':0, 'LowScore':70, 'HighScore':-1, 'pathPage':quiz.slug, 'dialogue':""}
		errors = editPath(quiz, customRequest, self.courseSlug)
		self.failUnlessEqual(errors, ["High Score must be between 0 and 100", "Low Score must be less than or equal too High Score"])

		# Case 7
		customRequest.POST = {'path':0, 'LowScore':70, 'HighScore':101, 'pathPage':quiz.slug, 'dialogue':""}
		errors = editPath(quiz, customRequest, self.courseSlug)
		self.failUnlessEqual(errors, ["High Score must be between 0 and 100"])

		# Case 8
		customRequest.POST = {'path':0, 'LowScore':70, 'HighScore':"abc", 'pathPage':quiz.slug, 'dialogue':""}
		errors = editPath(quiz, customRequest, self.courseSlug)
		self.failUnlessEqual(errors, ["High Score must be an integer"])

		# Case 9
		customRequest.POST = {'path':0, 'LowScore':1, 'HighScore':49, 'pathPage':quiz.slug, 'dialogue':"test"}
		errors = editPath(quiz, customRequest, self.courseSlug)
		self.failUnlessEqual(numPaths, quiz.paths.all().count())
		editedPath = quiz.paths.get(lowscore=1)
		self.failUnlessEqual(editedPath.lowscore, 1)
		self.failUnlessEqual(editedPath.pk, path.pk)
		self.failUnlessEqual(editedPath.highscore, 49)
		self.failUnlessEqual(editedPath.text, "test")
		self.failUnlessEqual(editedPath.toPage.quiz, quiz)
		self.failUnlessEqual(editedPath.passed, False)

		# Case 10
		customRequest.POST = {'path':1, 'LowScore':1, 'HighScore':49, 'pathPage':quiz.slug, 'dialogue':"test", 'passing':'on'}
		editPath(quiz, customRequest, self.courseSlug)
		customRequest.POST = {'path':99, 'LowScore':99, 'HighScore':100, 'pathPage':quiz.slug, 'dialogue':""}
		errors = editPath(quiz, customRequest, self.courseSlug)
		self.failUnlessEqual(errors, [])

		# Case 11
		customRequest.POST = {'path':99, 'LowScore':99, 'HighScore':100, 'pathPage':quiz.slug, 'dialogue':"", 'passing':'on'}
		editPath(quiz, customRequest, self.courseSlug)
		customRequest.POST = {'path':1, 'LowScore':1, 'HighScore':49, 'pathPage':quiz.slug, 'dialogue':"test"}
		editPath(quiz, customRequest, self.courseSlug)
		customRequest.POST = {'path':99, 'LowScore':99, 'HighScore':100, 'pathPage':quiz.slug, 'dialogue':""}
		errors = editPath(quiz, customRequest, self.courseSlug)
		self.failUnlessEqual(len(errors), 2)

	def test_publishQuiz(self):
		'''
			Test that publishQuiz actually copies over all the 
			quizzes contents to the published version and doesnt
			leave any fragments in database

			@author Evan Kleist
		'''
		workingQuiz = Quiz.objects.get(slug=self.quizSlug1 + "_workingCopy")

		# Make a change to the working copy of the quiz
		workingQuiz.name = "modifiedName"
		workingQuiz.text = "modifiedName"
		workingQuiz.slug = slugify("modifiedName")
		workingQuiz.hidden = True
		workingQuiz.save()

		# Publish the changes
		publishQuiz(workingQuiz)

		# Make sure the changes are now in the live quiz
		quiz = Quiz.objects.get(slug=slugify("modifiedName"))
		self.failUnlessEqual(quiz.name, workingQuiz.name)
		self.failUnlessEqual(quiz.name, workingQuiz.name)
		self.failUnlessEqual(quiz.hidden, True)
		self.failUnlessEqual(quiz.upToDate, True)

	def test_removePath(self):
		'''
			Test that removing a path works as expected

			Case no.    Input          Expected Output                   Remark
			1           path0          errors = [], Path.DoesNotExist    Path no longer exists
			2           path100        error

			@author Evan Kleist
		'''
		quiz = Quiz.objects.get(slug = self.quizSlug1)
		environ = {
			'HTTP_COOKIE': self.client.cookies,
			'PATH_INFO': '/',
			'QUERY_STRING': '',
			'REQUEST_METHOD': 'GET',
			'SCRIPT_NAME': '',
			'SERVER_NAME': 'testserver',
			'SERVER_PORT': 80,
			'SERVER_PROTOCOL': 'HTTP/1.1',
		}
		environ.update(self.client.defaults)

		customRequest = WSGIRequest(environ)

		# Case 1
		path = quiz.paths.get(lowscore = 0)
		customRequest.POST = {'path':0}
		errors = removePath(quiz, customRequest)
		self.failUnlessEqual(errors, [])
		try:
			path = quiz.paths.get(lowscore = 0)
			self.failUnlessEqual(0,1, "The path wasnt actually deleted from the database")
		except Path.DoesNotExist:
			pass

	def test_removeQuiz(self):
		'''
			Test that removing a quiz actually removes it and all its associated data

			Case no.    Input          Expected Output            Remark
			1           quiz           Quiz.DoesNotExist          Make sure the quiz does not exist anymore
			2           questions      Question.DoesNotExist      Make sure all of the quizzes questions were also deleted
			3           answers        Answer.DoesNotExist        Make sure all of the answers were also deleted
			4           quiz           Quiz.DoesNotExist          Make sure the working_copy quiz does not exist anymore
			5           questions      Question.DoesNotExist      Make sure all of the working_copy questions were also deleted
			6           answers        Answer.DoesNotExist        Make sure all of the working_copy answers were also deleted
			7           prerequisites  Prerequisite.DoesNotExist  Make sure all of the prerequisites were also deleted
			8           prerequisites  Prerequisite.DoesNotExist  Make sure all of the working_copy prereqs were also deleted
			9           paths          Path.DoesNotExist          Make sure all of the paths were also deleted
			10          paths          Path.DoesNotExist          Make sure all of the working_copy paths were also deleted

			@author Evan Kleist
		'''
		quiz = Quiz.objects.get(slug=self.quizSlug2)
		quiz2 = Quiz.objects.get(slug=(self.quizSlug2 + "_workingCopy"))
		questions = []
		questions2 = []
		answers = []
		answers2 = []
		prereqs = []
		prereqs2 = []
		paths = []
		paths2 = []

		# Get all the questions
		for q in quiz.questions.all():
			if (isMultipleChoiceQuestion(q)):
				questions.append(q.multiplechoicequestion)
			else:
				questions.append(q.codequestion)
		for q in quiz2.questions.all():
			if (isMultipleChoiceQuestion(q)):
				questions2.append(q.multiplechoicequestion)
			else:
				questions2.append(q.codequestion)
		# Get all the answers
		for q in quiz.questions.all():
			if (isMultipleChoiceQuestion(q)):
				q = q.multiplechoicequestion
				answers.append(q.answers.all())
		for q in questions2:
			if (isMultipleChoiceQuestion(q)):
				answers2.append(q.answers.all())
		# Get all the prerequisites
		for p in quiz.prerequisites.all():
			prereqs.append(p)
		for p in quiz2.prerequisites.all():
			prereqs2.append(p)
		# Get all the paths
		for p in quiz.paths.all():
			paths.append(p)
		for p in quiz2.paths.all():
			paths2.append(p)

		# Delete the quiz
		removeQuiz(quiz)

		# Case 1
		try:
			Quiz.objects.get(slug=self.quizSlug2)
			self.failUnlessEqual(0, 1, "The quiz was not deleted")
		except Quiz.DoesNotExist:
			self.failUnlessEqual(1, 1)

		# Case 2
		for q in questions:
			try:
				quiz.questions.get(order=q.order)
				self.failUnlessEqual(0, 1, "A question still exists in the database")
			except Question.DoesNotExist:
				self.failUnlessEqual(1, 1)

		# Case 3
		answers = iter(answers)
		for q in questions:
			if (isMultipleChoiceQuestion(q)):
				q = q.multiplechoicequestion
				anss = answers.next()
				for a in anss:
					try:
						q.answers.get(order=a.order)
						self.failUnlessEqual(0, 1, "An answer still exists in the database")
					except Answer.DoesNotExist:
						self.failUnlessEqual(1, 1)

		# Case 4
		try:
			Quiz.objects.get(slug=(self.quizSlug2 + "_workingCopy"))
			self.failUnlessEqual(0, 1, "The working_copy was not deleted")
		except Quiz.DoesNotExist:
			self.failUnlessEqual(1, 1)

		# Case 5
		for q in questions2:
			try:
				quiz2.questions.get(order=q.order)
				self.failUnlessEqual(0, 1, "A question still exists in the database")
			except Question.DoesNotExist:
				self.failUnlessEqual(1, 1)

		# Case 6
		answers2 = iter(answers2)
		for q in questions2:
			if (isMultipleChoiceQuestion(q)):
				q = q.multiplechoicequestion
				anss = answers2.next()
				for a in anss:
					try:
						q.answers.get(order=a.order)
						self.failUnlessEqual(0, 1, "An answer still exists in the database")
					except Answer.DoesNotExist:
						self.failUnlessEqual(1, 1)

		# Case 7
		for p in prereqs:
			try:
				quiz.prerequisites.get(containingQuiz = p.containingQuiz, requiredQuiz = p.requiredQuiz)
				self.failUnlessEqual(0, 1, "A prerequisite still exists in the database")
			except Answer.DoesNotExist:
				self.failUnlessEqual(1, 1)

		# Case 8
		for p in prereqs2:
			try:
				quiz2.prerequisites.get(containingQuiz = p.containingQuiz, requiredQuiz = p.requiredQuiz)
				self.failUnlessEqual(0, 1, "A prerequisite still exists in the database")
			except Answer.DoesNotExist:
				self.failUnlessEqual(1, 1)

		# Case 9
		for p in paths:
			try:
				quiz.paths.get(lowscore = p.lowscore)
				self.failUnlessEqual(0, 1, "A path still exists in the database")
			except Answer.DoesNotExist:
				self.failUnlessEqual(1, 1)

		# Case 10
		for p in paths2:
			try:
				quiz2.paths.get(lowscore = p.lowscore)
				self.failUnlessEqual(0, 1, "A path still exists in the database")
			except Answer.DoesNotExist:
				self.failUnlessEqual(1, 1)


	def test_reorderQuestions(self):
		'''
			Test that reoderQuestions actually does reorder the questions into a valid state

			Case no.    Input          Expected Output          Remark
			1           quiz           false                    Make sure the questions are not in order
			2           quiz           true                     Check to make sure that the questions are in a valid state

			@author Evan Kleist
		'''
		quiz = Quiz.objects.get(slug=self.quizSlug1)
		questions = quiz.questions.all()

		# Make the questions order something arbitrary
		for q in questions:
			q.order = 0
			q.save()

		# Case 1
		self.failUnlessEqual(validateQuestionOrder(quiz), False)

		# Now reorder the questions
		reorderQuestions(quiz)

		# Case 2
		self.failUnlessEqual(validateQuestionOrder(quiz), True)

	def test_revertQuiz(self):
		'''
			Test that revertQuiz actually reverts all the 
			working copies contents to the published version and doesnt
			leave any fragments in database  
			
			@author Evan Kleist     
		'''
		workingQuiz = Quiz.objects.get(slug=self.quizSlug1 + "_workingCopy")

		# Make a change to the working copy of the quiz
		workingQuiz.name = "modifiedName22"
		workingQuiz.hidden = True
		workingQuiz.save()

		# Revert the changes
		revertQuiz(workingQuiz)

		# Make sure the changes were undone
		quiz = Quiz.objects.get(slug = self.quizSlug1)
		workingQuiz = Quiz.objects.get(slug=self.quizSlug1 + "_workingCopy")
		self.failUnlessEqual(quiz.name, workingQuiz.name)
		self.failUnlessEqual(quiz.hidden, workingQuiz.hidden)
		self.failUnlessEqual(quiz.upToDate, True)


	def test_safeSlug(self):
		'''
			Test that safeSlug actually returns a safe slug when expected to

			Case no.    Input                               Expected Output          Remark
			1           quizSlug1                           quizSlug1                A "safe" slug
			2           quizSlug1_workingCopy               quizSlug1                An "unsafe" slug
			3           quizSlug1_workingCopy_workingCopy   quizSlug1_workingCopy    Special case if a quiz happened to have a name ending in  _workingCopy
			4           _workingCopy                        _workingCopy             Special case name _workingCopy

			@author Evan Kleist
		'''
		# Case 1
		slug = safeSlug(self.quizSlug1)
		self.failUnlessEqual(slug, self.quizSlug1)

		# Case 2
		slug = safeSlug(self.quizSlug1 + "_workingCopy")
		self.failUnlessEqual(slug, self.quizSlug1)

		# Case 3
		slug = safeSlug(self.quizSlug1 + "_workingCopy_workingCopy")
		self.failUnlessEqual(slug, self.quizSlug1 + "_workingCopy")

		# Case 4
		slug = safeSlug("_workingCopy")
		self.failUnlessEqual(slug, "_workingCopy")

	def test_saveQuiz(self):
		'''
			Test that saveQuiz actually saves a quiz and updates all of its components

			Case no.  Input                              Expected Output                          Remark
			1         quizTitle = "QuizUnitTests_Quiz2"  errors = ["Quiz Title already exists!"]  A quiz with a duplicate name
			2         quizTitle = ""                     errors ["Quiz Title cannot be blank!"]   Blank quiz title
			3         quizTitle = "New Title"            quiz.name = "New Title"                  Change the title, make quiz hidden, swap question 2 and 3
			                                             quiz.slug = "new-title"
			                                             quiz.text = "New Title"
			          hidden = True                      quiz.hidden = True   
                   mcq3text = "Question 2"            quiz.question3.text = "Question 2"
                   mcq3order = 2                      quiz.question3.order = 2
			          mcq2text = "Question 3"            quiz.question2.text = "Question 3"
			          mcq2order = 3                      quiz.question2.order = 3
		'''
		environ = {
			'HTTP_COOKIE': self.client.cookies,
			'PATH_INFO': '/',
			'QUERY_STRING': '',
			'REQUEST_METHOD': 'GET',
			'SCRIPT_NAME': '',
			'SERVER_NAME': 'testserver',
			'SERVER_PORT': 80,
			'SERVER_PROTOCOL': 'HTTP/1.1',
		}
		environ.update(self.client.defaults)
		quizSlug = self.quizSlug1
		customRequest = WSGIRequest(environ)

		# Case 1
		customRequest.POST = {'quizTitle':"QuizUnitTests_Quiz2"}
		r = saveQuiz(customRequest, self.courseSlug, quizSlug)
		errors = r["errors"]
		quizSlug = r["quiz_slug"]
		self.failUnlessEqual(errors, ["Quiz Title already exists!"])

		# Case 2
		customRequest.POST = {'quizTitle':""}
		r = saveQuiz(customRequest, self.courseSlug, quizSlug)
		errors = r["errors"]
		quizSlug = r["quiz_slug"]
		self.failUnlessEqual(errors, ["Quiz Title cannot be blank!"])

		# Case 3
		customRequest.POST = {'quizTitle':"New Title",
									 'hidden':"on",
									 'mcq1text':"Test question 1",
									 'mcq1order':1,
									 'mcq1a1':"a1",
									 'mcq1a1order':1,
									 'mcq1ac':1,
									 'mcq1a2':"b1",
									 'mcq1a2order':2,
									 'mcq2text':"Test question 3",
									 'mcq2order':3,
									 'mcq2a1':"a1",
									 'mcq2a1order':1,
									 'mcq2ac':1,
									 'mcq2a2':"b1",
									 'mcq2a2order':2,
									 'mcq3text':"Test question 2",
									 'mcq3order':2,
									 'mcq3a1':"a1",
									 'mcq3a1order':1,
									 'mcq3ac':1,
									 'mcq3a2':"b1",
									 'mcq3a2order':2,
									}
		r = saveQuiz(customRequest, self.courseSlug, quizSlug)
		errors = r["errors"]
		quizSlug = r["quiz_slug"]
		quiz = Quiz.objects.get(slug=quizSlug + "_workingCopy")
		self.failUnlessEqual(quiz.name, "New Title")
		self.failUnlessEqual(quiz.text, "New Title")
		self.failUnlessEqual(quiz.slug, "new-title_workingCopy")
		self.failUnlessEqual(quiz.hidden, True)
		self.failUnlessEqual(errors, [])

	def test_scoreQuiz(self):
		'''
			Test that scoreQuiz correctly returns a score for the submitted quiz

			Case no.    Input          Expected Output          Remark
			1           quiz2          100                      submitting a blank quiz is 0/0
			2           quiz1          0                        submitting a quiz without answering anything is 0/3
			3           quiz1          100                      submitting a quiz with all correct answers is 3/3

			@author Evan Kleist           
		'''
		environ = {
			'HTTP_COOKIE': self.client.cookies,
			'PATH_INFO': '/',
			'QUERY_STRING': '',
			'REQUEST_METHOD': 'GET',
			'SCRIPT_NAME': '',
			'SERVER_NAME': 'testserver',
			'SERVER_PORT': 80,
			'SERVER_PROTOCOL': 'HTTP/1.1',
		}
		environ.update(self.client.defaults)
		quizSlug = self.quizSlug1
		customRequest = WSGIRequest(environ)

		# Case 1
		customRequest.POST = {}
		customRequest.user = False
		quiz = Quiz.objects.get(slug=self.quizSlug2)
		score = scoreQuiz(quiz, customRequest, self.courseSlug, quiz.slug)
		self.failUnlessEqual(score, 0)

		# Case 2
		customRequest.POST = {}
		customRequest.user = False
		quiz = Quiz.objects.get(slug=quizSlug)
		score = scoreQuiz(quiz, customRequest, self.courseSlug, quiz.slug)
		self.failUnlessEqual(score, 0)

		# Case 3
		customRequest.POST = {'mcq1':1, 'mcq2':1, 'mcq3':1}
		customRequest.user = False
		quiz = Quiz.objects.get(slug=quizSlug)
		score = scoreQuiz(quiz, customRequest, self.courseSlug, quiz.slug)
		self.failUnlessEqual(score, 3)

	def test_validateQuestionOrder(self):
		'''
			Test that reoderQuestions actually does reorder the questions into a valid state

			Case no.    Input          Expected Output          Remark
			1           quiz           true                     Quiz with all questions in valid order
			2           quiz           false                    Quiz with first question 0, not 1
			3           quiz           false                    Quiz with duplicate ordering
			4           quiz           false                    Quiz with last question not last order

			@author Evan Kleist
		'''
		quiz = Quiz.objects.get(slug=self.quizSlug1)
		questions = quiz.questions.all()

		# Case 1
		self.failUnlessEqual(validateQuestionOrder(quiz), True)

		# Case2
		q = quiz.questions.get(order=1)
		q.order = 0
		q.save()
		self.failUnlessEqual(validateQuestionOrder(quiz), False)
		q = quiz.questions.get(order=0)
		q.order = 1
		q.save()

		# Case 3
		q = quiz.questions.get(order=2)
		q.order = 1
		q.save()
		self.failUnlessEqual(validateQuestionOrder(quiz), False)
		q = quiz.questions.get(text="<p>Test question 2</p>")
		q.order = 2
		q.save()

		# Case 4
		q = quiz.questions.get(order=3)
		q.order = 99
		q.save()
		self.failUnlessEqual(validateQuestionOrder(quiz), False)
		q = quiz.questions.get(order=99)
		q.order = 3
		q.save()

	def test_validateQuiz(self):
		'''
			Test that validateQuizcorrectly handles bad data

			Case no.  Input                         Expected Output                            Remark
			1         quiz.text = ""                errors = ["Quiz Title can not be blank"]   Blank quiz title
			2         quiz.prereq = self.quiz2      errors = ["QuizUnitTests_Quiz2 does not    Invalid prerequisite
			                                                   have a passing path"]
			3         quiz.question2.text = ""      errors = ["Question cannot have a blank    Blank mcq prompt
			                                                   prompt"]
			4         quiz.question2.a1.text = ""   errors = ["Answer must not be blank"]      Blank answer
			5         quiz.question1.text = ""      errors = ["Code Question prompt must       Blank cq prompt
			                                                   not be blank"
			6         quiz.question1.eo = ""        errors = ["Code Question expected output   Blank cq expected output
			                                                   must not be blank"
			7         quiz.question1.order = "0"    errors = ["Questions must have a valid     Invalid question ordering
			                                                   ordering"]

			@author Evan Kleist      
		'''
		quizSlug = "validatequiz_quiz_workingCopy"

		# Case 1
		quiz = Quiz.objects.get(slug=quizSlug)
		quiz.text = ""
		quiz.save()
		errors = validateQuiz(quiz)
		self.failUnlessEqual(errors, ["Quiz Title can not be blank"])
		revertQuiz(quiz)

		# Case 2
		newPrereq = Prerequisite(containingQuiz = Quiz.objects.get(slug=quizSlug), requiredQuiz = Quiz.objects.get(slug=self.quizSlug2))
		newPrereq.save()
		quiz = Quiz.objects.get(slug=quizSlug)
		errors = validateQuiz(quiz)
		self.failUnlessEqual(errors, ["QuizUnitTests_Quiz2 does not have a passing path"])
		revertQuiz(quiz)

		# Case 3
		question = quiz.questions.get(order="2")
		question.text = ""
		question.save()
		quiz = Quiz.objects.get(slug=quizSlug)
		errors = validateQuiz(quiz)
		self.failUnlessEqual(errors, ["Question cannot have a blank prompt"])
		revertQuiz(quiz)


		# Case 4
		question = quiz.questions.get(order="2").multiplechoicequestion
		answer = question.answers.get(order="1")
		answer.text = ""
		answer.save()
		quiz = Quiz.objects.get(slug=quizSlug)
		errors = validateQuiz(quiz)
		self.failUnlessEqual(errors, ["Answer must not be blank"])
		revertQuiz(quiz)

		# Case 5
		question = quiz.questions.get(order="1").codequestion
		question.text = ""
		question.save()
		quiz = Quiz.objects.get(slug=quizSlug)
		errors = validateQuiz(quiz)
		self.failUnlessEqual(errors, ["Code Question prompt must not be blank"])
		revertQuiz(quiz)

		# Case 6
		question = quiz.questions.get(order="1").codequestion
		question.expectedOutput = ""
		question.save()
		quiz = Quiz.objects.get(slug=quizSlug)
		errors = validateQuiz(quiz)
		self.failUnlessEqual(errors, ["Code Question expected output must not be blank"])
		revertQuiz(quiz)

		# Case 7
		question = quiz.questions.get(order="2")
		question.order = 0
		question.save()
		quiz = Quiz.objects.get(slug=quizSlug)
		errors = validateQuiz(quiz)
		self.failUnlessEqual(errors, ["Questions must have a valid ordering"])
		revertQuiz(quiz)
class QuizViewTests(TestCase):
	''' 
		Unit Tests on Quiz Views.  Tests use an emulated Web Client
		to simulate a user making requests via the web interface

		Test fixtures include...

		@author Evan Kleist
	'''
	fixtures = ['QuizViewTests']

	def setUp(self):
		'''
			Set up the tests
		'''
		self.client = Client()
		self.courseSlug = 'QuizViewTests_Course1'
		self.quizSlug1 = 'QuizViewTests_Quiz1'
		self.quizSlug2 = 'QuizViewTests_Quiz2'

	def testPublicQuizUrl(self):
		'''
			Test that the urls to a known public quiz page works properly

			Case no.    Input                                                        Expected Output         Remark
			1           url = /course/courseSlug/page/quizSlug1/                     200                     302 is a found code
			2           url = /course/badCourse/page/quizSlug1/                      404                     404 is a bad link error
			3           url = /course/courseSlug/page/badQuiz/                       404                     404 is a bad link error
			4           url = /course/badCourse/page/badQuiz/                        404                     404 is a bad link error

			@author Evan Kleist
		'''

		# Case 1 - A good course and a good quiz should display properly		
		response = self.client.get('/course/' + self.courseSlug + '/page/' + self.quizSlug1 + '/')
		self.failUnlessEqual(response.status_code, 200)

		# Case 2 - A bad course and a good quiz should display an error
		response = self.client.get('/course/' + 'badClass' + '/page/' + self.quizSlug1 + '/')
		self.failUnlessEqual(response.status_code, 404) 

		# Case 3 - A good course and a bad quiz should display an error
		response = self.client.get('/course/' + self.courseSlug + '/page/' + 'badQuiz' + '/')
		self.failUnlessEqual(response.status_code, 404) 

		# Case 4 - A bad course and a bad quiz should display an error
		response = self.client.get('/course/' + 'badClass' + '/page/' + 'badQuiz' + '/')
		self.failUnlessEqual(response.status_code, 404)

	def testPrivateQuizUrl(self):
		'''
			Test that the urls to a known private quiz page works properly when logged in and errors otherwise

			Case no.    Input                                                        Expected Output         Remark
			1           url = /course/courseSlug/page/quizSlug1/                     200                     User not logged in, course private
			            user not logged in                                           denied.html
			2           url = /course/courseSlug/page/quizSlug1/                     200                     User logged in, not enrolled, course private
			            user logged in, not enrolled                                 denied.html
			3           url = /course/courseSlug/page/quizSlug1/                     200                     User logged in, enrolled, course private
			            user logged in, enrolled                                     viewQuiz.html
	
			@author Evan Kleist
		'''
		courseSlug = "QuizViewTests_Course2"
		quizSlug = "QuizViewTests_Quiz3"
		enrolledUser = "testUser2"
		unenrolledUser = "testUser1"
		enrolledUserPwd = "password"
		unenrolledUserPwd = "password"

		# Case 1		
		response = self.client.get('/course/' + courseSlug + '/page/' + quizSlug + '/')
		self.assertTemplateUsed(response, "page/denied.html")

		# Case 2
		self.failUnlessEqual(self.client.login(username=unenrolledUser, password=unenrolledUserPwd), True)
		response = self.client.get('/course/' + courseSlug + '/page/' + quizSlug + '/')
		self.assertTemplateUsed(response, "page/denied.html")

		# Case 3
		self.client.logout()
		self.failUnlessEqual(self.client.login(username=enrolledUser, password=enrolledUserPwd), True)
		response = self.client.get('/course/' + courseSlug + '/page/' + quizSlug + '/')
		self.assertTemplateUsed(response, "page/quiz/viewQuiz.html")
		
		pass

	def testHiddenQuizUrl(self):
		'''
			Test that the urls to a known private quiz page works properly when logged in and errors otherwise

			Case no.    Input                                                        Expected Output         Remark
			1           url = /course/courseSlug/page/quizSlug1/                     200                     User not logged in, no prereqs
			            user not logged in                                           denied.html
			2           url = /course/courseSlug/page/quizSlug1/                     200                     User logged in, not enrolled, no prereqs
			            user logged in, not enrolled                                denied.html
			3           url = /course/courseSlug/page/quizSlug1/                     200                     User logged in, enrolled, no prereqs
			            user logged in, enrolled                                     denied.html
			4           url = /course/courseSlug/page/quizSlug1/                     200                     User logged in, enrolled, prereqs
			            user logged in, enrolled                                     viewQuiz.html

			@author Evan Kleist
		'''

		pass

	def testSubmitPublicQuizUrl(self):
		'''
			Test that the urls to submit a public quiz page works properly

			Case no.    Input                                                        Expected Output         Remark
			1           url = /course/courseSlug/page/quizSlug1/submitQuiz/                200                     302 is a found code
			2           url = /course/badCourse/page/quizSlug1/submitQuiz/                 404                     404 is a bad link error
			3           url = /course/courseSlug/page/badQuiz/submitQuiz/                  404                     404 is a bad link error
			4           url = /course/badCourse/page/badQuiz/submitQuiz/                   404                     404 is a bad link error
		
			@author Evan Kleist
		'''

		# Case 1 - A good course and a good quiz should display properly		
		response = self.client.get('/course/' + self.courseSlug + '/page/' + self.quizSlug1 + '/submitQuiz/')
		self.failUnlessEqual(response.status_code, 200)

		# Case 2 - A bad course and a good quiz should display an error
		response = self.client.get('/course/' + 'badClass' + '/page/' + self.quizSlug1 + '/submitQuiz/')
		self.failUnlessEqual(response.status_code, 404) 

		# Case 3 - A good course and a bad quiz should display an error
		response = self.client.get('/course/' + self.courseSlug + '/page/' + 'badQuiz' + '/submitQuiz/')
		self.failUnlessEqual(response.status_code, 404) 

		# Case 4 - A bad course and a bad quiz should display an error
		response = self.client.get('/course/' + 'badClass' + '/page/' + 'badQuiz' + '/submitQuiz/')
		self.failUnlessEqual(response.status_code, 404) 

	def testSubmitPrivateQuizUrl(self):
		'''
			Test that the urls to submit a private quiz page works properly

			Case no.    Input                                                        Expected Output         Remark
			1           url = /course/courseSlug/page/quizSlug1/submitQuiz/          200                     User not logged in, course private
			            user not logged in                                           denied.html
			2           url = /course/courseSlug/page/quizSlug1/submitQuiz/          200                     User logged in, not enrolled, course private
			            user logged in, not enrolled                                 denied.html
			3           url = /course/courseSlug/page/quizSlug1/submitQuiz/          submitQuiz.html         User logged in, enrolled, course private, no POST
			                                                                         score = 0
			4           url = /course/courseSlug/page/quizSlug1/submitQuiz/                                  User logged in, enrolled, course private, with POST
			            user logged in, enrolled                                     submitQuiz.html
	
		@author Evan Kleist
		'''
		courseSlug = "QuizViewTests_Course2"
		quizSlug = "QuizViewTests_Quiz3"
		enrolledUser = "testUser2"
		unenrolledUser = "testUser1"
		enrolledUserPwd = "password"
		unenrolledUserPwd = "password"

		# Case 1		
		response = self.client.get('/course/' + courseSlug + '/page/' + quizSlug + '/submitQuiz/')
		self.assertTemplateUsed(response, "page/denied.html")

		# Case 2
		self.failUnlessEqual(self.client.login(username=unenrolledUser, password=unenrolledUserPwd), True)
		response = self.client.get('/course/' + courseSlug + '/page/' + quizSlug + '/submitQuiz/')
		self.assertTemplateUsed(response, "page/denied.html")

		# Case 3
		self.client.logout()
		self.failUnlessEqual(self.client.login(username=enrolledUser, password=enrolledUserPwd), True)
		response = self.client.get('/course/' + courseSlug + '/page/' + quizSlug + '/submitQuiz/')
		self.assertTemplateUsed(response, "page/quiz/submitQuiz.html")


	def testSubmitHiddenQuizUrl(self):
		'''
			Test that the urls to submit a hidden quiz page works properly

			Case no.    Input                                                        Expected Output         Remark
			1           url = /course/courseSlug/page/quizSlug1/submitQuiz/                200                     302 is a found code
			2           url = /course/badCourse/page/quizSlug1/submitQuiz/                 404                     404 is a bad link error
			3           url = /course/courseSlug/page/badQuiz/submitQuiz/                  404                     404 is a bad link error
			4           url = /course/badCourse/page/badQuiz/submitQuiz/                   404                     404 is a bad link error
		
			@author Evan Kleist
		'''

		pass

	def testSubmitQuizUrl_BadData(self):
		'''
			Test the urls to make sure that submitting a quiz with 
			bad data is properly handeled

			@author Evan Kleist
		'''
		pass

	def testEditPublicQuizUrl(self):
		'''
			Test that the urls to edit a known public quiz page works properly

			Case no.    Input                                                        Expected Output         Remark
			1           url = /course/courseSlug/page/quizSlug1/edit/                200                     302 is a found code
			2           url = /course/badCourse/page/quizSlug1/edit/                 404                     404 is a bad link error
			3           url = /course/courseSlug/page/badQuiz/edit/                  404                     404 is a bad link error
			4           url = /course/badCourse/page/badQuiz/edit/                   404                     404 is a bad link error
		
			@author Evan Kleist
		'''

		# Case 1 - A good course and a good quiz should display properly		
		response = self.client.get('/course/' + self.courseSlug + '/page/' + self.quizSlug1 + '/edit/')
		self.failUnlessEqual(response.status_code, 302)

		# Case 2 - A bad course and a good quiz should display an error
		response = self.client.get('/course/' + 'badClass' + '/page/' + self.quizSlug1 + '/edit/')
		self.failUnlessEqual(response.status_code, 302) 

		# Case 3 - A good course and a bad quiz should display an error
		response = self.client.get('/course/' + self.courseSlug + '/page/' + 'badQuiz' + '/edit/')
		self.failUnlessEqual(response.status_code, 302) 

		# Case 4 - A bad course and a bad quiz should display an error
		response = self.client.get('/course/' + 'badClass' + '/page/' + 'badQuiz' + '/edit/')
		self.failUnlessEqual(response.status_code, 302)

	def testEditPrivateQuizUrl(self):
		'''
			Test that the urls to edit a known private quiz page works properly

			Case no.    Input                                                        Expected Output         Remark
			1           url = /course/courseSlug/page/quizSlug1/edit/                200                     302 is a found code
			2           url = /course/badCourse/page/quizSlug1/edit/                 404                     404 is a bad link error
			3           url = /course/courseSlug/page/badQuiz/edit/                  404                     404 is a bad link error
			4           url = /course/badCourse/page/badQuiz/edit/                   404                     404 is a bad link error
		
			@author Evan Kleist
		'''

		pass

	def testEditHiddenQuizUrl(self):
		'''
			Test that the urls to edit a known hidden quiz page works properly

			Case no.    Input                                                        Expected Output         Remark
			1           url = /course/courseSlug/page/quizSlug1/edit/                200                     302 is a found code
			2           url = /course/badCourse/page/quizSlug1/edit/                 404                     404 is a bad link error
			3           url = /course/courseSlug/page/badQuiz/edit/                  404                     404 is a bad link error
			4           url = /course/badCourse/page/badQuiz/edit/                   404                     404 is a bad link error
		
			@author Evan Kleist
		'''

		pass

	def testDeleteQuizView(self):
		'''
			Test that will make sure the quiz deletion confirmation
			 dialogue is working properly

		
			@author Evan Kleist
		'''
		pass

	def testDeleteQuestionView(self):
		'''
			Test that will make sure the question deletion
			confirmation dialogue is working properly

			@author Evan Kleist
		'''
		pass

	def testAddPathView(self):
		'''
			Test that will make sure add path view is working properly

			@author Evan Kleist
		'''
		pass
	def testEditPathView(self):
		'''
			Test that will make sure the edit path view is working properly

			@author Evan Kleist
		'''
		pass

