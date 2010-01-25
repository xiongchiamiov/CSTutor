from django.shortcuts import render_to_response
from courses.models import Course

def create_quiz(request):
	print "Create Quiz\n" #TODO
	return render_to_response('quiz/create-quiz.html', {'courses': Course.objects.all()})

def show_quiz(request, course, courses, pid):
	#page = Quiz.objects.get(slug=pid)
	#questions = page.questions.all()
	return render_to_response('quiz/index.html', {'course':course, 'courses':courses, 'pid':pid})

