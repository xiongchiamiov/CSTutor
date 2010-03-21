'''
Contains the lesson model

@author Russell Mezzetta
@author Mark Gius
'''
from django.db import models
from pages.models import Page

# Create your models here.

class Lesson(Page):
	'''
	Model for a Lesson.

	A lesson is a specific type of Page.  It represents a single Topic that
	is represented on a single "Page."  Lessons can include executable code
	segments and images.

	@author Russell Mezzetta
	@author Mark Gius
	'''
	content = models.TextField()
	workingCopy = models.TextField()

	def __unicode__(self):
		'''
		Like toString in java
	
		@author Mark Gius
		'''
		return self.content
	
	def get_absolute_url(self):
		'''
		Constructs a url based on an in memory object.

		deprecated	

		@author Mark Gius
		'''
		return ('pages.lesson.views.show_page', \
				  [str(self.course.slug), self.slug])
