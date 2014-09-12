..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Exercises
---------



#. 


    .. tabbed:: q1

        .. tab:: Question

            The following sample file called ``studentdata.txt`` contains one line for each student in an imaginary class.  The 
            students name is the first thing on each line, followed by some exam scores.  
            The number of scores might be different for each student.

            .. raw:: html

                <pre id="studentdata.txt">
                joe 10 15 20 30 40
                bill 23 16 19 22
                sue 8 22 17 14 32 17 24 21 2 9 11 17
                grace 12 28 21 45 26 10
                john 14 32 25 16 89
                </pre>

            Using the text file ``studentdata.txt`` write a program that prints out the names of
            students that have more than six quiz scores. 



            .. actex:: ex_files_1
               
               # Hint: first see if you can write a program that just prints out the number of scores on each line
               
               # Then, make it print the number only if the number is at least six
               
               # Then, switch it to printing the name instead of the number
