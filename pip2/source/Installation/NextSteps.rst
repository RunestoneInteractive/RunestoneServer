..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, Dario Mitchell, Paul Resnick.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

.. _next_steps:

Preparing for the Rest of the Course
====================================

It has been convenient to be able to execute python code right in the browser. To write and
execute bigger programs, to use modules beyond the few (like the ``random`` module) that have been implemented for this environment, and to perform file and network operations, you will need to run Python *natively* on your computer.

First, we'll provide an overview of how writing and running programs on your own computer works. Then we'll provide instructions for installing what you need and getting the new setup going.

There are different instructions for Windows users and Mac users below. (If you use Linux, there are no instructions for you -- we assume in that case you know what you are doing here, but if you are confused, let us know.)

None of the steps that follow is particularly difficult, but there are a lot of them, and if you inadvertently skip one, you may not have a good time. We recommend that you print out this chapter and use a pen to check off the steps as you do them, or do the equivalent on screen with a PDF file.

Important Concepts
==================

Up till now, we have written code in the active code windows and clicked "Run" to run it. You saw results in the console, below the active code windows-- remember, ``print`` is for people.

When you write code and run it *on your own computer*, what happens is basically this:

You'll write a program and save it as a file. You need a text editor to do this (more about this below! Note that MS Word is *not* a text editor). 

.. note::

   All programs you will write from here on will be stored in files (or groups of files, but we'll get to that) that are saved in a certain way, with the extension **.py**, so the computer knows these are *Python programs*. 

You will have an interpreter for Python programs installed on your computer. Read on to find out how to do that. Naturally enough, that interpreter will be called ``python``.

You'll use the command prompt, which you've already been learning about, to essentially say "hey, python, find this file that has my Python program, and interpret and then run it."  The analog of clicking on the "Run" button in our online environment will be to type ``python <your_code_file_name.py>`` at a command prompt. For example:

.. image:: Figures/secondprog1.JPG

You'll always have to know exactly where you saved your code file on your computer. Similar to how every single character matters when you write Python code, you have to tell the computer exactly where the program file you want to run is. 

In summary, the biggest differences from the online environment you've been using will be that you'll switch back and forth between two windows (one for editing the code, another for running it), you will name all the code files you save, and it's very important how and where you save your files. This is where your file system and Unix knowledge from the past few weeks will help!

Preparing Your Computer for the Rest of the Course
==================================================

We will walk you through the process of setting up your computer to run Python natively. It will involve the following steps:

1. Install and configure a text editor

#. Install and configure Python

Then, you'll save your files in the folder/file structure we've been working with for the Unix Problems, so you have one folder where all of your code lives. **Make sure** to save all your code in this same place, where you can find it and know exactly where it all is -- not doing so will create a headache for you!

The instructions diverge a bit, depending on whether you are on Windows or a Mac. (If you're on
Linux, we presume that you know what you're doing already and can make appropriate
improvisations from the instructions for Windows or Mac, but feel free to ask.)