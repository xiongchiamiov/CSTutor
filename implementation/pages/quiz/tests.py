'''
This file contains tests for the Quiz package.

All tests are ran by the django test runner

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
from django.http import QueryDict

class QuizUnitTests(TestCase):
	'''
		Unit Tests on backend quiz operations. This class contains
		tests for 100% code coverage of quiz.py

		Test Fixtures are described as follows
		
		USERS
		--------------------------------
		ekleist - Used as the user capable of editing course content.
		          Not actually used in the tests, but used in the creation
		          of the test fixtures
		testuser - User used in checkPrerequisites and scoreQuiz. This user
		           is enrolled in the course and is the subject of prerequisite
		           testing and quiz scoring
		--------------------------------

		COURSES
		--------------------------------
		QuizUnitTests_Course - The container course for all of the used quizzes
		--------------------------------

		QUIZZES
		--------------------------------
		QuizUnitTests_Quiz1 - A quiz containing 3 multiple choice questions, 
			                   a passing and non-passing path, and a prerequisite.
		                      It is the primary quiz used in most tests
		QuizUnitTests_Quiz2 - A blank quiz
		QuizUnitTests_Quiz3 - A second blank quiz
		validateQuiz_Quiz - A quiz with 1 code question and 1 multiple choice
		                    question. It is the basic quiz used in validating
		                    a quiz for improper data
		checkPrerequisites_Quiz - A quiz with a prerequisite used in testing
		                          prerequisites
		copyQuiz_Quiz - A quiz containing one of every element used in testing
		                copyQuiz to make sure every element is successfully copied
		scoreQuiz_Quiz - A quiz with a sample MCQ and CQ used to test for
		                 proper grading of questions
		--------------------------------

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
			Test that adding a code question to a quiz works as expected.
			Ensures that only one new question was added, the question was
			added as the last question, and that the "new" question is blank

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
			Test that adding a multiple choice question to a quiz works as expected. 
			Ensures that only one new question was added, the question was
			added as the last question, and that the "new" question is blank

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
			or returns the appropriate errors.

			Ensures that addPath validates data to the following criteria:
			   isInt(LowScore) && isInt (HighScore)
			   0 < Low Score <= High Score <= 100
			   New Path does not conflict with an existing pah
			

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
			Test that prerequisites are properly checked and the correct
			boolean is returned. Tests with AnonymousUsers and well as
			logged in users with varying degrees of prerequisites
			satisfied. Tests that checkPrerequisites only returns true if
			either the quiz has no prerequisites or ALL prerequisites
			have been met

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
		Stat.CreateStat(quiz.course, Quiz.objects.get(slug="quizunittests_quiz1"), user, 0)
		result = checkPrerequisites(quiz, user)
		self.failUnlessEqual(result, False)

		# Case 5
		user = User.objects.get(username="testuser")
		quiz = Quiz.objects.get(slug="checkprerequisites_quiz")
		Stat.CreateStat(quiz.course, Quiz.objects.get(slug="quizunittests_quiz1"), user, 3)
		quiz = Quiz.objects.get(slug="checkprerequisites_quiz")
		result = checkPrerequisites(quiz, user)
		self.failUnlessEqual(result, True)

	def test_copyQuiz(self):
		'''
			Test that copyQuiz copies over EVERY element of the quiz.
			This includes related objects questions, answers, paths,
			and prerequisites. Essentially quiz1 shoudl equal quiz2
			in every aspect except for its slug and primary key.

			Case no.    Input          Expected Output   Remark
			1           quiz1, quiz3   quiz1 == quiz3    Copy the contents of quiz1 to quiz3 and make sure its a replica

			@author Evan Kleist
		'''
		quiz1 = Quiz.objects.get(slug="copyquiz_quiz")
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
			Test that editing a successfully edits a path or returns
			a list of errors. Errors originate from the POST data being submitted
			being validated against the following criteria:

			   0 <= Low Score <= High Score <= 100
				Low Score and High Score must both be integers
				Path cannot overlap into an existing path (except itself)
				If changing a path to go from passing to not passing, ensure that
				   either an alternate passing path exists OR no other quizzes
			      require this quiz as a prerequisite. If both of these conditions
			      are not met, it could lead to an unreachable quiz.

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
			Test that publishQuiz copies content over from the workingCopy of a
			quiz to its corresponding published copy. Also test to make sure the
			published copy is set to be "Up TO Date"

			Note: publishQuiz calls copyQuiz() which is tested prior to this test.
			This means that assuming copyQuiz works properly, I do not need to
			check every single field of the quiz. I arbitrarily selected some
			random fields and changed them and made sure they changes were
			reflected in the published copy. If they were, and copyQuiz works
			properly, then I know that ANY changes made would be copied over.

			Case no.    Input                               Expected Output        Remark
			1           workingQuiz.name = "modifiedName"   quiz == workingQuiz    Make sure modified fields are copied over
			            workingQuiz.text = "modifiedName"   quiz.upToDate == True
			            workingQuiz.slug = "modifiedname"
			            workingQuiz.hidden = True

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
		self.failUnlessEqual(quiz.text, workingQuiz.text)
		self.failUnlessEqual(quiz.hidden, True)
		self.failUnlessEqual(quiz.upToDate, True)

	def test_removePath(self):
		'''
			Test that removing a successfully removes a path or returns
			a list containing any errors that occured

			Case no.    Input          Expected Output                   Remark
			1           path99         len(errors) == 2                  Cant remove the only passing path if other quizzes require it as a prerequisite
			1           path0          errors = [], Path.DoesNotExist    Path no longer exists

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
		customRequest.POST = {'path':99}
		errors = removePath(quiz, customRequest)
		self.failUnlessEqual(len(errors), 2)
		
		# Case 2
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
			Test that removing a quiz actually removes it and all its associated
			data. No item should be left in the database after a remove for both
			the quiz and its working copy

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
		quiz = Quiz.objects.get(slug="copyquiz_quiz")
		quiz2 = Quiz.objects.get(slug="copyquiz_quiz_workingCopy")
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
			Quiz.objects.get(slug="copyquiz_quiz")
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
			Quiz.objects.get(slug=("copyquiz_quiz_workingCopy"))
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
				quiz.prerequisites.get(requiredQuiz = p.requiredQuiz)
				self.failUnlessEqual(0, 1, "A prerequisite still exists in the database")
			except Prerequisite.DoesNotExist:
				self.failUnlessEqual(1, 1)

		# Case 8
		for p in prereqs2:
			try:
				quiz2.prerequisites.get(requiredQuiz = p.requiredQuiz)
				self.failUnlessEqual(0, 1, "A prerequisite still exists in the database")
			except Prerequisite.DoesNotExist:
				self.failUnlessEqual(1, 1)

		# Case 9
		for p in paths:
			try:
				quiz.paths.get(lowscore = p.lowscore)
				self.failUnlessEqual(0, 1, "A path still exists in the database")
			except Path.DoesNotExist:
				self.failUnlessEqual(1, 1)

		# Case 10
		for p in paths2:
			try:
				quiz2.paths.get(lowscore = p.lowscore)
				self.failUnlessEqual(0, 1, "A path still exists in the database")
			except Path.DoesNotExist:
				self.failUnlessEqual(1, 1)


	def test_reorderQuestions(self):
		'''
			Arbitraily make question ordering invalid and test that
		   reoderQuestions actually does reorder the questions
			into a valid state as specified by validateQuestionOrder().

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
			Arbitrarily change some of a quizes workingCopy content
			and test that revert quiz successfully reverts it to its
			published state.

			Note: Since this method calls another tested method copyQuiz()
			I do not need to test for every field of the quiz. That
			is done in another test.

			Case no.    Input                                 Expected Output                       Remark
			1           workingQuiz.name = "modifiedName22"   workingQuiz.name == quiz.name         Test that some arbitrary fields
			            workingQuiz.hidden = True             workingQuiz.hidden == quiz.hidden     are successfully reverted
			
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
			Test that safeSlug will strip the trailing "_workingCopy" from a slug,
			if one exists. If it doesnt, it should return and unmodified slug.
			Also covers the special case where a quiz name happens to end in
			"_workingCopy" by chance and that this doesn't also get stripped
			from the slug

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
			Test that saveQuiz actually saves a quiz and updates all
			of its components or returns any appropriate errors
			indicating a failure.

			Case no.  Input                              Expected Output                          Remark
			1         quizTitle = "QuizUnitTests_Quiz2"  errors = ["Quiz Title already exists!"]  A quiz with a duplicate name
			2         quizTitle = ""                     errors ["Quiz Title cannot be blank!"]   Blank quiz title
			3         quizTitle = "New Title"            quiz.name = "New Title"                  Change the title, make quiz hidden, swap question 1 and 2
			                                             quiz.slug = "new-title"
			                                             quiz.text = "New Title"
			          hidden = True                      quiz.hidden = True   
                   cq1 = "cq"                         quiz.question1.text = "cq"
                   cq1order = 2                       quiz.question1.order = 2
			          mcq2text = "mcq"                   quiz.question2.text = "mcq"
			          mcq2order = 1                      quiz.question2.order = 1
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
		quizSlug = "copyquiz_quiz"
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
		dictionary = {'quizTitle':"New Title",
									 'hidden':"on",
									 'prereqs':"checkprerequisites_quiz",
									 'cq1text':"cq",
									 'cq1eo':"cqeo",
									 'cq1order':2,
									 'mcq2text':"mcq",
									 'mcq2order':1,
									 'mcq2a1':"a1",
									 'mcq2a1order':1,
									 'mcq2ac':1,
									 'mcq2a2':"b1",
									 'mcq2a2order':2,
									}
		qd = QueryDict({})
		qd = qd.copy()
		qd.update(dictionary)
		customRequest.POST = qd
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

			Case no.    Input            Expected Output          Remark
			1           quiz2            0                        submitting a blank quiz is 0/0
			2           scorequiz_quiz   0                        submitting a quiz without answering anything is 0/2
			3           scorequiz_quiz   1                        submitting a quiz with incorrect mcq is 1/2
			4           scorequiz_quiz   1                        submitting a quiz with incorrect cq is 1/2
			5           scorequiz_quiz   2                        submitting a quiz with correct cq is 2/2

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
		quizSlug = "scorequiz_quiz"
		customRequest = WSGIRequest(environ)

		# Case 1
		customRequest.POST = {}
		customRequest.user = AnonymousUser()
		quiz = Quiz.objects.get(slug=self.quizSlug2)
		score = scoreQuiz(quiz, customRequest, self.courseSlug, quiz.slug)
		self.failUnlessEqual(score, 0)

		# Case 2
		customRequest.POST = {'cq1':""}
		customRequest.user = User.objects.get(username="testuser")
		quiz = Quiz.objects.get(slug=quizSlug)
		score = scoreQuiz(quiz, customRequest, self.courseSlug, quiz.slug)
		self.failUnlessEqual(score, 0)

		# Case 3
		customRequest.POST = {'mcq2':1, 'cq1':"print \"Hello World\""}
		customRequest.user = User.objects.get(username="testuser")
		quiz = Quiz.objects.get(slug=quizSlug)
		score = scoreQuiz(quiz, customRequest, self.courseSlug, quiz.slug)
		self.failUnlessEqual(score, 1)

		# Case 4
		customRequest.POST = {'mcq2':2, 'cq1':"fdsd"}
		customRequest.user = User.objects.get(username="testuser")
		quiz = Quiz.objects.get(slug=quizSlug)
		score = scoreQuiz(quiz, customRequest, self.courseSlug, quiz.slug)
		self.failUnlessEqual(score, 1)

		# Case 5
		customRequest.POST = {'mcq2':2, 'cq1':"print \"Hello World\""}
		customRequest.user = User.objects.get(username="testuser")
		quiz = Quiz.objects.get(slug=quizSlug)
		score = scoreQuiz(quiz, customRequest, self.courseSlug, quiz.slug)
		self.failUnlessEqual(score, 2)

	def test_validateQuestionOrder(self):
		'''
			Test that validateQuestionOrder only returns true
			if the questions are uniquely ordered from
			1 - # of questions or returns false otherwise.

			Case no.    Input          Expected Output          Remark
			1           quiz1          true                     Quiz with all questions in valid order
			2           quiz1          false                    Quiz with first question 0, not 1
			3           quiz1          false                    Quiz with duplicate ordering
			4           quiz1          false                    Quiz with last question not last order
			5           quiz2          true                     Quiz with no questions

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

		# Case 5
		quiz = Quiz.objects.get(slug = self.quizSlug2)
		self.failUnlessEqual(validateQuestionOrder(quiz), True)

	def test_validateQuiz(self):
		'''
			Test that validateQuiz checks all fo a quizzes data and enforces
			the following validation rules:

			   Quiz Title cannot be blank
			   All prerequisites must have a corresponding passing path
			   No quesiton prompt can be blank
			   No answer can be blank
			   Questions must be in a valid ordering
			   Multiple choice questions must have a correct answer

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
			8         quiz.question2.answers < 2    errors = ["Question must have at least     Only one answer for mcq
			                                                   two possible answers"
			10        validatequiz_quiz             []                                         Valid quiz

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
		newPrereq = Prerequisite(containingQuiz = Quiz.objects.get(slug=quizSlug), requiredQuiz = Quiz.objects.get(slug="scorequiz_quiz"))
		newPrereq.save()
		quiz = Quiz.objects.get(slug=quizSlug)
		errors = validateQuiz(quiz)
		self.failUnlessEqual(errors, ["scoreQuiz_quiz does not have a passing path"])
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

		# Case 8
		answer = quiz.questions.get(order="2").multiplechoicequestion.answers.get(order="2")
		answer.delete()
		quiz = Quiz.objects.get(slug=quizSlug)
		errors = validateQuiz(quiz)
		self.failUnlessEqual(errors, ["Question must have at least two possible answers"])
		revertQuiz(quiz)

		# Case 9
		answer = quiz.questions.get(order="2").multiplechoicequestion.answers.get(order="1")
		answer.correct = False
		answer.save()
		quiz = Quiz.objects.get(slug=quizSlug)
		errors = validateQuiz(quiz)
		self.failUnlessEqual(errors, ["Question must have a correct answer"])
		revertQuiz(quiz)

		# Case 10
		newPrereq = Prerequisite(containingQuiz = Quiz.objects.get(slug=quizSlug), requiredQuiz = Quiz.objects.get(slug=self.quizSlug2))
		newPrereq.save()
		quiz = Quiz.objects.get(slug=quizSlug)
		errors = validateQuiz(quiz)
		self.failUnlessEqual(errors, [])
		revertQuiz(quiz)

"""

	The following test cases were intentionally commented out.
	I was shooting to get 100% coverage of ALL my code, but realized
	that I wouldnt have enough time. All functions tested above have 100%
	coverage. The existing tests below this did not yet have 100% coverage
	so I didnt want to submit tests that didnt have 100% coverage, as per
	requirements.

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
		self.publicCourse = 'quizviewtests_public'
		self.privateCourse = 'quizviewtests_private'
		self.quiz1 = 'quiz1'
		self.hiddenquiz = 'hiddenquiz'

	def test_show_quiz(self):
		'''
			Test that the urls to a known public quiz page works properly

			Case no.    Input                                                        Expected Output         Remark
			1           url = /course/publicCourse/page/quiz1/                       200                     302 is a found code
			2           url = /course/badCourse/page/quiz1/                          404                     404 is a bad link error
			3           url = /course/publicCourse/page/badQuiz/                     404                     404 is a bad link error
			4           url = /course/badCourse/page/badQuiz/                        404                     404 is a bad link error
			5           url = /course/publicCourse/page/hiddenquiz/                  200                     User not logged in
			                                                                         template=denied.html

			@author Evan Kleist
		'''

		# Case 1 - A good course and a good quiz should display properly	
		response = self.client.get(reverse('pages.views.show_page', args=[self.publicCourse, self.quiz1]))
		self.failUnlessEqual(response.status_code, 200)

		# Case 2 - A bad course and a good quiz should display an error
		response = self.client.get(reverse('pages.views.show_page', args=["bad-course", self.quiz1]))
		self.failUnlessEqual(response.status_code, 404) 

		# Case 3 - A good course and a bad quiz should display an error
		response = self.client.get(reverse('pages.views.show_page', args=[self.publicCourse, "badquiz"]))
		self.failUnlessEqual(response.status_code, 404) 

		# Case 4 - A bad course and a bad quiz should display an error
		response = self.client.get(reverse('pages.views.show_page', args=["bad-course", "badquiz"]))
		self.failUnlessEqual(response.status_code, 404)

		# Case 5
		response = self.client.get(reverse('pages.views.show_page', args=[self.publicCourse, self.hiddenquiz]))
		self.failUnlessEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "page/denied.html")

	def test_delete_quiz(self):
		'''
			Test that the urls to a known public quiz page works properly

			Case no.    Input                                                        Expected Output         Remark
			1           user =                                         

			@author Evan Kleist
		'''

		# Case 1
		self.client.login(username="user_notEnrolled", password="password")
		response = self.client.post('/course/'+self.publicCourse+'/page/'+self.quiz1+'/edit/', {"Delete":"true"})
		self.assertTemplateUsed(response, "page/denied.html")
		self.client.logout()

		# Case 2
		self.client.login(username="user_enrolled", password="password")
		response = self.client.post('/course/'+self.publicCourse+'/page/'+self.quiz1+'/edit/', {"Delete":"true"})
		self.assertTemplateUsed(response, "page/denied.html")
		self.client.logout()

		# Case 3
		self.client.login(username="ekleist", password="password")
		response = self.client.post('/course/'+self.publicCourse+'/page/'+self.quiz1+'/edit/', {"Delete":"true"})
		self.assertTemplateUsed(response, "page/quiz/delete_quiz.html")
		self.client.logout()

		# Case 4
		response = self.client.post('/course/'+self.publicCourse+'/page/'+self.quiz1+'/edit/', {"Delete":"true"})
		self.assertEquals(response.status_code, 302)

		# Case 4
		self.client.login(username="ekleist", password="password")
		response = self.client.post('/course/'+self.publicCourse+'/page/'+self.quiz1+'/edit/', {"ConfirmDelete":"true"})
		self.assertEquals(response.status_code, 302)
		self.client.logout()

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
		pass"""

