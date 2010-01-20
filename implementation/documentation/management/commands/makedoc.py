from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
	help = "Write HTML docs for project into current dir"
	def handle_noargs(self, **options):
		import pydoc
		import settings
		pydoc.writedocs(settings.rootPath)
