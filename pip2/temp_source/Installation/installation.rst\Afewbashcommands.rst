..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

A few bash commands
-------------------

Here are a few commands that you'll be using all the time. Try experimenting with them.

#. ``ls`` is the command to list the contents of the current directory

#. ``ls -l`` will show more details about each of the files, such as when they were last saved

#. ``pwd`` will show you what the current **working directory** is, the directory that you are currently attached to.

#. ``cd <path>`` will connect to the directory you specify

   * If ``<path>`` begins with ``/`` it is an absolute path, meaning you have to specify the complete path. For example, ``/c/Users/presnick/``
   
   * If ``<path>`` does not being with ``/`` it is a relative path. It specifies a subdirectory of the current directory. For example, if you are connected to ``/c/Users/``, then ``cd presnick`` will connect you to ``/c/Users/presnick/``
   
   * If ``<path>`` is ``..``, then it moves you up to the parent directory. For For example, if you are connected to ``/c/Users/``, then ``cd ..`` will connect you to ``/c/``.
   
#. ``cat <fname>`` will print out the contents of <fname>, assuming <fname> is a file in the current directory.



.. _git_workflow:

