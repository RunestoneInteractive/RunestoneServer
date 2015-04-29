..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Command Line and Files
----------------------

The command prompt, or command line, is a way for you, a human programmer, to tell the computer what to do: what programs to use or run or open, what files to access, stuff like that. (If we say "the command line" or "the terminal window" that means the same thing as "command prompt". It'll look slightly different depending on your operating system, and it may work differently in a few small ways depending on your operating system, but it's all the same thing.) 

The command prompt has a special language of its own so you can find places (directories, or folders) in your computer without navigating through the images of folders and clicking on stuff. You'll be learning a few of the special commands that you can use at the command prompt.

When you use ``print`` in a code file and run the program using the command line as described (at a high level) above, the stuff you print will appear in the command prompt window also. We'll still call that the **console**. Just like we saw in the online environment, printing stuff happens for the benefit of the people who can see the screen. 

Your Python programs can also access files, using the ``open`` command. When you have python set up on your computer, the files that are opened will be files on your computer. One new thing you'll be able to do that you couldn't do in the online environment was have your program write text or other data to a file on your computer's file system.

.. note:: 

  The bit after the dot on a file is called the *file extension*, which tells the computer what *kind* of file it is and helps you figure out what programs you can open it with. Just like when you save an Excel spreadsheet with the ``.xlsx`` extension, saving a file with a ``.txt`` extension means it is *plain text*, and saving a file with a ``.py`` extension means that it is a *Python file*, which you can run.

As you write code, you'll want to keep track of what you change, as well as putting your homework somewhere for it to be graded. We'll use a **version control** system called **git** to do this, which you can read about later in this chapter.


Preparing Your Computer for the Rest of the Course
==================================================

We will walk you through the process of setting up your computer to run Python natively. It will
involve the following steps:

1. Create a directory (folder) where your code for this course will live.

#. Install and configure a text editor

#. Install and configure Python

#. Install and configure git on your computer 

#. Fork and Clone the git repository for code samples and exercises


The instructions diverge here for the first four steps, depending on whether you are on Windows or a Mac. (If you're on
Linux, we presume that you know what you're doing already and can make appropriate
improvisations from the instructions for Windows or Mac, but feel free to ask.) Once your basic environment
is set up, you will Clone the Git repository in the same way, on either platform.

* :ref:`Windows instructions <windows_install>`

* :ref:`Mac instructions <mac_install>`

* :ref:`Fork and Clone the git repository <git_repos>`

.. _windows_install:

Windows Instructions
====================

