..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Iterating over lines in a file
------------------------------


We will now use this file as input in a program that will do some data
processing. In the program, we will **read** each line of the file and
print it with some additional text. Because text files are sequences of
lines of text, we can use the *for* loop to iterate through each line of
the file.

A **line** of a file is defined to be a sequence of characters up to and
including a special character called the **newline** character. If you
evaluate a string that contains a newline character you will see the
character represented as ``\n``. If you print a string that contains a
newline you will not see the ``\n``, you will just see its effects. When
you are typing a Python program and you press the enter or return key on
your keyboard, the editor inserts a newline character into your text at
that point.

As the *for* loop iterates through each line of the file the loop
variable will contain the current line of the file as a string of
characters. The general pattern for processing each line of a text file
is as follows:

::

        for line in myFile:
            statement1
            statement2
            ...

To process all of our quarterback data, we will use a *for* loop to iterate over the lines of the file. Using
the ``split`` method, we can break each line into a list containing all the fields of interest about the
quarterback. We can then take the values corresponding to first name, lastname, and passer rating to
construct a simple sentence.


.. activecode:: files_for

    qbfile = open("qbdata.txt","r")

    for aline in qbfile:
        values = aline.split()
        print('QB ', values[0], values[1], 'had a rating of ', values[10] )

    qbfile.close()



