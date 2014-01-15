..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

The Slice Operator
------------------

A substring of a string is called a **slice**. Selecting a slice is similar to
selecting a character:

.. activecode:: chp08_slice1
    
    singers = "Peter, Paul, and Mary"
    print(singers[0:5])
    print(singers[7:11])
    print(singers[17:21])
    

The `slice` operator ``[n:m]`` returns the part of the string from the n'th character
to the m'th character, including the first but excluding the last. In other words,  start with the character at index n and
go up to but do not include the character at index m.
This
behavior may seem counter-intuitive but if you recall the ``range`` function, it did not include its end
point either.

If you omit the first index (before the colon), the slice starts at the
beginning of the string. If you omit the second index, the slice goes to the
end of the string.

.. activecode:: chp08_slice2
    
    fruit = "banana"
    print(fruit[:3])
    print(fruit[3:])

What do you think ``fruit[:]`` means?

**Check your understanding**

.. mchoicemf:: test_question8_5_1
   :answer_a: python
   :answer_b: rocks
   :answer_c: hon r
   :answer_d: Error, you cannot have two numbers inside the [ ].
   :correct: c
   :feedback_a: That would be s[0:6].
   :feedback_b: That would be s[7:].
   :feedback_c: Yes, start with the character at index 3 and go up to but not include the character at index 8.
   :feedback_d: This is called slicing, not indexing.  It requires a start and an end.


   What is printed by the following statements?
   
   .. code-block:: python

      s = "python rocks"
      print(s[3:8])



.. mchoicemf:: test_question8_5_2
   :answer_a: rockrockrock
   :answer_b: rock rock rock
   :answer_c: rocksrocksrocks
   :answer_d: Error, you cannot use repetition with slicing.
   :correct: a
   :feedback_a: Yes, rock starts at 7 and goes thru 10.  Repeat it 3 times.
   :feedback_b: Repetition does not add a space.
   :feedback_c: Slicing will not include the character at index 11.  Just up to it (10 in this case).
   :feedback_d: The slice will happen first, then the repetition.  So it is ok.


   What is printed by the following statements?
   
   .. code-block:: python

      s = "python rocks"
      print(s[7:11]*3)



.. note::

    This workspace is provided for your convenience.  You can use this activecode window to try out anything you like.

    .. activecode:: scratch_08_01



.. index:: string comparison, comparison of strings

