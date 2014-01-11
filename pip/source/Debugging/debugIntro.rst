..  Copyright (C)  Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".
..  Edits by Paul Resnick

How to be a Successful Programmer
=================================

One of the most important skills you need to aquire to complete this book successfully is the ability to debug your programs.  Debugging might be the most under-appreciated, and under-taught, skill in introductory computer science.  For that reason we are introducing a series of "debugging interludes."  Debugging is a skill that you need to master over time, and some of the tips and tricks are specific to different aspects of Python programming.  So look for additional debugging interludes throughout the rest of this book.

Programming is an odd thing in a way.  Here is why.  As programmers we spend 99% of our time trying to get our program to work.  We struggle, we stress, we spend hours deep in frustration trying to get our program

How to Avoid Debugging
----------------------

Perhaps the most important lesson in debugging is that it is **largely avoidable** -- if you work carefully.

1.  **Start Small**  This is probably the single biggest piece of advice for programmers at every level.  Of course its tempting to sit down and crank out an entire program at once.  But, when the program -- inevitably -- does not work then you have a myriad of options for things that might be wrong.  Where to start?  Where to look first?  How to figure out what went wrong?  I'll get to that in the next section.  So, start with something really small.  Maybe just two lines and then make sure that runs ok.  Hitting the run button is quick and easy, and gives you immediate feedback about whether what you have just done is ok or not.  Another immediate benefit of having something small working is that you have something to turn in.  Turning in a small, incomplete program, is almost always better than nothing.


3.  **Keep it working**  Once you have a small part of your program working the next step is to figure out something small to add to it.  If you keep adding small pieces of the program one at a time, it is much easier to figure out what went wrong, as it is most likely that the problem is going to be in the new code you have just added.  Less new code means its easier to figure out where the problem is.

This notion of **Get something working and keep it working** is a mantra that you can repeat throughout your career as a programmer.  Its a great way to avoid the frustrations mentioned above.  Think of it this way.  Every time you have a little success, your brain releases a tiny bit of chemical that makes you happy.  So, you can keep yourself happy and make programming more enjoyable by creating lots of small victories for yourself.


Ok, lets look at an example.  Lets solve the problem posed in question 3 at the end of the Simple Python Data chapter.  Ask the user for the time now (in hours 0 -- 23), and ask for the number of hours to wait. Your program should output what the time will be on the clock when the alarm goes off.

So, where to start?  The problem requires two pieces of input from the user, so lets start there and make sure we can get the data we need.

.. activecode:: db_ex3_1

   current_time = input("what is the current time (in hours)?")
   wait_time = input("How many hours do you want to wait")

   print(current_time)
   print(wait_time)


If you haven't yet, click Run: get in the habit of checking whether small things are working before you go on. 

So far so good.  Now lets take the next step.  We need to figure out what the time will be after waiting ``wait_time`` number of hours.  A good first approximation to that is to simply add ``wait_time`` to ``current_time`` and print out the result.  So lets try that.

.. activecode:: db_ex3_2

   current_time = input("what is the current time (in hours 0--23)?")
   wait_time = input("How many hours do you want to wait")

   print(current_time)
   print(wait_time)

   final_time = current_time + wait_time
   print(final_time)

Hmm, when you run that example you see that something funny has happened.

.. mchoicemf:: db_q_ex3_1
   :answer_a: Python is stupid and does not know how to add properly.
   :answer_b: There is nothing wrong here.
   :answer_c: Python is doing string concatenation, not integer addition.
   :correct: c
   :feedback_a: No, Python is probabaly not broken.
   :feedback_b: No, try adding the two numbers together yourself, you will definitely get a different result.
   :feedback_c: Yes!  Remember that input returns a string.  Now we will need to convert the string to an integer

   Which of the following best describes what is wrong with the  previous example?

This error was probably pretty simple to spot, because we printed out the value of ``final_time`` and it is easy to see that the numbers were just concatenated together rather than added.  So what do we do about the problem?  We will need to convert both ``current_time`` and ``wait_time`` to ``int``.  At this stage of your programming development, it can be a good idea to include the type of the variable in the variable name itself.  So lets look at another iteration of the program that does that, and the conversion to integer.


