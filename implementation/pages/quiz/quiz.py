'''
quiz.py fil for quiz related operations.

Contains operations for all lessons

@author Evan Kleist
'''
from django.template.defaultfilters import slugify
from models import *
from question.models import *
from question.question import isMultipleChoiceQuestion
from question.question import removeQuestion
from pages.page import removePage
from stats.models import Stat


def addMultipleChoiceQuestion(self):
	'''
		Takes a quiz and adds a blank multiple choice question to it
	'''
	questions = self.questions.all()
	newQuestion = MultipleChoiceQuestion(order=(len(questions)+1), quiz=self)
	newQuestion.save()
	return newQuestion

def addCodeQuestion(self):
	'''
		Takes a quiz and adds a blank code question to it
	'''
	questions = self.questions.all()
	newQuestion = CodeQuestion(order=(len(questions)+1), quiz=self)
	newQuestion.save()
	return newQuestion

def addPath(self, request, course_slug):
	'''
		Takes a working copy of a quiz, a request containing post data, and a course_slug
		and adds a path to the quiz
	'''
	errors = []
	try:
		lowScore = int(request.POST["LowScore"])
		if (lowScore < 0 or lowScore > 100):
			errors.append("Low Score must be between 0 and 100")

		try:
			matchingPath = matchPath(self, lowScore)
			errors.append("Conflicting path ranges. Please change the range")
		except NoMatchingPath:
			pass			
	except ValueError:
		errors.append("Low Score must be an integer")

	try:
		highScore = int(request.POST["HighScore"])
		if (highScore < 0 or highScore > 100):
			errors.append("High Score must be between 0 and 100")
		if (highScore < lowScore):
			errors.append("High Score must be less than Low Score")
	except ValueError:
		errors.append("High Score must be an integer")

	course = Course.objects.get(slug=course_slug)
	page = course.pages.get(slug=request.POST["pathPage"])
	passing = "passing" in request.POST
	dialogue = request.POST["dialogue"]

	if (len(errors) == 0):
		newPath = Path(quiz = self, highscore = highScore, lowscore = lowScore, toPage = page, passed = passing, text = dialogue)
		newPath.save()

	return errors

def matchPath(self, score):
	'''
		This function takes a quiz and a "score" on the quiz, represented as a percentage,
		and returns the quiz path that the score matches. If no matching path
		is found, it raises the NoMatchingPath exception.
	'''
	paths = self.paths.all()

	for p in paths:
		if (score >= p.lowscore and score < p.highscore):
			return p
		if (score == p.highscore and score == 100):
			return p

	raise NoMatchingPath

def checkPrerequisites(self, user):
	'''
		This function takes a quiz and a user. It then loooks the user's
		statistics up and makes sure all of the quizzes prerequisites
		have been met. If the user has edit permissions on the course,
		then it returns true. Otherwise, it returns true if all prereqs
		have been met and false if not.
	'''
	prereqs = self.prerequisites.all()
	if (len(prereqs) > 0):
		if (user.isAnonymous()):
			return False
		enrollment = user.enrollments.get(course=self.course)
		if (not enrollment.edit):
			for p in prereqs:
				print "Prereq: " + p.requiredQuiz.slug + "\n"
				requiredQuiz = p.requiredQuiz
				#score = getUserBestQuizScore(requiredQuiz, user)
				score = 100
				path = matchPath(requiredQuiz, score)
				print "User Score on Prereq: " + str(path.passed) + "\n"
				if (path.passed == False):
					return False

	return True

