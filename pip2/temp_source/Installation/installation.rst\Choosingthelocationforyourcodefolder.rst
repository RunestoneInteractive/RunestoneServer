..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Choosing the location for your code folder
------------------------------------------

When you start git bash, you will be connected to a folder like /c/Users/presnick, which corresponds
to the Windows file path c:\\Users\\presnick. Of course, instead of presnick, it will
be your Windows username. To see what directory you are in, at the command prompt you
can type ``pwd``.

#. When you use git, as described further on, a subdirectory will be created for you automatically. If you want that subdirectory to be underneath c:\Users\<yourWindowsUsername>, then you're done with this step. That's what I recommend. If you want it to be somewhere else, you will need to figure out the correct "path" to it, and figure out how to translate that path into the unix format so that you can issue the appropriate ``cd`` command. (I have chosen to put my code in c:\\Users\\presnick\\106code, which translates in to /c/Users/presnick/106code in the unix path format.)

#. Go back to Notedpad++ and resave firstprog.py into c:\Users\<yourWindowsUsername>. You can navigate to that directory when doing a Save As in NotePad++ by starting at C:, then going to Users, then your Windows username.

#. The unix command for listing the contents of a directory is ls. In git bash, type ``ls``. You should now see firstprog.py is a file in that directory. You may see lots of other files as well, if you stayed in the default location of /c/Users/<yourWindowsUsername>.

#. At gitbash, type ``python firstprog.py``. It should print out ``hello world`` as shown in the figure.

.. image:: Figures/directory.JPG

