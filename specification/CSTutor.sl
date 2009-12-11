object CSTutorDB
   components: userDB:UserDB and courseDB:CourseDB;
   description: (* A top level directory or database that holds all user/course  information *);
end CSTutorDB;

object UserDB
	components: userList:User*;
	description: (* A UserDB is the database that contains the userlist for a class. *);
end UserDB;

object CourseDB
   components: course:Course*;
   description: (* An object that contains all courses *);
end CourseDB;

object Course
	components: p:Page* and r:Roster and privateClass:boolean and name:string and chatRoom:string and Stats and text:string* and userDB:UserDB;
	operations: AddPage, RemovePage, SetPrivate, EditCourse;
	description: (* A course is a course. It contains zero or more pages, a course roster, a boolean determining whether or not the course is public or private, a string for the name of the course, a string for the chat room, a Stats object containing all of the course specific statistics, and a string containing a welcome text for the course *);
end Course; 

operation createLesson
	inputs: name:string and course:Course;
	outputs: newLesson:Lesson;
	precondition: ;
	postcondition: exists (page in course.p) (page.pageId = newLesson.pageId);
	description: (* A lesson is created when an user with manage permissions for a Course clicks Submit on the Add Lesson page.  createLesson takes in a string for the name and a Course in which the lesson will be contained. createLesson returns the new created Lesson *);
end createLesson;

operation removePage
	inputs: toRemove:Page and course:Course;
	outputs: success:boolean and newCourse:Course;
   precondition: exists (page in course.p) (page = toRemove);
   postcondition: forall (page in course.p) ((page = toRemove) or exists (diffpage in newCourse.p) (diffpage = page));
	description: (* A page is removed from CSTutor when the delete button is hit for the Course.  removeCourse takes in a Page, either a Lesson or Quiz, to be removed and returns a boolean saying if the delete succeeded or not *);
end removePage;

operation createCourse
	inputs: db:CourseDB and name:string and private:boolean and instructor:User; 
	outputs: newCourse:Course;
   precondition: not exists (course in db.course) (course.name = name);
   postcondition: exists (course in db.course) (course.name = name);
	description: (* A new course is created when an Instructor user clicks on the Create Class button.  createCourse takes in a string for the class name, a boolean that specifies if the class is privately or publicly available and a User which is the creator of the class.  createCourse returns a new Course in which the User passed in as the intructor has Manage permissions *);
end createCourse;

operation removeCourse
	inputs: db:CourseDB and toRemove:Course;
	outputs: success:boolean;
	precondition: exists (course in db.course) (course.name = toRemove.name);
   postcondition: not exists (course in db.course) (course.name = toRemove.name);
   description: (* A course is removed from CSTutor when the delete button is hit for the Course.  removeCourse takes in a Course to be removed and returns a boolean saying if the delete succeeded or not *);
end removeCourse;

operation SetPrivate
	inputs: db:CourseDB and current:Course;
	outputs: updatedCourse:Course;
   precondition: exists (course in db.course) (course.name = current.name);
   postcondition: ;
	description: (*Takes in a course and sets the course to be private*);
end SetPrivate;

object Page
	components: pageId:number and prevPage:number and nextPage:number and prereq:number*;
	operations: Validate, getNextPage, getPrevPage, displayPage, movePage;	
	description: (* A Page has a link to the previous and next pages, as well as zero or more Page prerequisites.*); 
end Page;
 
operation Validate
	inputs: requestedPage:Page and usersStats:Stats and course:Course;
	outputs: authenticated:boolean;
   precondition: exists (page in course.p) (page = requestedPage);
   postcondition: (* none *);
	description: (* Takes a requested page and checks to see if all of the prerequisites have been successfully completed for the student. Returns a boolean *);
end Validate;

object Lesson extends Page
	components: text:string* and code:string* and subtopic:Page*;
	operations: AddPage, RemovePage, EditLesson;
	description: (* A lesson is a specific type of Page. It contains zero or more text fields, zero or more code fields, and links to any subpages *);
end Lesson;

operation getNextPage
	inputs: current:Page;
   outputs: next:Page;
   precondition: current.nextPage != -1;
   postcondition: next.pageId = current.nextPage;
	description: (*Takes in a Page, and returns the next logical page.*);
end getNextPage;

operation getPrevPage
	inputs: current:Page;
   outputs: prev:Page;
   precondition: current.prevPage != -1;
   postcondition: prev.pageId = current.nextPage;
	description: (*Takes in a Page, and returns the previous logical page.*);
end getPrevPage;

operation displayPage
	inputs: requestedPage:Page and course:Course;
	outputs: pageSource:string;
   precondition: exists (page in course.p) (page = requestedPage);
   postcondition: (* none *);
	description:  (*Takes in a page and returns the content to display *);
