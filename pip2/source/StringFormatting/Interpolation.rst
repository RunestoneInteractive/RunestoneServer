..  Copyright (C)  Paul Resnick, Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

String Interpolation
====================

Until now, we have created strings with variable content using the + operator to concatenate partial strings together. That works, but it's very hard for people to read or debug a code line that includes variable names and strings and complex expressions. Consider the following: 

.. activecode:: interpolation_1

   name = "Rodney Dangerfield"
   score = -1  # No respect!
   print "Hello " + name + ". Your score is " + str(score)

Or perhaps more realistically:
 
.. activecode:: interpolation_2
 
   scores = [("Rodney Dangerfield", -1), ("Marlon Brando", 1), ("You", 100)]
   for (name, score) in scores:
      print "Hello " + name + ". Your score is " + str(score)

In this section, you will learn to write that in a more readable way:

.. activecode:: interpolation_3
 
   scores = [("Rodney Dangerfield", -1), ("Marlon Brando", 1), ("You", 100)]
   for (name, score) in scores:
      print "Hello %s. Your score is % d" % (name, score)
      
   # or some might find this even more readable
   for (name, score) in scores:
      print "Hello %(nm)s. Your score is %(sc) d" % {"nm":name, "sc":score}

``%`` is the interpolation operator. It takes a format string on the left, and a tuple of values on the right. Together, the whole expression produces a single string. 

You now know enough python that you can start to learn directly from the python documentation. The python documentation on string interpolation is readable, with some effort, and a few explanations below. `String interpolation documentation <http://docs.python.org/2/library/stdtypes.html#string-formatting-operations>`_   

* **Unicode** is a special kind of character string that allows the use of non-English characters

* What the documentation refers to as ``format`` is a string with some % signs embedded in it. These will be substituted for in the final string. When the documentation says "If *format* requires a single argument, it means there's just one % within the format string, indicating one element to be substituted for.

* The minimum field width and precision are useful for formatting numbers.

* The length modifier is not used, so don't worry about it.

Let's use the vocabulary of the documentation to parse the line of code ``"Hello %s. Your score is % 2d" % (name, score)``:

* The ``format string`` is "Hello %s. Your score is % d".

   * The first conversion specifier is ``%s``, which calls for a string value to be substituted.
   
   * The second conversion specifier is ``% d``, which calls for an integer. The space before the d is a flag, indicating that if the number is positive, it should generate a string without a + sign in it.
   
* The values are specified in the tuple ``(name, score)``. Note that neither name nor score are in quotes, so both are variables whose values are looked up. 

.. note::

   The ``%`` operator produces a string. It does not print anything, and it does not return anything. If you want a person to see the string, print it. If you want to save it for later, assign it to a variable or put it in a list. If you want a function to return the string, make an explicit return statement.

Try to predict what each of these lines will produce as you step through the code.

.. codelens:: interpolation_4

   x = 3.75
   print x
   print "You have $%0.2f in your pocket" % (x)
   print "You have $%f in your pocket" % (x)
   print "You have $%10.1f in your pocket" % (x)
   print "You have $%0.0f in your pocket" % (x)
   print "You have $%d in your pocket" % (x)
   print "You have $%02d in your pocket" % (x)
   print "You have $%0.2f. If you spend $1.25, you will have $%0.2f left" % (x, x-1.25)


