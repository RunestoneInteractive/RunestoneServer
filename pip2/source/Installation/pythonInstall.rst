..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, Dario Mitchell, Paul Resnick.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Now, you'll need to install the Python interpreter on your computer. This process will again be a little bit different depending on whether you have a computer that runs a Mac or the Windows operating system. Follow the appropriate set of instructions:

.. _windows_python_install:

Install and configure python
----------------------------

Please download and install Python 2.7 from:

http://python.org/download/releases/2.7.6/

Download and install the file python-2.7.6.msi - when the install process asks you which directory to use - make sure to keep the default directory of C:\Python27\. If you are not sure if your Windows is 64-bit - install the 32-bit version of Python, the
one that just says, "Windows x86 MSI Installer (2.7.6) (sig)".

.. note::

   Make sure that you install the latest version of Python 2.x - do not install Python 3.x. 
   There are signficant differences between Python 2 and Python 3 and this book/site is based on Python 2.

With just this installation, you can get an interactive python interpreter where
you can type code one line at a time and have it executed. You may find some options
on the Windows menu for this, such as Idle. We *do not* recommend using these.

With just this installation it is also possible to run python from the Windows command prompt. 
But the Windows command prompt is tricky to deal with. To establish
greater consistency with the environment in which Mac users will be working and 
because it's just a better command prompt, we will invoke Python using Git Bash.


.. _mac_python_install:

Install and configure python for Mac
====================================

Because you have a mac, you're lucky in this case (though you can develop fine on any operating system!) -- you already have Python. It comes pre-installed. However, we need to make sure you have the correct version of Python. We will be using version **2.7.**

If you have Mac OS 10.7 (Lion) or later, you definitely have Python 2.7. If you have Mac OS 10.6 (Snow Leopard) or earlier, you may have a different version of Python. If so, let's get this straightened out early -- come see one of the instructors. (If this applies to many people, we will provide additional instructions for that installation!)

To find out what version of Python you have, you'll first need to open a program on your mac called the **Terminal**. You can find it via Spotlight, or in your Applications folder. The icon looks like this:

.. image:: Figures/terminalicon.png

When you open it, you'll see a window that should look something like this:

.. image:: Figures/emptyterminal.png

Except the name of *your* computer will be there. (That'll be whatever you called your hard drive -- probably your name, if you've chosen to keep the default!)

Terminal is the way you use your **command line**. That blinking cursor when you first open the window -- when you type there, we might say you're typing at the command prompt. Before we talk about how you use this, you're going to use a command that will tell us what version of python you have installed on your mac.

Type: ``python -V``, and press return. That process should look something like this:

.. image:: Figures/typedpython.png
        :width: 300px

.. image:: Figures/returntypedpython.png
        :width: 300px

If you see a 2.7 (and the third number can be anything) on the screen, like in that image above, you're fine. If you get an error, please see one of the instructors!

You're now all ready to run Python.