def copyQuiz(quiz1, quiz2):
	'''
		Takes two quizzes and copies the contents of quiz1 into quiz2
	'''

	# Copy Title
	quiz2.text = quiz1.text
	quiz2.name = quiz1.name

	# Copy Hidden
	quiz2.hidden = quiz1.hidden

	# Copy Prerequisites
	curPrereqs = quiz2.prerequisites.all()
	for p in curPrereqs:
		p.delete()
	curPrereqs = quiz1.prerequisites.all()
	for p in curPrereqs:
		newPrereq = Prerequisite(containingQuiz = quiz2, requiredQuiz = p.requiredQuiz)
		newPrereq.save()

	# Copy Paths
	curPaths = quiz2.paths.all()
	for p in curPaths:
		p.delete()
	curPaths = quiz1.paths.all()
	for p in curPaths:
		newPath = Path(quiz = quiz2, lowscore = p.lowscore, highscore = p.highscore, text = p.text, passed = p.passed, toPage = p.toPage)
		newPath.save()

	# Copy Questions
	curQuestions = quiz2.questions.all()
	for q in curQuestions:
		removeQuestion(q)
	curQuestions = quiz1.questions.all()
	for q in curQuestions:
		if (isMultipleChoiceQuestion(q)):
			q = q.multiplechoicequestion
			newQ = MultipleChoiceQuestion(text = q.text, order = q.order, quiz = quiz2)
			newQ.save()
			# Copy Answers
			curAnswers = q.answers.all()
			for a in curAnswers:
				newA = Answer(question = newQ, correct = a.correct, order = a.order, text = a.text)
				newA.save()
		else:
			q = q.codequestion
			newQ = CodeQuestion(text = q.text, order = q.order, quiz = quiz2, beforeCode = q.beforeCode, showBeforeCode = q.showBeforeCode, editableCode = q.editableCode, afterCode = q.afterCode, showAfterCode = q.showAfterCode, expectedOutput = q.expectedOutput)
			newQ.save()

		quiz2.save()

def editPath(self, request, course_slug):
	'''
		Takes a working copy of a quiz, a request containing post data, and a course_slug
		and edits the matching path of the quiz
	'''
	errors = []
	path = int(request.POST["path"])
	path = self.paths.get(lowscore=request.POST["path"])

	try:
		lowScore = int(request.POST["LowScore"])
		if (lowScore < 0 or lowScore > 100):
			errors.append("Low Score must be between 0 and 100")

		try:
			matchingPath = matchPath(self, lowScore)
			if (matchingPath != path):
				errors.append("Conflicting path ranges. Please change the range")
		except NoMatchingPath:
			pass			
	except ValueError:
		errors.append("Low Score must be an integer")

	try:
		highScore = int(request.POST["HighScore"])
		if (highScore < 0 or highScore > 100):
			errors.append("High Score must be between 0 and 100")
		if (highScore < lowScore):
			errors.append("High Score must be less than Low Score")
	except ValueError:
		errors.append("High Score must be an integer")

	if (path.passed == True and not "passing" in request.POST):
		# Trying to change a path to go from passing to not passing
		# If other quizzes require this quiz as a prerequisite,
		# make sure an alternate passing path is available
		paths = self.paths.all()
		otherPassing = False
		for p in paths:
			if (p.passed and p.lowscore != path.lowscore):
				otherPassing = True
		if (otherPassing == False):
			# No passing path so make sure no quizzes require it as a prerequisite
			course = self.course
			for quiz in course.pages.all():
				try:
					quiz = quiz.quiz
					if (quiz.slug == safeSlug(quiz.slug)):
						prereqs = quiz.prerequisites.all()
						for p in prereqs:
							if (p.requiredQuiz.slug == safeSlug(self.slug)):
								# A quiz requires this quiz as a prerequisite
								# and no pathing pass exists, error
								errors.append(quiz.name + " requires this quiz as a prerequisite and no other passing path exists")
				except Quiz.DoesNotExist:
					pass

	course = Course.objects.get(slug=course_slug)
	if (len(errors) == 0):
		path.lowscore = lowScore
		path.highscore = highScore
		path.toPage = course.pages.get(slug=request.POST["pathPage"])
		path.text = request.POST["dialogue"]
		path.passed = "passing" in request.POST
		print request.POST
		path.save()
	
	return errors

def removePath(self, request):
	'''
		Takes a working copy of a quiz and a request containing post data and
		removes the path from the quiz
	'''
	errors = []
	course = self.course
	path = self.paths.get(lowscore = request.POST["path"])
	# See if there is still a passing path
	paths = self.prerequisites.all()
	passingPath = False
	for p in paths:
		if (p.passed == True and not p.lowscore == path.lowscore ):
			passingPath = True
	
	if (passingPath == False):
		# No passing path so make sure no quizzes require it as a prerequisite
		for quiz in course.pages.all():
			try:
				quiz = quiz.quiz
				if (quiz.slug == safeSlug(quiz.slug)):
					prereqs = quiz.prerequisites.all()
					for p in prereqs:
						if (p.requiredQuiz.slug == safeSlug(self.slug)):
							# A quiz requires this quiz as a prerequisite
							# and no pathing pass exists, error
							errors.append(quiz.name + " requires this quiz as a prerequisite and no other passing path exists")
			except Quiz.DoesNotExist:
				pass

	if (len(errors) == 0):
		path.delete()

	return errors

