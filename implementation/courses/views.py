# Create your views here.
def show_roster(request):
	courseid = request.GET['courseid']
	course = Courses.objects.filter(id=courseid)
   enrollments = course.roster.all();
	userList = []

   for enrollment in enrollments:
      #do something
		userList.append(user.name)

	return render_to_response('roster/index.html', {'course', course, 'users', usersList,}
