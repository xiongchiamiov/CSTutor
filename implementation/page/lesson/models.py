from django.db import models
from page.models import Page

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