.. activecode:: db_ex3_3

   current_time_str = input("what is the current time (in hours 0-23)?")
   wait_time_str = input("How many hours do you want to wait")

   current_time_int = int(current_time_str)
   wait_time_int = int(wait_time_str)

   final_time_int = current_time_int + wait_time_int
   print(final_time_int)


.. index:: boundary conditions, testing, debugging

Now, thats a lot better, and in fact depending on the hours you chose, it may be exactly right.  If you entered 8 for the current time and 5 for the wait time then 13 is correct.  But if you entered 17 (5pm) for the hours and 9 for the wait time then the result of 26 is not correct.  This illustrates an important aspect of **testing**, which is that it is important to test your code on a range of inputs.  It is especially important to test your code on **boundary conditions**.  In this case you would want to test your program for hours including 0, 23, and some in between.  You would want to test your wait times for 0, and some really large numbers.  What about negative numbers?  Negative numbers don't make sense, but since we don't really have the tools to deal with telling the user when something is wrong we will not worry about that just yet.  

So finally we need to account for those numbers that are bigger than 23.  For this we will need one final step, using the modulo operator.

.. activecode:: db_ex3_4

   current_time_str = input("what is the current time (in hours 0-23)?")
   wait_time_str = input("How many hours do you want to wait")

   current_time_int = int(current_time_str)
   wait_time_int = int(wait_time_str)

   final_time_int = current_time_int + wait_time_int
   
   final_answer = final_time_int % 24

   print("The time after waiting is: ", final_answer)

Of course even in this simple progression, there are other ways you could have gone astray.  We'll look at some of those and how you track them down in the next section.

Beginning tips for Debugging
----------------------------

Debugging a program is a different way of thinking than writing a program.  The process of debugging is much more like being a detective.  Here are a few rules to get you thinking about debugging.

#. Everyone is a suspect (Except Python)!  Its common for beginner programmers to blame Python, but that should be your last resort.  Remember that Python has been used to solve CS1 level problems millions of times by millions of other programmers.  So, Python is probably not the problem.

#. Find clues.  This is the biggest job of the detective and right now there are two important kinds of clues for you to understand.

    #. Error Messages

    #. Print Statements

Know your error Messages
~~~~~~~~~~~~~~~~~~~~~~~~

Many problems in your program will lead to an error message.  For example as I was writing and testing this chapter of the book I wrote the following version of the example program in the previous section.

.. sourcecode:: python

   current_time_str = input("what is the current time (in hours 0-23)?")
   wait_time_str = input("How many hours do you want to wait")

   current_time_int = int(current_time_str)
   wait_time_int = int(wait_time_int)

   final_time_int = current_time_int + wait_time_int
   print(final_time_int)

Can you see what is wrong, just by looking at the code?  Maybe, maybe not.  Our brain tends to see what we think is there, so sometimes it is very hard to find the problem just by looking at the code.  Especially when it is our own code and we are sure that we have done everything right!

Lets try the program again, but this time in an activecode:

.. activecode:: db_ex3_5

   current_time_str = input("what is the current time (in hours 0-23)?")
   wait_time_str = input("How many hours do you want to wait")

   current_time_int = int(current_time_str)
   wait_time_int = int(wait_time_int)

   final_time_int = current_time_int + wait_time_int
   print(final_time_int)


Aha!  Now we have an error message that might be useful.  The name error tells us that  ``wait_time_int`` is not defined.  It also tells us that the error is on line 5.  That's **really** useful information.  Now look at line five and you will see that ``wait_time_int`` is used on both the left and the right hand side of the assignment statement. 

.. mchoicemf:: db_qex32
   :answer_a: You cannot use a variable on both the left and right hand sides of an assignment statement.
   :answer_b: wait_time_int does not have a value so it cannot be used on the right hand side.
   :answer_c: This is not really an error, Python is broken.
   :correct: b
   :feedback_a: No, You can, as long as all the variables on the right hand side already have values.
   :feedback_b: Yes.  Variables must already have values in order to be used on the right hand side.
   :feedback_c: No, No, No!

   Which of the following explains why ``wait_time_int = int(wait_time_int)`` is an error.


