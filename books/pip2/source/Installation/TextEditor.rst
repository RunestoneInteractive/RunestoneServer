..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, Dario Mitchell, Paul Resnick.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".


.. _text_editor_installation:


Installing a Text Editor
========================

You will need a text editor. There are many options for this. For example, serious
programmers often use Eclipse or XCode, which are environments that include some useful tools, or Vim or Emacs, which are text editors that you can use inside the command prompt, which require learning a lot of keyboard commands. We do not recommend those for beginners programming -- better to focus on the problem-solving itself, and there's a lot of stuff to configure in those that you don't need right now. (Many serious programmers don't use those either!) 

Definitely **do not** use MS Word. Word will not save files in the right format, so you will not be able to run programs, and it doesn't do any syntax highlighting or other useful things. Default programs that come with your operating system like TextEdit for Mac or plain Notepad for Windows are also not a good idea -- this can lead to file formatting issues, and you won't have syntax highlighting and other useful features. 


.. _windows_install:

Windows Instructions
====================

The editor that we will help you to use is called **NotePad++**. Please download it from
`this site <http://notepad-plus-plus.org/download/>`_. Download it and then run the installer to install NotePad++, like you would most programs you download.

.. note::

   Important! Before you create your first program, you need to make one small change in the Preferences for NotePad++. This will save you lots of "Python indent errors" anguish later. 
   Under *Settings -> Preferences -> Language Menu/Tab Settings*, tick the check box for "Expand Tabs", leaving the value at "4", and 
   press the "Close" button.
   
   .. image:: Figures/tabs.JPG


Follow the instructions below. It should be 
quite intuitive. The one thing to keep in mind is that NotePad++ is an environment
for *creating* python programs. It doesn't run them!  You'll have to install a little
more stuff to run your programs, as described in later sections.
(If you'd like to see a demonstration of NotePad++, Dr. Chuck has a screen cast for the use of NotePad++. 
You can either view this `on YouTube <http://www.youtube.com/watch?v=o0X-VHX6ls0>`_ or you can download the high-quality `QuickTime version <http://www-personal.umich.edu/~csev/courses/shared/podcasts/windows-python-notepad-plus.mov>`_ 
of the screen cast. You will need Apple QuickTime installed to view this video. )

Start NotePad++ from either a Desktop icon or from the Start Programs menu and enter your first Python program into NotePad++:

   .. image:: Figures/helloworld.JPG
      :width: 300px
    
Save your program as ``firstprog.py``. You can save it anywhere. In a little while we'll
create a code folder in a convenient place on your machine and you can resave the file then. 
You will notice that after you save the file, NotePad++ will color your code based on the Python syntax rules. 
Syntax coloring is a very helpful feature as it gives you visual feedback about your program and can help you track down syntax errors more easily. 
NotePad++ only knows that your file is a Python file after you save it with a ``.py`` suffix, also known as file extension. It's like the ``.txt`` file extension we've seen that means a file is a plain text file, except this ``.py`` extension means that this file is a Python program.

   .. image:: Figures/firstprog.JPG
      :width: 300px


.. _mac_install:

Mac Instructions
================

The editor that we will help you to use is called **TextWrangler**. (TextWrangler and Notepad++ are very similar, but one runs on Macs and one runs on Windows.) Please download it from
`the TextWrangler site <http://www.barebones.com/products/TextWrangler/download.html>`_. Download it and then run the installer to install TextWrangler, like you would most programs you download.

TextWrangler may ask you to register for something, or to install other programs. You can hit Cancel -- you do not need to register for anything to use TextWrangler, you do not need any other programs, and it will not expire.

Follow the instructions that follow. It should be 
quite intuitive. Keep in mind the concepts from earlier -- TextWrangler is an environment (a piece of software)
for _creating_ python programs. It's not intended (in this course) for running them!

Start TextWrangler from a Dock shortcut icon, finding it in your Applications folder, or startinit from Spotlight. Enter your first Python program into TextWrangler:

   .. image:: Figures/helloworldmac.png
      :width: 300px
    
Save your program as ``firstprog.py``, in your 106 folder. You will notice that after you save the file, TextWrangler will color your code based on the Python syntax rules. That's because you saved it with the ``.py`` file extension, which tells the computer this file is a Python program.

Syntax coloring is a very helpful feature, as it gives you visual feedback about your program and can help you track down syntax errors more easily. 
TextWrangler only knows that your file is a Python file after you save it with a ``.py`` suffix, also known as file extension. It's like the ``.txt`` file extension we've seen that means a file is a plain text file, except this ``.py`` extension means that this file is a Python program.

   .. image:: Figures/firstprogram_tw.png
      :width: 300px

