from django.shortcuts import render_to_response

def show_lesson(request, course, courses, pid, lessonContent):
	return render_to_response('page/lesson/index.html', 
									{'course':course, 'courses':courses, 'pid':pid, 'lessonContent': lessonContent})

