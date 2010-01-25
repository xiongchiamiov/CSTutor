from django.shortcuts import render_to_response

def show_quiz(request, course, courses, pid):
	return render_to_response('quiz/index.html', {'course':course, 'courses':courses, 'pid':pid})

