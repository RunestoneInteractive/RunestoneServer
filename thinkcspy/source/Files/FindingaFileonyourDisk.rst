..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

.. qnum::
   :prefix: file-1-
   :start: 1

Finding a File on your Disk
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Opening a file requires that you, as a programmer, and Python agree about the location of the file on your disk.  The way that files are located on disk is by their **path**  You can think of the filename as the short name for a file, and the path as the full name.  For example on a Mac if you save the file ``hello.txt`` in your home directory the path to that file is ``/Users/yourname/hello.txt``  On a Windows machine the path looks a bit different but the same principles are in use.  For example on windows the path might be ``C:\Users\yourname\My Documents\hello.txt``

You can access files in folders, also called directories, under your home directory by adding a slash and the name of the folder.  For example, if you had a file called ``hello.py`` in a folder called ``CS150``  that was inside a folder called ``PyCharmProjects`` under your home directory, then the full name for ``hello.py`` stored in the CS150 folder would be ``/Users/yourname/PyCharmProjects/CS150/hello.py``

Here's the important rule to remember:  If your file and your Python program are in the same directory you can simply use the filename. ``open('myfile.txt', 'r')`` If your file and your Python program are in different directories then you should use the path to the file ``open('/Users/joebob01/myfile.txt', 'r')``.

