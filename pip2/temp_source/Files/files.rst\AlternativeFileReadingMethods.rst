..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Alternative File Reading Methods
--------------------------------

In addition to the ``for`` loop, Python provides three other methods to read data
from the input file. You don't really need to use all of them, but in case you encounter them, here's what they do.
The ``readline`` method reads one line from the file and
returns it as a string. The string returned by ``readline`` will contain the
newline character at the end. This method returns the empty string when it
reaches the end of the file. The ``readlines`` method returns the contents of
the entire file as a list of strings, where each item in the list represents
one line of the file. It is also possible to read the entire file into a
single string with ``read``. :ref:`Table 2 <filemethods2a>` summarizes these methods
and the following session shows them in action.

.. _filemethods2a:

======================== =========================== =====================================
**Method Name**           **Use**                     **Explanation**
======================== =========================== =====================================
``write``                 ``filevar.write(astring)``  Add astring to the end of the file.
                                                      filevar must refer to a file that has
                                                      been  opened for writing.
``read(n)``               ``filevar.read()``          Reads and returns a string of ``n``
                                                      characters, or the entire file as a
                                                      single string if  n is not provided.
``readline(n)``           ``filevar.readline()``      Returns the next line of the file with
                                                      all text up to and including the
                                                      newline character. If n is provided as
                                                      a parameter than only n characters
                                                      will be returned if the line is longer
                                                      than ``n``.
``readlines(n)``          ``filevar.readlines()``     Returns a list of strings, each
                                                      representing a single line of the file.
                                                      If n is not provided then all lines of
                                                      the file are returned. If n is provided
                                                      then n characters are read but n is
                                                      rounded up so that an entire line is
                                                      returned.
======================== =========================== =====================================


In this course, we will generally either iterate through the contents of a file using a for loop, or use read() to get all of the contents as a single string.

In other programming languages, where they don't have the convenient for loop method of going through the lines of the file one by one, they use a different pattern which requires a different kind of loop, 
the ``while`` loop. Fortunately, you don't need to learn this other pattern, and we will put off consideration of ``while`` loops indefinitely in this course.

.. note::

   A common error that novice programmers make is not realizing that all these ways of reading the file, including
   using the for loop to iterate over the lines, **use up the file**. 
   If you want to go through the contents twice, for now it is probably easiest to just
   open it twice, and iterate through it twice. If you cared about efficiency, you might 
   prefer to save the contents in a variable.


