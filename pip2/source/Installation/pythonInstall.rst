..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, Dario Mitchell, Paul Resnick.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".



Install and configure Python
============================

Now, you'll need to install the Python interpreter on your computer. This process will again be a little bit different depending on whether you have a computer that runs a Mac or the Windows operating system. Follow the appropriate set of instructions:

* :ref:`Windows <windows_python_install>`
* :ref:`Mac <mac_python_install>`

.. _windows_python_install:

Install and configure python for Windows
----------------------------------------

Please download and install Python 2.7 from:

https://www.python.org/downloads/release/python-278/

Download and install the file Windows x86 MSI Installer (2.7.8) - when the install process asks you which directory to use - make sure to keep the default directory of C:\Python27\. If you are not sure if your Windows is 64-bit - install the 32-bit version of Python, the
one that just says, "Windows x86 MSI Installer (2.7.8)". If you know that you have 64-bit Windows, you can download the X86-64 MSI Installer.

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

You have one configuration to do, to tell Git Bash where in the file system to find the Python interpreter. Follow the steps below to do that.

#. Launch the program Git Bash in the usual way that you launch Windows programs. A shortcut for Git Bash was created during installation.

#. At the command prompt, paste this command ``export PATH="$PATH:/c/Python27"``. That will tell Windows where to find Python. (This assumes that you installed it in C:\\Python27, as we told you to above.)

#. Check to make sure that this worked correctly by entering the command ``python --version``.  It should say Python 2.7.8 (or 2.7.something), as shown in the figure below.

#. Assuming that worked correctly, you will want to set up git bash so that it always knows where to find python. To do that, enter the following command: ``echo 'export PATH="$PATH:/c/Python27"' > .bashrc``. That will save the command into a file called .bashrc. .bashrc is executed every time git bash launches, so you won't have to manually tell the shell where to find python again.

#. Check to make sure that worked by typing exit, relaunching git bash, and then typing ``python --version`` again.

.. image:: Figures/environment.JPG

.. _mac_python_install:

Install and configure python for Mac
------------------------------------

Because you have a mac, you're lucky in this case -- you already have Python. It comes pre-installed. However, we need to make sure you have the correct version of Python. We will be using version **2.7.**

If you have Mac OS 10.7 (Lion) or later, you definitely have Python 2.7. If you have Mac OS 10.6 (Snow Leopard) or earlier, you may have a different version of Python. If so, let's get this straightened out early -- come see one of the instructors. (If this applies to many people, we will provide additional instructions for that installation!)

To find out what version of Python you have, you'll first need to open your Terminal program.

Now you're going to use a command that will tell us what version of python you have installed on your mac.

Type: ``python -V``, and press return. That process should look something like this:

 .. image:: Figures/typedpython.png
        :width: 300px

 .. image:: Figures/returntypedpython.png
        :width: 300px

If you see a 2.7 (and the third number can be anything) on the screen, like in that image above, you're fine. If you get an error, please see one of the instructors!

You're now all ready to run Python.