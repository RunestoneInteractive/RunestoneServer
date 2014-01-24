..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Simple Tables
-------------

One of the things loops are good for is generating tabular data.  Before
computers were readily available, people had to calculate logarithms, sines and
cosines, and other mathematical functions by hand. To make that easier,
mathematics books contained long tables listing the values of these functions.
Creating the tables was slow and boring, and they tended to be full of errors.

When computers appeared on the scene, one of the initial reactions was, *"This is
great! We can use the computers to generate the tables, so there will be no
errors."* That turned out to be true (mostly) but shortsighted. Soon thereafter,
computers and calculators were so pervasive that the tables became obsolete.

Well, almost. For some operations, computers use tables of values to get an
approximate answer and then perform computations to improve the approximation.
In some cases, there have been errors in the underlying tables, most famously
in the table the Intel Pentium processor chip used to perform floating-point division.

Although a power of 2 table is not as useful as it once was, it still makes a good
example of iteration. The following program outputs a sequence of values in the
left column and 2 raised to the power of that value in the right column:

.. activecode:: ch07_table1

    print("n",'\t',"2**n")     #table column headings
    print("---",'\t',"-----")

    for x in range(13):        # generate values for columns
        print(x, '\t', 2**x)

The string ``'\t'`` represents a **tab character**. The backslash character in
``'\t'`` indicates the beginning of an **escape sequence**.  Escape sequences
are used to represent invisible characters like tabs and newlines. The sequence
``\n`` represents a **newline**.

An escape sequence can appear anywhere in a string.  In this example, the tab
escape sequence is the only thing in the string. How do you think you represent
a backslash in a string?

As characters and strings are displayed on the screen, an invisible marker
called the **cursor** keeps track of where the next character will go. After a
``print`` function is executed, the cursor normally goes to the beginning of the next
line.

The tab character shifts the cursor to the right until it reaches one of the
tab stops. Tabs are useful for making columns of text line up, as in the output
of the previous program.
Because of the tab characters between the columns, the position of the second
column does not depend on the number of digits in the first column.




.. index::
    single: local variable
    single: variable; local

**Check your understanding**

.. mchoicemf:: test_question7_7_1
  :answer_a: A tab will line up items in a second column, regardless of how many characters were in the first column, while spaces will not.
  :answer_b: There is no difference
  :answer_c: A tab is wider than a sequence of spaces
  :answer_d: You must use tabs for creating tables.  You cannot use spaces.
  :correct: a
  :feedback_a: Assuming the size of the first column is less than the size of the tab width.
  :feedback_b: Tabs and spaces will sometimes make output appear visually different.
  :feedback_c: A tab has a pre-defined width that is equal to a given number of spaces.
  :feedback_d: You may use spaces to create tables.  The columns might look jagged, or they might not, depending on the width of the items in each column.

  What is the difference between a tab (\t) and a sequence of spaces?