end displayPage;

operation movePage
	inputs: Page and Page;
	outputs: boolean;
	description: (*Takes in two pages, the page to move and the page to 
	              place the moved page after, and moves the first page to be
	              the "next" of the second Page.  Returns boolean indicating 
	              success *);
end movePage;

object Quiz extends Page
	components: Question* and text:string* and title:string and paths:Path* and hidden:boolean;
	operations: AddQuestion, RemoveQuestion, EditQuiz, SubmitAnswers, CheckAnswers, DeterminePath;
	description: (* A quiz is a specific type of Page. It contains zero or more Questions, a title string, zero or more text fields. It also contains a link to a Page being required as a prerequisite and a boolean for visibility.*);
end Quiz;

operation createQuiz
	inputs: oldCourse:Course and newQuiz:Quiz;
	outputs: newCourse:Course;
	precondition: (newQuiz.isValid()) and (forall (q:Quiz | oldCourse.contains(q)) (q.title != newQuiz.title));
	postcondition: exists(newQuiz in oldCourse.p);
	description: (* Takes a course as well as the form submitted containing the new quiz and creates a new Course page containing the quiz *);
end createQuiz;

operation deleteQuiz
	inputs: quiz:Quiz and course:Course;
	outputs: newCourse:Course;
	precondition: exists (quiz in course.p);
	postcondition: !exists(quiz in course.p);
	description: (* Takes a course and a specified quiz and deletes the quiz from the course. It also deletes any corresponding statistics *);
end deleteQuiz;

operation editQuiz
	inputs: oldCourse:Course and oldQuiz:Quiz and modifiedQuiz:Quiz;
	outputs: newCourse:Course;
	precondition: exists(oldQuiz in oldCourse.p) and modifiedQuiz.isValid();
	postcondition: exists(modifiedQuiz in newCourse.p) and !exists(oldQuiz in newCourse.p);
	description: (* Takes an old Quiz, the Quiz containing the changes, as well as the course containing the quiz and merges the changes in the modified quiz into the old Quiz *);
end editQuiz;

operation addQuestion
	inputs: course:Course quiz:Quiz and q:Question;
	outputs: newCourse:Course and newQuiz:Quiz;
	precondition: q.isValid() and exists(quiz in course.p);
	postcondition: exists(q in newQuiz.q) and exists(newQuiz in newCourse.p);
	description: (* Takes the quiz being worked on and the question being added, and adds the question to the quiz *);
end addQuestion;

operation removeQuestion
	inputs: course:Course and quiz:Quiz and q:Question;
	outputs: newCourse:Course and newQuiz:Quiz;
	precondition: exists(quiz in course.p) and exists(q in quiz.q);
	postcondition: !exists(q in newQuiz.q) and exists(newQuiz in newCourse.p);
	description: (* Takes the quiz being worked on and the question being removed, and removes the question from the quiz *);
end removeQuestion;

operation DeterminePath
	inputs: quizScore:number and quiz:Quiz;
	outputs: Path;
   precondition: exists(p in quiz.paths) (p.minScore <= quizScore and p.maxScore > quizScore);
   postcondition: (* Path returned exists and is a path of the Quiz? *);
	description: (* DeterminePath takes in the score of a quiz and then determines the right path for a student. *);
end DeterminePath;

object Path
	components: maxScore:number and minScore:number and dialog:string and page:number and passed:boolean;
	description: (*A path determines where a student is sent after his quiz has been graded *);
end Path;

object Question
	components: text:string* and question:string;
	description: (* A Question is question. It contains a string for the prompt, and a string for the title *);
end Question;

object MultipleChoiceQuestion extends Question
	components: Answer*;
	description: (* A multiple choice question is a specific type of question. It contains a list of possible Answers. *);
end MultipleChoiceQuestion;

object CodeQuestion extends Question
	components: code:string and output:string;
	operations: compareOutput;
	description: (* A code question is a specific type of question. It allows for code to be entered which is then ran and the output is compared against predefined output. It contains a string for their code, and a string for the correct output *);
end CodeQuestion;

operation compareOutput
	inputs: userCode:string and correctOutput:string;
	outputs: correct: boolean and output:string;
   precondition: (* NONE *);
   postcondition: if (userCode = correctOutput) then correct = true else correct = false;
	description: (*This operation takes in a users code snippet, runs it, and compares the output. It returns a boolean whether the output matched, as well as the correct output.*);
end compareOutput;

object Answer
	components: answer:string and correct:boolean;
	description: (* A answer is a possible answer for a multiple choice question. It contains a string for the answer and a boolean determining whether or not the answer is correct.*);
end Answer;

object Stats
	components: User and StatsObject*;
	operations: getStats, clearStats, displayStats();
	description: (* A Stats is tied to a particular user, and has a list of notable actions performed by said user, along with the datetime of the action, and any notes that are useful for later data crunching. *);
