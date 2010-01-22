from django.shortcuts import render_to_response
from page.models import page

def show_page(request, course, courses, pid):
	page = page.objects.get(slug=pid)
	
	if page.__class__ == 'page.models.Quiz':
		return show_quiz(request, course, courses, pid)

def show_quiz(request, course, courses, pid):
	return render_to_response('quiz/index.html', {'course':course, 'courses':courses, 'pid':pid})

