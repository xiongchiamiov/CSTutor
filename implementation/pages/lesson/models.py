from django.db import models
from pages.models import Page

# Create your models here.

class Lesson(Page):
	'''
	Model for a Lesson.

	A lesson is a specific type of Page.  It represents a single Topic that
	is represented on a single "Page."  Lessons can include executable code
	segments and images.
	'''
	content = models.TextField()

	def __unicode__(self):
		return self.content
	
	def get_absolute_url(self):
		return ('pages.lesson.views.show_page', \
				  [str(self.course.slug), self.slug])
