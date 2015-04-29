..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

.. qnum::
   :prefix: data-8-
   :start: 1

Input
-----

.. video:: inputvid
    :controls:
    :thumb: ../_static/inputthumb.png

    http://media.interactivepython.org/thinkcsVideos/input.mov
    http://media.interactivepython.org/thinkcsVideos/input.webm


The program in the previous section works fine but is very limited in that it only works with one value for ``total_secs``.  What if we wanted to rewrite the program so that it was more general.  One thing we could
do is allow the user to enter any value they wish for the number of seconds.  The program could then print the
proper result for that starting value.

In order to do this, we need a way to get **input** from the user.  Luckily, in Python
there is a built-in function to accomplish this task.  As you might expect, it is called ``input``.

.. sourcecode:: python

    n = input("Please enter your name: ")

The input function allows the user to provide a **prompt string**.  When the function is evaluated, the prompt is
shown.
The user of the program can enter the name and press `return`. When this
happens the text that has been entered is returned from the `input` function,
and in this case assigned to the variable `n`.  Make sure you run this example a number
of times and try some different names in the input box that appears.

.. activecode:: inputfun

    n = input("Please enter your name: ")
    print("Hello", n)

It is very important to note that the ``input`` function returns a string value.  Even if you asked the user to enter their age, you would get back a string like
``"17"``.  It would be your job, as the programmer, to convert that string into
an int or a float, using the ``int`` or ``float`` converter functions we saw
earlier.

To modify our previous program, we will add an input statement to allow the user to enter the number of seconds.  Then
we will convert that string to an integer.  From there the process is the same as before.  To complete the example, we will
print some appropriate output.

.. activecode:: int_secs

    str_seconds = input("Please enter the number of seconds you wish to convert")
    total_secs = int(str_seconds)

    hours = total_secs // 3600
    secs_still_remaining = total_secs % 3600
    minutes =  secs_still_remaining // 60
    secs_finally_remaining = secs_still_remaining  % 60

    print("Hrs=", hours, "mins=", minutes, "secs=", secs_finally_remaining)


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

     n = input("Please enter your age: ")
     # user types in 18
     print ( type(n) )


.. index:: order of operations, rules of precedence