end Stats;

operation clearStats
	inputs: stats:Stats;
	outputs: freshStats:Stats;
	description: (* Clear a set of statistics. *);
end clearStatistics;

operation displayStats
	inputs: Stats;
	outputs: string;
	description:  (*Takes in a Stats and returns the content to display *);
end displayStats;

operation getStats
	inputs: roster:Roster;
	outputs: stats:Stats;
	description: (* Get the statistics for a class from the roster *);
end getStats;

object StatsObject
	components: pageId:number and score:number and passed:boolean and date:string and notes:string;
	description: (*A stats object stores the related stats information about a page *);
end StatsObject;

object Roster
	components: (User, Permissions, Stats)*;
	operations: addUser, deleteUser, editPermissions, updateRoster;
	description: (* A roster keeps track of the permissions and statistics for all associated users. *);
end Roster;

operation addUser
	inputs: name:string and roster:Roster;
	outputs: updatedRoster:Roster;
	precondition: #name <= 25 (* The name of the given user must be unique and less than or equal to 25 characters *);
	postcondition: name in Roster (* The given name is in the updated roster *);
	description: (* addUser adds the given string name into the Roster and produces an updated Roster. *);
end addUser;

operation removeUser
	inputs: nameList:string* and roster:Roster;
	outputs: updatedRoster:Roster;
	precondition: forall(name:nameList)
						name in roster (* The given name list is in the roster. *);
	postcondition: forall(name:nameList)
						name not in roster; (* The given name list is not in the updated roster*);
	description: (* removeUser removes the inputed string names from the roster and produces an updated Roster. *);
end removeUser;

operation setUserPermissions
	inputs: permission:PermissionSet* and roster:Roster;
	outputs: updatedRoster:Roster;
	precondition: (* The inputted permission set is valid *);
	postcondition: (* The updated roster reflects the changes in the inputted permission set *);
	description: forall(permission)
						permission.name = roster.name 
						and
						permission.permissions = roster.Permissions;
(* setUserPermissions will take in a list of tuples consisting of a string name, boolean edit, boolean manage, and boolean states and will produce an updated Roster with the new user permissions. *);
end setUserPermissions;

operation updateRoster
	inputs: roster:Roster and userDB:UserDB;
	outputs: updated:Roster and UserDB;
	precondition: (* The updated roster is valid *);
	postcondition: forall(roster.user)
						roster.user in userDB;(* The updated database roster reflects the changes given by the inputed roster *);
	description: (* updateRoster will take in a roster and update the user database. *);
end updateRoster;

object Permissions
	components: view:boolean and edit:boolean and stats:boolean and manage:boolean;
	description: (* Permissions are a set of booleans that map the permissions for users. The view permission allows the user to view the course material. The edit permission allows the user to edit the course material. The stats permission allows the user to view class-wide statistics and roster. The manage permission allows the user to modify the roster and all associated permissions *);
end Permissions;

object User
	components: isInstructor:boolean and userName:string and password:string and enrolled:Course* and email:string;
	operations: editProfile, setUserPermissions;
	description: (* A user contains a boolean determining whether or not the user has instructor permissions, a string for the username, a string for the password, and a list of Courses that the user is enrolled in. Additionally, a user may provide an email address. *);
end User;

operation editProfile
	inputs: currentProfile:User and modifiedProfile:User;
	outputs: newProfile:User;
	description: (*This operation takes a users profile and any modifications and merges them together, returning an updated profile*);
end editProfile;

operation login
	inputs: username:string, password:string, userDB:UserDB;
   outputs: homePage:Page;
   precondition: exists (u in userDB) (username = u.userName) and (password = u.password);
   postcondition: (* none *);
	description: (* Takes in username and password then checks server to see if there is a
						match. If so then it grants access *);
end login;
	
operation logout
	inputs: (* none *);
   outputs: (* display the login page *);
   precondition: (* none *);
   postcondition: (* none *);
	description: (* There is nothing special done when a user logs out *);
end logout;

object PermissionSet
	components: name:string and permissions:Permissions;
	operations: editPermissions;
   description: (* A permissions set links a name to a permissions associated with the name *);
end PermissionSet;

operation editPermissions
	inputs: name:string and modifiedPermissions:Permissions and roster:Roster;
	outputs: newPermissions:Permissions;
	precondition: name in roster(* The user is a valid user in the roster and the permissions are valid *);
	postcondition: if(name = roster.name)
						modifiedPermissions = roster.Permissions;(* The new permissions of the user are the same ast he modified permissions *);
	description: (*This operation takes a user's name and a set of modified permissions, replaces the old permissions, and returns an updated permissions*);
end editPermissions;

