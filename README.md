Checking out the project
------------------------
    git clone git://github.com/xiongchiamiov/CSTutor.git
    cd CSTutor
    git svn init -s --prefix=origin/ https://autotutor.csc.calpoly.edu/svn

Making changes
--------------
    git svn fetch
    git svn rebase
    [hack hack hack]
    git add .
    git commit -m 'a super-helpful message'
    git svn dcommit

