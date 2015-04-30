..  Copyright (C)  Paul Resnick.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

.. _pip_chap:

Installing Modules
==================

Eventually, you will want to install additional python modules (sometimes called libraries) that are not pre-packaged with your python installation. 

.. figure:: Figures/xkcdmodule.png

   There are lots of great modules out there. In fact, there so many that you'll feel like you're flying.
   

Installing pip
--------------

pip is python's package installer. Once you've installed it, installing most other modules will be easy. Installing pip itself may be a little tricky.

The official instructions are at `<http://pip.readthedocs.org/en/latest/installing.html>`_. Here are a few pointers that may help you.

* When the instructions say to securely download the file get-pip.py, the easiest way to do that is probably to right-click on the link and "save as".

* Make sure that you have saved get-pip.py in the same directory you are in when you run the ``python get-pip.py`` command.

* When it says that running ``python get-pip.py`` may require administrator access, they mean that you might get an authorization error when it tries to write some of the new files to your computer's file system. If so, you may be able to solve that problem by running the command as a super-user: ``sudo python get-pip.py``


Using pip to install other modules
----------------------------------

Most other modules that you might want to use can be installed using pip.

For example, we will be using the requests module. That can be installed by typing ``pip install requests``. There are a couple of potential gotchas.

* If you get an authorization error when it tries to write some files, that means you need to run the command with sudo: ``sudo install requests``

* Especially on Windows machines, your installation may not be set up to automatically look in the Scripts folder for pip. In that case, you will need to give it a full path to the pip command. If your installation is that same as mine, meaning that python was installed in c:\Python27, at the bash shell you would give a command like ``/c/Python27/Scripts/pip install requests``.