In writing and using this book over the last few years we have collected a lot of statistics about the programs in this book.  Here are some statistics about error messages for the exercise we have been looking at.

=================== ======= =======
Message             Number  Percent
=================== ======= =======
ParseError:         4999    54.74%
TypeError:          1305    14.29%
NameError:          1009    11.05%
ValueError:         893     9.78%
URIError:           334     3.66%
TokenError:         244     2.67%
SyntaxError:        227     2.49%
TimeLimitError:     44      0.48%
IndentationError:   28      0.31%
AttributeError:     27      0.30%
ImportError:        16      0.18%
IndexError:         6       0.07%
=================== ======= =======

Nearly 90% of the error messages encountered for this  problem are ParseError, TypeError, NameError, or ValueError.  We will look at these errors in three stages:

* First we will define what these four error messages mean.
* Then, we will look at some examples that cause these errors to occur.
* Finally we will look at ways to help uncover the root cause of these messages.


ParseError
^^^^^^^^^^

Parse errors happen when you make an error in the syntax of your program.  Syntax errors are like making grammatical errors in writing.  If you don't use periods and commas in your writing then you are making it hard for other readers to figure out what you are trying to say.  Similarly Python has certain grammatical rules that must be followed or else Python can't figure out what you are trying to say.

Usually ParseErrors can be traced back to missing punctuation characters, such as parenthesis, qutation marks, or commas. Remember that in Python commas are used to separate parameters to functions.  Paretheses must be balanced, or else Python thinks that you are trying to include everything that follows as a parameter to some function.

Here are a couple examples of Parse errors in the example program we have been using.  See if you can figure out what caused them.

