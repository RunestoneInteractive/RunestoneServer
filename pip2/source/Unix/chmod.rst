..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".


The chmod Command
-----------------

Another useful Unix command prompt command is ``chmod``. 

We've discussed the basic layout of your computer's file system -- files within directories within directories... and so on. Each directory, and file, has *permissions* as well, which determine which logged in users can access, read, and change what files. Some files require what's called **root access** to your machine -- you have to put in a password that proves you are the administrative owner before you can change them, beca use they could have a serious effect on your file system. 

In other, less serious cases, permissions might be restricted depending upon what group of users you are (you may have noticed that as a University of Michigan student you cannot do everything on a university computer that you can do on your personal laptop), or you might have multiple login accounts on your computer but only one of them has permission to access your course folders. Many people have not explicitly dealt with any permissions on their personal laptops, but how to manage permissions is useful to know in collaborative environments.

``chmod`` is the command that allows access to and change of permissions on a file or directory. To understand it, there are a few symbols to be aware of.

The syntax is as follows: ``chmod [any options] mode[,mode] file1 file2`` -- where **file1** and **file2** are actual files whose permissions you are working with.

``rwx`` stands for read permissions (read a file), write permissions (make changes to a file and save them), and permissions to execute a file (e.g. run a Python file or another piece of software). Numbers represent different possible permissions. The table below shows the options:

#	Permission	rwx
7	read, write and execute	111
6	read and write	110
5	read and execute	101
4	read only	100
3	write and execute	011
2	write only	010
1	execute only	001
0	none	000

But even easier, there are letters that represent whole groups of users. ``u`` means a user, ``g`` is for a group, and ``o`` is for others -- people who are not specific users or in a specific group.


For example, if you wanted to give **execute access** on a file ``sampleFile.py`` that you recently saved, you would ``cd`` to the directory where it is saved, and type at the command prompt:

``chmod a+x sampleFile.py``

This tells the computer, 'change permissions such that all people can run the file sampleFile.py'

If you wanted to revoke all permissions on that same file for all users, you would:

``chmod u-rx sampleFile.py``

This tells the computer, 'change permissions such that the user cannot read or write to the file sampleFile.py'.

There are many reasons that permissions may be relevant to a programmer working on collaborative projects, but understanding that these permissions exist is an important part of getting a sense for your Unix environment.