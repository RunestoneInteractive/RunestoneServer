..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".


Understanding Code
==================

Whether you’re trying to understand a code snippet that someone else wrote or trying to understand your own code that isn’t doing exactly what you wanted, you can avoid a lot of frustration if you slow down and spend the time to fully understand that code. It will reduce your anxiety level as well and make programming more fun!

The basic strategy for understanding code is the "explain; predict; check" loop.

Explain (Make a reference diagram)
----------------------------------

To understand what a snippet of code (one or more lines) does, you should first form a hypothesis about the *state* of the program just before your snippet executes.

It’s a good idea to make a reference diagram by hand, the kind of diagram that CodeLens produces for you. In particular, for each of the variable names that are referred to in the code snippet you are trying to understand, you should make a prediction about:

* the type of that variable’s value (integer, string, list, dictionary, etc.)   
* the value of that variable

You should also be able to state, in English, what each of the operations in your code snippet does. For example, if your code snippet includes a line ``x.append(4)``, then you should be able to say, “The append operation takes a list, x in this case, and appends an item, 4 in this case, to the end of the list. It changes the actual list, so any other variable that is an alias for the list will also have its value changed.”

Predict
-------

In the predict phase, you will predict the effect of running a snippet of code. Later on in your development, you may make predictions about large snippets of code, but for now you will typically be predicting the effect of executing a single line of code, or at most the net effect of running an entire ``for`` loop. A prediction will either be about what gets printed out, or about the value of a variable, or that an error will occur.

A prediction is not a random guess. It is based on some explanation you have about what the current state of variables is and about what you think certain commands in python do.

Check
-----

To check your understanding or your predictions, you will run a program. 

To check your understanding about the state of variables before your code snippet runs, add diagnostic print statements that print out the types and values of variables. Add these print statements just *before* the code snippet you are trying to understand.

If you made a prediction about the output that will be generated when the code snippet runs, then you can just run the program. If, however, you made a prediction about a change that occurs in the value of a variable, you will need to add an extra diagnostic print statement right after the line of code that you think should be changing that variable. 

The diagnostic print statements are temporary.  Once you have verified that a program is doing what you think it’s doing, you will remove these extra print statements.

If you get any surprises, then you will want to revise your understanding or your predictions. If you were wrong about the values or types of variables before the code snippet was run, you may to revisit your understanding of the previous code. 

If you were wrong about the effect of an operation, you may need to revisit your understanding of that operation. One good way to do that is to run that operation on some very simple values. For example, if you thought ``x.append([4, 5])`` appended x as the second element of the list that already contains 4 and 5, you might want to try it on even simpler values, like ``x.append(4)`` in order to realize that the item in parentheses in the one being appended, not the list one being appended to.

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