def publishQuiz(self):
	''' 
		Takes a working copy of a quiz and copies it over to the published copy
	'''
	publishedSlug = safeSlug(self.slug)
	publishedQuiz = Quiz.objects.get(slug=publishedSlug)
	
	copyQuiz(self, publishedQuiz)
	publishedQuiz.upToDate = True
	publishedQuiz.save()

			

def removeQuiz(self):
	'''
		Removes a quiz from the database, as well as all related 
		objects
	'''
	questions = self.questions.all()
	prerequisites = self.prerequisites.all()
	paths = self.paths.all()
	workingQuiz = Quiz.objects.get(slug=(self.slug + "_workingCopy"))
	workingQuestions = workingQuiz.questions.all()
	workingPrerequisites = workingQuiz.prerequisites.all()
	workingPaths = workingQuiz.paths.all()

	# Remove Questions
	for q in questions:
		removeQuestion(q)
	for q in workingQuestions:
		removeQuestion(q)

	# Remove Prerequisites
	for p in prerequisites:
		p.delete()
	for p in workingPrerequisites:
		p.delete()

	# Remove Paths
	for p in paths:
		p.delete()
	for p in workingPaths:
		p.delete()

	# Remove Pages
	removePage(self)
	removePage(workingQuiz)
	# should also remove all associated quiz objects such as stats, questions, answers, paths
	return 0

def reorderQuestions(self):
	'''
		Takes a quiz, retrieves its questions, and then reorders the 
		questions into a valid state.
	'''
	questions = self.questions.all().order_by("order")
	qNum = 1
	for q in questions:
		q.order = qNum
		q.save()
		qNum = qNum + 1
	# Sanity check to make sure the question ordering is still valid
	if (validateQuestionOrder(self)):
		return 0
	return -1

def revertQuiz(self):
	'''
		Takes a working copy of a quiz and reverts it to its published version
	'''
	publishedSlug = safeSlug(self.slug)
	publishedQuiz = Quiz.objects.get(slug=publishedSlug)
	
	copyQuiz(publishedQuiz, self)
	publishedQuiz.upToDate = True
	publishedQuiz.save()


def safeSlug(page_slug):
	'''
		Takes a quiz slug and makes sure they are not trying to directly access
		the working copy. If so, it returns the slug to the published copy
	'''

	if (page_slug.endswith("_workingCopy") != False and page_slug.find("_workingCopy") == len(page_slug) - 12):
		return page_slug[:-12]

	return page_slug
		

def saveQuiz(request, course, pid):
	'''
		Takes a request, a course, and a page id. It then pulls the 
		quiz from the post data and updates the elements in the 
		database. Before saving, it validates for proper data
	'''
	data = {}
	errors = []
	quiz = Page.objects.get(slug=(pid + "_workingCopy")).quiz
	publishedQuiz = Page.objects.get(slug=pid).quiz

	if (request.method != "POST"):
		errors.append("Trying to save quiz from a non POST request")

	elif "Save" in request.POST or "Publish" in request.POST:
		errors = validateQuizFromPost(quiz, request)
		if (len(errors) == 0):
			quiz.text = request.POST["quizTitle"]
			quiz.name = request.POST["quizTitle"]
			publishedQuiz.slug = slugify(quiz.name)
			quiz.slug = publishedQuiz.slug + "_workingCopy"
			if "hidden" in request.POST:
				quiz.hidden = True
			else:
				quiz.hidden = False
			# Delete current prerequisites
			for p in quiz.prerequisites.all():
				p.delete()
			if "prereqs" in request.POST:
				# Create prerequisites
				for p in request.POST.getlist("prereqs"):
					reqQuiz = Course.objects.get(slug=course).pages.get(slug=p).quiz
					newPrereq = Prerequisite(containingQuiz=quiz, requiredQuiz=reqQuiz)
					newPrereq.save()
				
			questions = quiz.questions.all()
			for q in questions:
				if (isMultipleChoiceQuestion(q)):
					q = q.multiplechoicequestion
					for a in q.answers.all():
						a.text = request.POST['mcq%sa%s' % (q.order, a.order)]
						a.correct = (request.POST['mcq%sac' % q.order] == str(a.order))
						a.save()
					q.text = request.POST['mcq%stext' % q.order]
					q.order = request.POST['mcq%sorder' % q.order]
				else:
					q = q.codequestion
					q.text = request.POST['cq%stext' % q.order]
					q.expectedOutput = request.POST['cq%seo' % q.order]
					q.order = request.POST['cq%sorder' % q.order]
				q.save()

			publishedQuiz.upToDate = False
			quiz.save()
			publishedQuiz.save()

	data = {"quiz_slug":publishedQuiz.slug, "errors":errors}
	return data

