..  Copyright (C)  Paul Resnick.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".


When to use try/except
----------------------

The reason to use try/except is when you have a code block to execute that will sometimes run correctly and sometimes not, depending on conditions you can't foresee at the time you're writing the code.

For example, when you are running code that fetches data from a website, you may run the code when you don't have a network connection or when the external website is temporarily not responding. If your program can still do something useful in those situations, you would like to handle the exception and have the rest of your code execute.

As another example, for the problem sets we have been including some hidden code that runs tests to automatically inform you whether your programs are running correctly. We do that by running a function called testEqual, in the test module, that takes two inputs and checks whether they are equal. We call testEqual, passing the values of variables or the return values from function calls. If those variables and functions are defined but produce the wrong values, our code tells you that you have failed the test. On the other hand, if our test calls a function that you have not yet defined, it will cause a run-time error. When there is a danger of that, we have wrapped our call to test.testEqual in a try/except. Starting with this problem set, where you get all of the code in a file, you can see these try/except clauses. For example, in ps7, we have the following:

.. sourcecode:: python

   fall_list = ["leaves","apples","autumn","bicycles","pumpkin","squash","excellent"]
   
   # Write code to sort the list fall_list in reverse alphabetical order. 
   # Assign the sorted list to the variable sorted_fall_list.
   
   # Now write code to sort the list fall_list by length of the word, longest to shortest.
   # Assign this sorted list to the variable length_fall_list.
   
   try:
       test.testEqual(sorted_fall_list[0], 'squash', "squash first")
       test.testEqual(length_fall_list[0], 'excellent', "excellent first")
   except:
       print "sorted_fall_list or length_fall_list don't exist or have no items"
   

When you first run this, sorted_fall_list is not bound, so you get an error that is handled by the exception clause. If you add ``sorted_fall_list = [1, 2, 3]``, it will tell you that the first test doesn't pass, because the list has the wrong first element.

.. note::

   The testEqual function that we have provided you for download is slightly different than the one that's built into ActiveCode test module. It takes an extra parameter (e.g., "squash first") that is just a comment string. This code may not work properly in an ActiveCode window.  



