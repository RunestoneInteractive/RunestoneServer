..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Input
-----

Our programs get more interesting if they don't do exactly the same thing every time they run. One way to make them more interesting is to get **input** from the user.  Luckily, in Python
there is a built-in function to accomplish this task.  It is called ``raw_input``.

.. note::
   There is another function for input, called simply ``input``, but ``raw_input`` is preferable
   for reasons that we won't go into here.

.. sourcecode:: python

    n = raw_input("Please enter your name: ")

The raw_input function allows the user to provide a **prompt string**.  When the function is evaluated, the prompt is
shown (in the browser, look for a popup window).
The user of the program can enter the name and press `return`. When this
happens the text that has been entered is returned from the `input` function,
and in this case assigned to the variable `n`.  Run this example a few times and try some different names in the input box that appears.

.. activecode:: inputfun

    n = raw_input("Please enter your name: ")
    print "Hello", n

It is very important to note that the ``raw_input`` function returns a string value.  Even if you asked the user to enter their age, you would get back a string like
``"17"``.  It would be your job, as the programmer, to convert that string into
an int or a float, using the ``int`` or ``float`` converter functions we saw
earlier.

Here's is a program that turns a number of seconds into more human readable counts of hours, minutes, and seconds. An call to raw_input allows the user to enter the number of seconds.  Then we  convert that string to an integer.  From there we use the division and modulus operators to compute teh results.

.. activecode:: int_secs

    str_seconds = raw_input("Please enter the number of seconds you wish to convert")
    total_secs = int(str_seconds)

    hours = total_secs // 3600
    secs_still_remaining = total_secs % 3600
    minutes =  secs_still_remaining // 60
    secs_finally_remaining = secs_still_remaining  % 60

    print "Hrs=", hours, "mins=", minutes, "secs=", secs_finally_remaining


The variable ``str_seconds`` will refer to the string that is entered by the user. As we said above, even though this string may be ``7684``, it is still a string and not a number.  To convert it to an integer, we use the ``int`` function.
The result is referred to by ``total_secs``.  Now, each time you run the program, you can enter a new value for the number of seconds to be converted.

**Check your understanding**

.. mchoicemf:: test_question2_7_1
   :answer_a: &lt;class 'str'&gt;
   :answer_b: &lt;class 'int'&gt;
   :answer_c: &lt;class 18&gt;
   :answer_d: 18
   :correct: a
   :feedback_a: All input from users is read in as a string.
   :feedback_b: Even though the user typed in an integer, it does not come into the program as an integer.
   :feedback_c: 18 is the value of what the user typed, not the type of the data.
   :feedback_d: 18 is the value of what the user typed, not the type of the data.

   What is printed when the following statements execute?

   .. code-block:: python

     n = raw_input("Please enter your age: ")
     # user types in 18
     print  type(n)


.. index:: order of operations, rules of precedence

