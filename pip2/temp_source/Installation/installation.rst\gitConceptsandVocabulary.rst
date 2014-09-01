..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

git Concepts and Vocabulary
---------------------------

git is a tool for keeping track of collections of files, and tracking multiple versions of them. The whole collection of files is called a **repository**, or **repo** for short. A **commit** defines a snapshot of the state of all the files. You can work locally, in your **working directory** with files and then, when you have them all cleaned up, you create a new commit, with a commit message that is a comment describing what you have changed since the last commit. 

.. note:: 

  "Working directory" means the directory on your computer that the command prompt is attached to. You can find out what that is by typing ``pwd`` at a command prompt, and you can change it using the command ``cd``.

You can **checkout** different commits from a repository, and revert back to earlier versions, though we won't be teaching you how to do that (yet). 

.. note:: 

  Every time you **commit** a new version of the state of all your files in a folder, that *instance of when you commit* has a unique identifier: that's ONE VERSION of your code. That's related to why it's called "version control"! We'll talk more about this later.

You can also **merge** in changes to files that other people make. git does pretty well at automatically merging changes together, but sometimes it isn't sure what was intended and you have to do that process manually. Next week we'll teach you how to do that. Hopefully, we will get through this week without needing to do any merges.

We say that one repository is a **fork** of another if it starts with the complete history of the other repository at some point in time. After the time of the fork, the two repositories may diverge. We have a main repository for the course code. You will make a fork of that repository and make changes to it, such as adding your problem set answers. You will also pull in any new code that gets added to the original repository of course code by setting up the original repository as an **upstream** repository.

Repositories can be synchronized across computers. A common setup, and one that we will use in the course, is to keep a **remote** copy of a repository on an Internet-accessible server, and keep a local repository on your private computer. We will use a free service on the Internet called BitBucket to keep the remote copies of our repositories. When we make an initial copy of a repository, we **clone** the repository. To synch any changes that other people might have made to the remote copy, we **pull** those changes from the remote. To synch any changes that we made, so that others can see them, we **push** those changes to the remote. Those words are all commands that you can use with Git in the command prompt. (Read on for more.)

