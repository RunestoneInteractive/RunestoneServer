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


In addition to the ``for`` loop, Python provides three methods to read data
from the input file. The ``readline`` method reads one line from the file and
returns it as a string. The string returned by ``readline`` will contain the
newline character at the end. This method returns the empty string when it
reaches the end of the file. The ``readlines`` method returns the contents of
the entire file as a list of strings, where each item in the list represents
one line of the file. It is also possible to read the entire file into a
single string with ``read``. :ref:`Table 2 <filemethods2a>` summarizes these methods
and the following session shows them in action.

Note that we need to reopen the file before each read so that we start from
the beginning. Each file has a marker that denotes the current read position
in the file. Any time one of the read methods is called the marker is moved to
the character immediately following the last character returned. In the case
of ``readline`` this moves the marker to the first character of the next line
in the file. In the case of ``read`` or ``readlines`` the marker is moved to
the end of the file.


::

    >>> infile = open("qbdata.txt","r")
    >>> aline = infile.readline()
    >>> aline
    'Colt McCoy QB, CLE\t135\t222\t1576\t6\t9\t60.8%\t74.5\n'
    >>>
    >>> infile = open("qbdata.txt","r")
    >>> linelist = infile.readlines()
    >>> print(len(linelist))
    34
    >>> print(linelist[0:4])
    ['Colt McCoy QB CLE\t135\t222\t1576\t6\t9\t60.8%\t74.5\n',
     'Josh Freeman QB TB\t291\t474\t3451\t25\t6\t61.4%\t95.9\n',
     'Michael Vick QB PHI\t233\t372\t3018\t21\t6\t62.6%\t100.2\n',
     'Matt Schaub QB HOU\t365\t574\t4370\t24\t12\t63.6%\t92.0\n']
    >>>
    >>> infile = open("qbdata.txt","r")
    >>> filestring = infile.read()
    >>> print(len(filestring))
    1708
    >>> print(filestring[:256])
    Colt McCoy QB CLE	135	222	1576	6	9	60.8%	74.5
    Josh Freeman QB TB	291	474	3451	25	6	61.4%	95.9
    Michael Vick QB PHI	233	372	3018	21	6	62.6%	100.2
    Matt Schaub QB HOU	365	574	4370	24	12	63.6%	92.0
    Philip Rivers QB SD	357	541	4710	30	13	66.0%	101.8
    Matt Ha
    >>>

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

Now lets look at another method of reading our file using a ``while`` loop.  This is important because many other programming languages do not support the ``for`` loop style for reading file but they do support the pattern we'll show you here.

.. activecode:: files_while

    infile = open("qbdata.txt","r")
    line = infile.readline()
    while line:
        values = line.split()
        print('QB ', values[0], values[1], 'had a rating of ', values[10] )
        line = infile.readline()

    infile.close()

The important thing to notice is that on line 2 we have the statement ``line = infile.readline()``.  
We call this initial read the **priming read**.
It is very important because the while condition needs to have a value for the ``line`` variable.  The ``readline`` method will return the
empty string if there is no more data in the file.  The condition ``while line:`` means `while the content of line is not the empty string`.  Remember that a
blank line in the file actually has a single character, the ``\n`` character (newline).  So, the only way that a line of data from the
file can be empty is if you are reading at the end of the file.

Finally, notice that the last line of the body of the ``while`` loop performs another ``readline``.  This statement will reassign the variable ``line`` to the next line of the file.  It represents the `change of state` that is necessary for the iteration to
function correctly.  Without it, there would be an infinite loop processing the same line of data over and over.

