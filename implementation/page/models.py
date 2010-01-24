'''
Models file for page related classes

Contains the Overall "Page" class, plus the Classes that are primarily
contained within a Page, such as Quiz and Lesson. In addition it contains
classes for path, question, codeQuestion, multipleChoiceQuestion, and answer.

Author(s): Russell Mezzetta, Mark Gius, James Pearson

'''
from django.db import models
from courses.models import Course

# Create your models here.

class Page(models.Model):
	'''
	A single unit of a course

	A page contains links to other pages based on the Course flow.
	'''
	course = models.ForeignKey(Course)
	nextPage = models.OneToOneField("self", related_name='prevPage', null=True)	
	# prevPage implied from Page
	parent = models.ForeignKey("self", related_name='children', null=True)
	# children implied from Page
	slug = models.SlugField(unique=True)
	# prereqs: stupid.  Not doing it
	name = models.TextField()
	order = models.IntegerField()

	def __unicode__(self):
		return self.name