.. tabbed:: db_tabs1

    .. tab:: Question

        Find and fix the error in the following code.

        .. activecode:: db_ex3_6

           current_time_str = input("what is the current time (in hours 0-23)?")
           wait_time_str = input("How many hours do you want to wait"

           current_time_int = int(current_time_str)
           wait_time_int = int(wait_time_str)

           final_time_int = current_time_int + wait_time_int
           print(final_time_int)

    .. tab:: Answer

        .. sourcecode:: python

           current_time_str = input("what is the current time (in hours 0-23)?")
           wait_time_str = input("How many hours do you want to wait"

           current_time_int = int(current_time_str)
           wait_time_int = int(wait_time_str)

           final_time_int = current_time_int + wait_time_int
           print(final_time_int)

        Since the error message points us to line 4 this might be a bit confusing.  If you look at line four carefully you will see that there is no problem with the syntax.  So, in this case the next step should be to back up and look at the previous line.  In this case if you look at line 2 carefully you will see that there is a missing right parenthesis at the end of the line.  Remember that parenthses must be balanced.  Since Python allows statements to continue over multiple lines inside parentheses python will continue to scan subsequent lines looking for the balancing right parenthesis.  However in this case it finds the name ``current_time_int`` and it will want to interpret that as another parameter to the input function.  But, there is not a comma to separate the previous string from the variable so as far as Python is concerned the error here is a missing comma.  From your perspective its a missing parenthesis.

**Finding Clues**  How can you help yourself find these problems?  One trick that can be very valuable in this situation is to simply start by commenting out the line number that is flagged as having the error.  If you comment out line four, the error message now changes to point to line 5.  Now you ask yourself, am I really that bad that I have two lines in a row that have errors on them?  Maybe, so taken to the extreme, you could comment out all of the remaining lines in the program. Now the error message changes to ``TokenError: EOF in multi-line statement``  This is a very technical way of saying that Python got to the end of file (EOF) while it was still looking for something.  In this case a right parenthesis.



.. tabbed:: db_tabs2

    .. tab:: Question

        Find and fix the error in the following code.

        .. activecode:: db_ex3_7

           current_time_str = input("what is the "current time" (in hours 0-23)?")
           wait_time_str = input("How many hours do you want to wait")

           current_time_int = int(current_time_str)
           wait_time_int = int(wait_time_str)

           final_time_int = current_time_int + wait_time_int
           print(final_time_int)

    .. tab:: Answer

        .. sourcecode:: python

           current_time_str = input("what is the "current time" (in hours 0-23)?")
           wait_time_str = input("How many hours do you want to wait")

           current_time_int = int(current_time_str)
           wait_time_int = int(wait_time_str)

           final_time_int = current_time_int + wait_time_int
           print(final_time_int)

        The error message points you to line 1 and in this case that is exactly where the error occurs. In this case your biggest clue is to notice the difference in  highlighting on the line.  Notice that the words "current time" are a different color than those around them.  Why is this?  Because "current time" is in double quotes inside another pair of double quotes Python things that you are finishing off one string, then you have some other names and findally another string.  But you haven't separated these names or strings by commas, and you haven't added them together with the concatenation operator (+).  So, there are several corrections you could make.  First you could make the argument to input be as follows:  ``"what is the 'current time' (in hours 0-23)"``  Notice that here we have correctly used single quotes inside double quotes.   Another option is to simply remove the extra double quotes.  Why were you quoting "current time" anyway?  ``"what is the current time (in hours 0-23)"``

**Finding Clues**  If you follow the same advice as for the last problem, comment out line one, you will immediately get a different error message.  Here's where you need to be very careful and not panic.  The error message you get now is: ``NameError: name 'current_time_str' is not defined on line 4``.  You might be very tempted to think that this is somehow related to the earlier problem and immediately conclude that there is something wrong with the variable name ``current_time_str`` but if you reflect for a minute  You will see that by commenting out line one you have caused a new and unrelated error.  That is, you have commented out the creation of the name ``current_time_str``.  So of course when you want to convert it to an ``int`` you will get the NameError.  Yes, this can be confusing, but it will become much easier with experience.  It's also important to keep calm, and evaluate each new clue carefully so you don't waste time chasing problems that are not really there.  

Uncomment line 1 and you are back to the ParseError.  Another track is to eliminate a possible source of error.  Rather than commenting out the entire line you might just try to assign ``current_time_str`` to a constant value.  For example you might make line one look like this:  ``current_time_str = "10"  #input("what is the "current time" (in hours 0-23)?")``.  Now you have assigned ``current_time_str`` to the string 10, and commented out the input statement.  And now the program works!  So you conclude that the problem must have something to do with the input function.

The color coding that happens automatically in ActiveCode windows can help with identifying some kinds of syntax errors.
For example, in original code for the exercise above, notice that "What is the" is in one color, and current time is in another color. That's
your clue that it thinks the string ends after the word the (because there's a closing double-quote). Also, notice that
when you put your cursor to left of a ``)``, it changes the color of that parenthesis and its matching ``(``. And similarly if
you put the cursor to the left of ``(``. But check what happens if the ``(`` has no matching ``)``.

.. mchoicemf:: db_qex33
   :answer_a: Nothing. The program has a syntax error and can't run.
   :answer_b: The left parenthesis turns green.
   :answer_c: The left parenthesis turns red.
   :correct: c
   :feedback_a: You may be reading too fast and not trying to test your understanding using an ActiveCode window
   :feedback_b: Sounds like you tried it on a left paren that did have a matching right paren.
   :feedback_c: This color coding is your friend and can help you notice and fix parenthesis errors

   In an ActiveCode window, what happens when you put the cursor left of a left parenthesis ``(`` that has no matching right parenthesis ``)``?


TypeError
^^^^^^^^^

TypeErrors occur when you you try to combine two objects that are not compatible.  For example you try to add together an integer and a string.  Usually type errors can be isolated to lines that are using mathematical operators, and usually the line number given by the error message is an accurate indication of the line.

Here's an example of a type error created by a Polish learner.  See if you can find and fix the error.

.. activecode:: db_ex3_8

    a = input('wpisuj cieciu godzine')
    x = input('wpisuj ile godzin cieciu')
    int(x)
    int(a)
    h = x // 24
    s = x % 24
    print (h, s)
    a = a + s
    print ('godzina teraz %s' %a) 



.. reveal:: dbex38_rev
    :showtitle: Show me the Solution
    :hidetitle: Hide

    .. admonition:: Solution

        In finding this error there are a few lessons to think about.  First, you may find it very disconcerting that you cannot understand the whole program.  Unless, of course, you speak Polish.  But, learning what you can ignore, and what you need to focus on is a very important part of the debugging process.  Second, types and good variable names are important and can be very helpful.  In this case a and x are not particularly helpful names, and in particular they do not help you think about the types of your variables, which as the error message implies is the root of the problem here.  The rest of the lessons we will get back to in a minute.

        The error message provided to you gives you a pretty big hint.  ``TypeError: unsupported operand type(s) for FloorDiv: 'str' and 'number' on line: 5``  On line five we are trying to use integer division on x and 24.  The error message tells you that you are tyring to divide a string by a number.  In this case you know that 24 is a number so x must be a string.  But how?  You can see the function call on line 3 where you are converting x to an integer.  ``int(x)`` or so you think.  This is lesson three and is one of the most common errors we see in introductory programming.  What is the difference between ``int(x)`` and ``x = int(x)``

        * The expression ``int(x)`` converts the string referenced by x to an integer but it does not store it anywhere.  It is very common to assume that ``int(x)`` somehow changes x itself, as that is what you are intending!  The thing that makes this very tricky is that ``int(x)`` is a valid expression, so it doesn't cause any kind of error, but rather the error happens later on in the program.

        * The assignment statement  ``x = int(x)`` is very different.  Again, the ``int(x)`` expression converts the string referenced by x to an integer, but this time it also changes what x references so that x now refers to the integer value returned by the ``int`` function.  

        So, the solution to this problem is to change lines 3 and 4 so they are assignment statements.


**Finding Clues**  One thing that can help you in this situation is to print out the values and the types of the variables involved in the statement that is causing the error.  You might try adding a print statement after line 4 ``print(x, type(x))``  You will see that at least we have confirmed that x is of type string.  Now you need to start to work backward through the program.  You need to ask yourself, where is x used in the program?  x is used on lines 2, 3, and of course 5 and 6 (where we are getting an error).  So maybe you move the print statement to be after line 2 and again after 3.  Line Three is where you expect the value of x to be changed to an integer.  Could line 4 be mysteriously changine x back to a string?  Not very likely.  So the value and type of x is just what you would expect it to be after line 2, but not after line 3.  This helps you isolate the problem to line 3.  In fact if you employ one of our earler techniques of commenting out line 3 you will see that this has no impact on the error, and is a big clue that line 3 as it is currently written is useless.


NameError
^^^^^^^^^

Name errors almost always mean that you have used a variable before it has a value.  Often NameErrors are simply caused by typos in your code.  They can be hard to spot if you don't have a good eye for catching spelling mistakes.  Other times you may simply mis-remember the name of a variable or even a function you want to call.    You have seen one example of a NameError at the beginning of this section.  Here is another one.  See if you can get this program to run successfully:

.. activecode:: db_ex3_9

    str_time=input("what time is it now?")
    str_wait_time=input("what is the number of nours to wait?")
    time=int(str_time)
    wai_time=int(str_wait_time)

    time_when_alarm_go_off=time+wait_time
    print time_when_alarm_go_off

.. reveal:: db_ex39_reveal
    :showtitle: Show me the Solution

    .. admonition:: Solution

        In this example, the student seems to be a fairly bad speller, as there are a number of typos to fix.  The first one is identified as wait_time is not defined on line 6.  Now in this example you can see that there is ``str_wait_time`` on line 2, and  ``wai_time`` on line 4 and ``wait_time`` on line 6.   If you do not have very sharp eyes its easy to miss that there is a typo on line 4.

**Finding Clues**  With name errors one of the best things you can do is use the editor, or browser search function.  Quite often if you search for the exact word in the error message one of two things will happen:

1.  The word you are searching for will appear only once in your code, its also likely that it will be on the right hand side of an assignment statment, or as a parameter to a function.  That should confirm for you that you have a typo somewhere.  If the name in question **is** what you thought it should be then you probably have a typo on the left hand side of an assignment statement on a line before your error message occurs.  Start looking backward at your assignment statements.  In some cases it's really nice to leave all the highlighted strings from the search function visible as they will help you very quickly find a line where you might have expected your variable to be highlighted.

2.  The second thing that may happen is that you will be looking directly at a line where you expected the search to find the string in question, but it will not be highlighted.  Most often that will be the typo right there.


Here is another one for you to try:

.. activecode:: db_ex3_10

    n = input("What time is it now (in hours)?")
    n = imt(n)
    m = input("How many hours do you want to wait?")
    m = int(m)
    q = m % 12
    print("The time is now", q)


.. reveal:: db_ex310_reveal
    :showtitle:  Show me the Solution

    .. admonition:: Solution    

        This one is once again a typo, but the typo is not in a variable name, but rather, the name of a function.  The search strategy would help you with this one easily, but there is another clue for you as well.  The editor in the textbook, as well as almost all Python editors in the world provide you with color clues.  Notice that on line 2 the function ``imt`` is not highlighted blue like the word ``int`` on line 4.


And one last bit of code to fix.

.. activecode:: db_ex3_11

    present_time = input("enter the present timein hours:")
    set_alarm = input("set the hours for alarm:")
    int (present_time,set_time,alarm_time)
    alarm_time = present_time + set_alarm
    print (alarm_time)

.. reveal:: db_ex311_reveal
    :showtitle: Show me the Solution

    .. admonition:: Solution

        In this example the error message is about ``set_time`` not defined on line 3.  In this case the undefined name is not used in an assignment statement, but is used as a parameter (incorrectly) to a function call.   A search on ``set_time`` reveals that in fact it is only used once in the program.  Did the author mean ``set_alarm``?  If we make that assumption we immediately get another error ``NameError: name 'alarm_time' is not defined on line: 3``.  The variable ``alarm_time`` is defined on line 4, but that does not help us on line 3.  Furthermore we now have to ask the question is this function call ``int(present_time,set_alarm,alarm_time)`` even the correct use of the ``int`` function?  The answer to that is a resounding no.  Lets list all of the things wrong with line 3:

        1.  ``set_time`` is not defined and never used, the author probably meant ``set_alarm``.
        2.  ``alarm_time`` cannot be used as a parameter before it is defined, even on the next line!
        3.  ``int`` can only convert one string to an integer at a time.
        4.  Finally, ``int`` should be used in an assignment statement.  Even if ``int`` was called with the correct number of parameters it would have no real effect.


.. advanced topic!

.. present_time = int(input("enter the present time(hhmm):"))
.. print type(present_time)

.. min = _ * 60 
.. tot_min = min + [2,4]
.. print (tot_min)
.. set_hrs = int(input("enter the hours (hhmm):"))
.. alarm_time = present_time + set_hrs
.. print (alarm_time)


ValueError
^^^^^^^^^^

Value errors occur when you pass a parameter to a function and the function is expecting a certain type, but you pass it a different type.  We can illustrate that with this particular program in two different ways.

.. activecode:: db_ex3_12

   current_time_str = input("what is the current time (in hours 0-23)?")
   current_time_int = int(current_time_str)

   wait_time_str = input("How many hours do you want to wait")
   wait_time_int = int(wait_time_int)

   final_time_int = current_time_int + wait_time_int
   print(final_time_int)


Run the program but instead of typing in anything to the dialog box just click OK.  You should see the following error message:  ``ValueError: invalid literal for int() with base 10: '' on line: 2``   This error is not because you have made a mistake in your program.  Although usually we do want to check the user input to make sure its valid, we don't have all the tools we need for that yet at this point in the course.  The error happens because the user did not give us something we can convert to an integer, instead we gave it an empty value.  Try running the program again.  Now this time enter "ten" instead of the number 10.  You will get a similar error message.

ValueErrors are not always caused by user input error, but in this program that is the case.  We'll look again at ValueErrors again when we get to more complicated programs.  For now it is worth repeating that you need to keep track of the types of your variables, and understand what types your function is expecting.  You can do this by writing comments in your code, or by naming your variables in a way that reminds you of their type.


Summary
~~~~~~~

* Make sure you take the time to understand error messages.  They can help you a lot.

* ``print`` statements are your friends.  Use them to help you uncover what is **really** happening in your code.

* Work backward from the error.  Many times an error message is caused by something that has happened before it in the program.  Always remember that python evaluates a program top to bottom.

