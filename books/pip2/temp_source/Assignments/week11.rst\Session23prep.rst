..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Session 23 prep
---------------

.. mchoicemf:: session23_1
   :answer_a: git clone newone.txt
   :answer_b: git add newone.txt
   :answer_c: git merge newone.txt
   :answer_d: git commit -m"a commit message"
   :answer_e: git push origin master
   :correct: b
   :feedback_a: clone makes a new copy of an entire repository
   :feedback_b: add can be used to take a file that is untracked, or one that is modified, and move it to the staging status
   :feedback_c: merge is to incorporate all the changes from one branch into another branch
   :feedback_d: commit takes all the staged files and makes a new snapshot that contains those files. Afterwards, it moves them from the staged to the unmodified state
   :feedback_e: push sends all commits to a remote server
   
   What is the git command to start tracking a previously untracked file named newone.txt?   

.. mchoicemf:: session23_2
   :answer_a: git clone newone.txt
   :answer_b: git add newone.txt
   :answer_c: git merge newone.txt
   :answer_d: git commit -m"a commit message" 
   :answer_e: git push origin master
   :correct: d
   :feedback_a: clone makes a new copy of an entire repository
   :feedback_b: add stages a file; it doesn't commit it
   :feedback_c: merge is to incorporate all the changes from one branch into another branch
   :feedback_d: commit takes all the staged files and makes a new snapshot that contains those files. Afterwards, it moves them from the staged to the unmodified state.
   :feedback_e: push sends all commits to a remote server
   
   What is the git command to take a snapshot of all the staged files and move them to the unmodified state?   

.. mchoicemf:: session23_3
   :answer_a: git clone newone.txt
   :answer_b: git add newone.txt
   :answer_c: git merge newone.txt
   :answer_d: git commit -m"a commit message"
   :answer_e: git push origin master
   :correct: e
   :feedback_a: clone makes a new copy of an entire repository
   :feedback_b: add can be used to take a file that is untracked, or one that is modified, and move it to the staging status
   :feedback_c: merge is to incorporate all the changes from one branch into another branch
   :feedback_d: commit takes all the staged files and makes a new snapshot that contains those files. Afterwards, it moves them from the staged to the unmodified state
   :feedback_e: push sends all commits to a remote server
   
   What is the git command to send all the commits you've made to a repository on bitbucket or some other server?   

.. mchoicemf:: session23_4
   :answer_a: git pull upstream master, then git push origin master
   :answer_b: git pull origin master, then git push origin master
   :answer_c: git commit, then git push origin master
   :answer_d: go into the Arboretum and throw your computer into the Huron River
   :correct: b
   :feedback_a: Someone made changes to the origin repository that you need to merge in, not changes to the upstream repository
   :feedback_b: Someone made changes to the origin repository that you need to merge in. This will typically happen when there's someone else you are collaborating with on a code project and they  have committed and pushed some changes.
   :feedback_c: The error message is not telling you anything about uncommitted changes that need to be committed
   :feedback_d: Hey, there's toxic stuff in computers. You don't want to pollute the river.
   
   Suppose you run git push origin master and you get an error message that reads, "Updates were rejected because the tip of your current branch is behind its remote counterpart. Merge the remote changes (e.g., 'git pull') before pushing again. What should you do?  


.. mchoicemf:: session23_5
   :answer_a: figure out which files are conflicted by running git status; manually edit them to remove the lines with <<<<<<, ========, and >>>>>>; then git add each of the files and git commit
   :answer_b: ignore it, because it doesn't really matter
   :answer_c: git commit, then git push origin master
   :correct: a
   :feedback_a: It's painful, but that's whay you've got to do. git found multiple versions of some lines of code, and you need to manually edit the files to decide what you really want to be in those files. 
   :feedback_b: Ignore it, and you're going to have a bad time. Next time you try to make a commit, you won't be able to, and you'll have to resolve it then.
   :feedback_c: That's not going to help with this problem.
   
   Suppose you run ``git pull origin master`` or ``git pull upstream master`` and you get a message about a conflict in the merge. What should you do?  

.. mchoicemf:: session23_6
   :answer_a: search online for a tutorial on how to use the vim editor, enter a commit message, and then save it
   :answer_b: type :q and then do git commit -m"some commit message"
   :correct: b
   :feedback_a: Actually, you could do this. Learning a little vim might be helpful for you. But it's kind of painful.
   :feedback_b: For the novice, :q is the most important vim command. Next time, don't forget the -m flag when you run git commit. 
   
   Suppose you run ``git commit`` and you get a whole screenful of text that looks something like this. What should you do? 

   .. sourcecode:: python
   
         
         # Please enter the commit message for your changes. Lines starting
         # with '#' will be ignored, and an empty message aborts the commit.
         # On branch master
         # Your branch is up-to-date with 'origin/master'.
         #
         # Changes to be committed:
         #  new file:   inclass/session23.py
         #
         # Changes not staged for commit:
         #  modified:   inclass/session20.py
            
