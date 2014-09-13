..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Directories and Paths
---------------------

When you navigate through the files on your computer, you probably click on folder icons. You can save files in folders, also known as **directories**, and you can create directories within other directories.

Navigating through the Unix file system means you are going from one directory to another in the command line interface on your computer (in this class, probably using the application **Terminal**, if you use a Mac, or **Git Bash**, if you use Windows).

Directories map to **paths**. A path is text that describes exactly what location something is in your file system on your computer. For example, if my computer account is called ``Jackies-Laptop``, the path to my **Desktop** directory is ``Users/Jackies-Laptop/Desktop``. (Even though you can see all the things laid out on your desktop background, that's just a nice way of looking at them for humans -- your Desktop is a directory the same way a folder you keep your SI 106 notes in is a directory!)

When you are in a command prompt window, you are always acting in some particular directory. When you open it, you start out at your home directory. You can see where you are by looking at the string in the prompt. For example, this is what it looks like in a Desktop directory:

.. image:: Figures/promptstring.JPG


Unix Commands: changing directories and listing files
-----------------------------------------------------

From there, you can use commands to move to other directories. The ``cd`` command stands for "change directory." You can use it to move to a directory that is directly accessible from where you are in the file system, by typing ``cd`` + the correct path to where you want to go in the command prompt.

Starting a path with ``/`` means you're starting at the very beginning. If you have a path such as ``/Users/kniznica/Desktop``, that is the *full path** to the Desktop folder. The symbol ``~`` refers to your home directory, which is the same as which is where your ``Desktop`` directory lives, among other things. So ``~/Desktop`` is another way to refer to the path to your desktop directory.

For example, if you have a folder in your ``Documents`` folder called ``SI_106``, and you start out in your home directory, you could type this at the command prompt: ``cd Documents/SI_106``. That means, 'change the directory I am at from here to the SI_106 folder, which is inside the Documents folder'. That string of text that comes after ``cd`` is the **path** to the directory you want to go to in your command prompt, relative to **where you are right now**. 

.. image:: Figures/cd_1.JPG

Doing ``cd Documents`` followed by ``cd SI_106`` is also fine. Each time, you are going to a *sub directory** of your current directory. In this example, ``SI_106`` is a sub directory of the ``Documents`` folder.

Now, if you are acting in this ``SI_106`` directory, and all it has in it is document files of notes you take in class and screenshot images, you cannot do ``cd Documents`` -- you can try, but it will not work. Once you are **in** ``SI 106``, ``cd Documents`` is the same as going from your home directory to ``cd Documents/SI_106/Documents``.

If you want to go back up one level in the file structure, there is a syntax especially for that: ``cd ..``. So if you are at ``~/Documents/SI_106`` and now you want to go back to the ``Documents`` directory in your command prompt, you would type ``cd ..`` at the prompt. If you wanted to go all the way back to your home directory, you would type ``cd ../..``. 

When you use the ``cd`` command, you're constructing paths to tell the computer where you want the command prompt to access in your system of files. 

Once you've reached a directory, there are a lot of powerful unix commands you can use. The next one we'll discuss is ``ls``, which is a command that lists all files that are in your current folder. (The directory, or folder, that you're **currently in** in the command prompt is often referred to as your **working directory**.) 

``ls`` is a way to list a directory's contents. For example, now that we have gone to a folder, ``ls`` will display a list like this:

.. image:: Figures/lsexample.JPG

This is useful for many reasons we'll get to later in the course, but also because it helps you see quickly, using the command prompt, what is saved in your current directory!