def scoreQuiz(self, request, course_slug, quiz_slug):
	'''
		Takes a quiz and a request. Pulls the submitted answers from 
		the form contained in the request and compares it to the 
		correct answers specified in the quiz. Generates a statistic 
		for a quiz, adds it to the database and returns their score.
	'''
	questions = self.questions.all()
	course = Course.objects.get(slug=course_slug)
	score = 0

	for q in questions:
		if (isMultipleChoiceQuestion(q)):
			q = q.multiplechoicequestion
			if ('mcq%s' % q.order) in request.POST:
				theirAnswer = request.POST['mcq%s' % q.order]
				if (q.answers.get(order=theirAnswer).correct):
					score = score + 1
		else:
			q = q.codequestion
			print "Grade code question\n"

	if (not request.user.is_anonymous()):
		Stat.CreateStat(course, self, request.user, score)
	
	return score

def validateQuestionOrder(self):
	'''
		Takes in a quiz, and verifies that all of its questions have
		a unique ordering, and are ordered from 1 -> # of questions

		Returns True if the above constraints are met, False otherwise
	'''
	questions = self.questions.all()
	usedNumbers = set([question.order for question in questions])
	if (len(questions) == 0):
		return True
	if len(questions) != len(usedNumbers) or \
		min(usedNumbers) != 1 or max(usedNumbers) != len(questions):
			return False
	return True

def validateQuizFromPost(self, request):
	'''
		Takes a request containing POST data for a quiz and makes sure
		any changed elements are valid. It returns and array array of
		or an emtpy array if no errors were found
	'''
	errors = []
	questions = self.questions.all();
	
	# Title - Make sure its not blank
	if (len(request.POST["quizTitle"]) == 0):
		errors.append("Quiz Title can not be blank")

	# Title - Make sure its not a duplicate in the course
	try:
		quiz = Quiz.objects.get(slug=slugify(request.POST["quizTitle"]) + "_workingCopy")
		if (quiz.pk != self.pk):
			errors.append("Quiz Title already exists!")
	except Quiz.DoesNotExist:
		pass

	# Hidden - There can be no errors in this

	# Prerequisites - Make sure the required quiz(s) have a "passing" path
	for prereq in request.POST.getlist("prereqs"):
		requiredQuiz = Quiz.objects.get(slug = prereq)
		foundPath = False
		for path in requiredQuiz.paths.all():
			if (path.passed == True):
				foundPath = True
		if (foundPath == False):
			errors.append(requiredQuiz.name + " does not have a passing path")

	for q in questions:
		if (isMultipleChoiceQuestion(q)):
			# Multiple Choice Question - Make sure its not blank
			q = q.multiplechoicequestion
			if (len(request.POST["mcq%stext" % q.order]) == 0):
				errors.append("Question cannot have a blank prompt")

			answers = q.answers.all()
			
			# Question must have at least two possible answers
			if (len(answers) < 2):
				errors.append("Answer must have at least two possible answers")

			for a in answers:
				# Answer must not be blank
				if (len(request.POST["mcq%sa%s" % (q.order, a.order)]) == 0):
					errors.append("Answer must not be blank")

			# Question must have a correct answer
			if (not ("mcq%sac" % q.order) in request.POST):
				errors.append("Question must have a correct answer")
		else:
			q = q.codequestion
			
			# Prompt must not be blank
			if (len(request.POST["cq%stext" % q.order]) == 0):
				errors.append("Code Question prompt must not be blank")

			# Expected output must not be blank
			if (len(request.POST["cq%seo" % q.order]) == 0):
				errors.append("Code Question expected output must not be blank")

	# Question Ordering - Must be valid
	if (not validateQuestionOrder(self)):
		errors.append("Questions must have a valid ordering")

	return errors
	
