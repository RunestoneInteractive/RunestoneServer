..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Run a Code File
---------------

Finally, you are ready to run a python program! At the terminal window, type ``python secondprog.py``. This will invoke the python interpreter, executing the code in file secondprog.py. That file just contains the line ``print "hello world"``, so *hello world* is output to the console. Notice that the console is just the area in the terminal window underneath where you entered the command that invoked python.

.. image:: Figures/secondprog1.JPG

.. note::

   If in a terminal window you type ``python`` without specifying a filename, it launches the **python interpreter** and gives a little different command prompt. It's then waiting for you type python commands one at a time, which it immediately evaluates. In my experience, using the python interpreter is very confusing for beginning students, because it mixes up the idea of printed representations being generated only by explicit print statements (print is for people!). If you accidentally launch the python interpreter, I encourage you to just kill it, by typing ``exit()``.
   
   .. image:: Figures/pythoninterpreter.JPG

