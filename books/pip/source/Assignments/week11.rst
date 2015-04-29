:orphan:

..  Copyright (C) Paul Resnick.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

.. highlight:: python
    :linenothreshold: 500


Week 11: ends April 4, 2014
===========================

For this week you have the following graded activities:

1. Prepare for classes

   * Before Tuesday's class:  
      * :ref:`Accumulation with map, filter, reduce, and list comprehensions <listcomp_chap>`         
      * get the code file lectures/session22.py via Bitbucket.org
         * ``git pull upstream master``
      * try to do the exercises in session22.py
   
   * Before Thursday's class:
      * Read chapter 1 and chapter 2 up through section 2.5 in `Pro Git <http://git-scm.com/book>`_
      * Read chapters 3.1 and 3.2 in `Pro Git <http://git-scm.com/book>`_ Don't worry too much about the details in this part, except do get familiar with the idea of how to `resolve a conflicted merge <http://git-scm.com/book/en/Git-Branching-Basic-Branching-and-Merging#Basic-Merge-Conflicts>`_ by manually editing the file. 
      * Answer the questions :ref:`below <session23>`
 
#. Turn in the reading response, by 8 PM the night before your registered section meets.

   * Read *The Success of Open Source*, Chapter 4
   * :ref:`Reading response 10 <response_10>`

#. Do Problem Set 10:

   * See /ps10 folder distributed via Bitbucket.org (coming soon)


.. _response_10:

Reading Response 10
-------------------

The chapter describes forking as something that could fragment developer efforts and thus slow down progress of a project. If you tried to make a "fork" of Linux today, would it be technically feasible to do so? What do you think would happen?
  
.. actex:: rr_10_1

   # Fill in your response in between the triple quotes
   s = """

   """

Pages 116-119 describes the genesis of "Bitkeeper", which later was replaced by git. Why would the promise of switching to use something like git have helped to defuse a potential forking of the Linux project? 

.. actex:: rr_10_2

   # Fill in your response in between the triple quotes
   s = """

   """

What material from the chapter would you like to discuss in class?

.. actex:: rr_10_3

   # Fill in your response in between the triple quotes
   s = """

   """

.. _session23:

.. qnum::
   :prefix: session23-
   :start: 1

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
            

