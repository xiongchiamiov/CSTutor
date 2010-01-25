from django.db import models
from page.models import Page
from views import show_lesson

# Create your models here.

class Lesson(Page):
	'''
	Model for a Lesson.

	A lesson is a specific type of Page.  It represents a single Topic that
	is represented on a single "Page."  Lessons can include executable code
	segments and images.
	'''
	content = models.TextField()
	# code?  Not sure how to handle

	def show(self, request, course_slug, courses, pid):
		#import pdb; pdb.set_trace()
		#p = Page.objects.get(slug = pid)
		#print self.content
		return show_lesson(request, course_slug, courses, pid, self.content)

