..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Example
-------

The following code illustrates what your program might look like after you complete the process above of adding comments that document your understanding and diagnostic print statements that allow you to check your understanding. This is what your code might look like prior to the cleanup phase.

In this program we are adding all the even numbers in a list together, accumulating a sum. You will see a diagnostic print statement inside the code block of the for loop, and one inside the if statement. All of these make it easier to check whether it’s doing what it’s supposed to do.
    
.. activecode:: db2_ex_1

    numbers = [1,2,6,4,5,6, 93]

    z = 0
    for num in numbers:
      print("*** LOOP ***")
      print("Num =",num)
      if (num % 2) == 0:
        print("Is even. Adding",num,"to",z)
        z = num + z
      print ("Running sum =",z)
    print("*** DONE ***")
    print ("Total = " , z)
