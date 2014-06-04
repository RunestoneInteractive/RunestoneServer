..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

String Methods
--------------

We previously saw that each turtle instance has its own attributes and 
a number of methods that can be applied to the instance.  For example,
we wrote ``tess.right(90)`` when we wanted the turtle object ``tess`` to perform the ``right`` method to turn
to the right 90 degrees.  The "dot notation" is the way we connect the name of an object to the name of a method
it can perform.  

Strings are also objects.  Each string instance has its own attributes and methods.  The most important attribute of the string is the collection of characters.  There are a wide variety of methods.  Try the following program.

.. activecode:: chp08_upper

    ss = "Hello, World"
    print(ss.upper())

    tt = ss.lower()
    print(tt)


In this example, ``upper`` is a method that can be invoked on any string object 
to create a new string in which all the 
characters are in uppercase.  ``lower`` works in a similar fashion changing all characters in the string
to lowercase.  (The original string ``ss`` remains unchanged.  A new string ``tt`` is created.)

In addition to ``upper`` and ``lower``, the following table provides a summary of some other useful string methods.  There are a few activecode examples that follow so that you can try them out.

==========  ==============      ==================================================================
Method      Parameters          Description
==========  ==============      ==================================================================
upper       none                Returns a string in all uppercase
lower       none                Returns a string in all lowercase
capitalize  none                Returns a string with first character capitalized, the rest lower

strip       none                Returns a string with the leading and trailing whitespace removed
lstrip      none                Returns a string with the leading whitespace removed
rstrip      none                Returns a string with the trailing whitespace removed
count       item                Returns the number of occurrences of item
replace     old, new            Replaces all occurrences of old substring with new

center      width               Returns a string centered in a field of width spaces
ljust       width               Returns a string left justified in a field of width spaces
rjust       width               Returns a string right justified in a field of width spaces

find        item                Returns the leftmost index where the substring item is found
rfind       item                Returns the rightmost index where the substring item is found
index       item                Like find except causes a runtime error if item is not found
rindex      item                Like rfind except causes a runtime error if item is not found
==========  ==============      ==================================================================

You should experiment with these
methods so that you understand what they do.  Note once again that the methods that return strings do not
change the original.  You can also consult the `Python documentation for strings <http://docs.python.org/py3k/library/stdtypes.html#index-21>`_.

.. activecode:: ch08_methods1

    ss = "    Hello, World    "

    els = ss.count("l")
    print(els)

    print("***" + ss.strip() + "***")
    print("***" + ss.lstrip() + "***")
    print("***" + ss.rstrip() + "***")

    news = ss.replace("o", "***")
    print(news)


.. activecode:: ch08_methods2


    food = "banana bread"
    print(food.capitalize())

    print("*" + food.center(25) + "*")
    print("*" + food.ljust(25) + "*")     # stars added to show bounds
    print("*" + food.rjust(25) + "*")

    print(food.find("e"))
    print(food.find("na"))
    print(food.find("b"))

    print(food.rfind("e"))
    print(food.rfind("na"))
    print(food.rfind("b"))

    print(food.index("e"))


**Check your understanding**

.. mchoicemf:: test_question8_3_1
   :answer_a: 0
   :answer_b: 2
   :answer_c: 3
   :correct: c
   :feedback_a: There are definitely o and p characters.
   :feedback_b: There are 2 o characters but what about p?
   :feedback_c: Yes, add the number of o characters and the number of p characters.


   What is printed by the following statements?
   
   .. code-block:: python
   
      s = "python rocks"
      print(s.count("o") + s.count("p"))




.. mchoicemf:: test_question8_3_2
   :answer_a: yyyyy
   :answer_b: 55555
   :answer_c: n
   :answer_d: Error, you cannot combine all those things together.
   :correct: a
   :feedback_a: Yes, s[1] is y and the index of n is 5, so 5 y characters.  It is important to realize that the index method has precedence over the repetition operator.  Repetition is done last.
   :feedback_b: Close.  5 is not repeated, it is the number of times to repeat.
   :feedback_c: This expression uses the index of n
   :feedback_d: This is fine, the repetition operator used the result of indexing and the index method.


   What is printed by the following statements?
   
   .. code-block:: python
   
      s = "python rocks"
      print(s[1] * s.index("n"))


.. index::
    single: len function
    single: function; len
    single: runtime error
    single: negative index
    single: index; negative

