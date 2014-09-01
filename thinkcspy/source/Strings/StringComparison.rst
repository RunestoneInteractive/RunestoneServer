..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

.. qnum::
   :prefix: strings-8-
   :start: 1

String Comparison
-----------------

The comparison operators also work on strings. To see if two strings are equal you simply write a boolean
expression using the equality operator.

.. activecode:: ch08_comp1
    
    word = "banana"
    if word == "banana":
        print("Yes, we have bananas!")
    else:
        print("Yes, we have NO bananas!")

Other comparison operations are useful for putting words in
`lexicographical order <http://en.wikipedia.org/wiki/Lexicographic_order>`__.
This is similar to the alphabetical order you would use with a dictionary,
except that all the uppercase letters come before all the lowercase letters.

.. activecode:: ch08_comp2

    word = "zebra"
    
    if word < "banana":
        print("Your word, " + word + ", comes before banana.")
    elif word > "banana":
        print("Your word, " + word + ", comes after banana.")
    else:
        print("Yes, we have no bananas!")


It is probably clear to you that the word `apple` would be less than (come before) the word ``banana``.
After all, `a` is before `b` in the alphabet.  But what if we consider the words ``apple`` and ``Apple``?
Are they the same?  

.. activecode:: chp08_ord1

    print("apple" < "banana")

    print("apple" == "Apple")
    print("apple" < "Apple")

It turns out, as you recall from our discussion of variable names, that uppercase and lowercase letters are considered to be different from one another.  The way the computer knows they are different is that
each character is assigned a unique integer value.  "A" is 65, "B" is 66, and "5" is 53.  The way you can
find out the so-called **ordinal value** for a given character is to use a character function called ``ord``.

.. activecode:: ch08_ord2

    print(ord("A"))
    print(ord("B"))
    print(ord("5"))

    print(ord("a"))
    print("apple" > "Apple")

When you compare characters or strings to one another, Python converts the characters into their equivalent ordinal values and compares the integers from left to right.  As you can see from the example above, "a" is greater than "A" so "apple" is greater than "Apple".

Humans commonly ignore capitalization when comparing two words.  However, computers do not.  A common way to address this issue is to convert strings to a standard
format, such as all lowercase, before performing the comparison. 

There is also a similar function called ``chr`` that converts integers into their character equivalent.

.. activecode:: ch08_ord3

    print(chr(65))
    print(chr(66))

    print(chr(49))
    print(chr(53))

    print("The character for 32 is", chr(32), "!!!")
    print(ord(" "))

One thing to note in the last two examples is the fact that the space character has an ordinal value (32).  Even though you don't see it, it is an actual character.  We sometimes call it a *nonprinting* character.

**Check your understanding**

.. mchoicemf:: test_question8_6_1
   :answer_a: True
   :answer_b: False
   :correct: a
   :feedback_a: Both match up to the g but Dog is shorter than Doghouse so it comes first in the dictionary.
   :feedback_b: Strings are compared character by character.
   
   Evaluate the following comparison:
   
   .. code-block:: python

      "Dog" < "Doghouse"

   
   
.. mchoicemf:: test_question8_6_2
   :answer_a: True
   :answer_b: False
   :answer_c: They are the same word
   :correct: b
   :feedback_a: d is greater than D according to the ord function (68 versus 100).
   :feedback_b: Yes, upper case is less than lower case according to the ordinal values of the characters.
   :feedback_c: Python is case sensitive meaning that upper case and lower case characters are different.
   
   Evaluate the following comparison:
   
   .. code-block:: python

      "dog" < "Dog"

   
  
.. mchoicemf:: test_question8_6_3
   :answer_a: True
   :answer_b: False
   :correct: b
   :feedback_a: d is greater than D.
   :feedback_b: The length does not matter.  Lower case d is greater than upper case D.

   Evaluate the following comparison:
   
   .. code-block:: python

      "dog" < "Doghouse"


   

.. index:: mutable, immutable, runtime error

