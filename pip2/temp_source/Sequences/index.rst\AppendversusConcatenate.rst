..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Append versus Concatenate
-------------------------

The ``append`` method adds a new item to the end of a list.  It is also possible to add a new item to the end of a list by using the concatenation operator.  However, you need to be careful.

Consider the following example.  The original list has 3 integers.  We want to add the word "cat" to the end of the list.

.. codelens:: appcon1

    origlist = [45,32,88]

    origlist.append("cat")



Here we have used ``append`` which simply modifies the list.  In order to use concatenation, we need to write an assignment statement that uses the accumulator pattern::

    origlist = origlist + ["cat"]

Note that the word "cat" needs to be placed in a list since the concatenation operator needs two lists to do its work.

.. codelens:: appcon2

    origlist = [45,32,88]

    origlist = origlist + ["cat"]


It is also important to realize that with append, the original list is simply modified.  
On the other hand, with concatenation, an entirely new list is created.  This can be seen in the following codelens example where
``newlist`` refers to a list which is a copy of the original list, ``origlist``, with the new item "cat" added to the end.  ``origlist`` still contains the three values it did before the concatenation.  This is why the assignment operation is necessary as part of the
accumulator pattern.

.. codelens:: appcon3

    origlist = [45,32,88]

    newlist = origlist + ["cat"]


**Check your understanding**

.. mchoicemf:: test_question9_15_1
   :answer_a: [4,2,8,6,5,999]
   :answer_b: Error, you cannot concatenate a list with an integer.
   :correct: b
   :feedback_a: You cannot concatenate a list with an integer.
   :feedback_b: Yes, in order to perform concatenation you would need to write alist+[999].  You must have two lists.
   
   What is printed by the following statements?
   
   .. code-block:: python

     alist = [4,2,8,6,5]
     alist = alist + 999
     print(alist)


.. note::

   This workspace is provided for your convenience.  You can use this activecode window to try out anything you like.

   .. activecode:: scratch_09_03

Splitting and Joining Strings
=============================

Two of the most useful methods on strings involve lists of
strings. The ``split`` method
breaks a string into a list of words.  By
default, any number of whitespace characters is considered a word boundary.

.. activecode:: ch09_split1
    
    song = "The rain in Spain..."
    wds = song.split()
    print(wds)

An optional argument called a **delimiter** can be used to specify which
characters to use as word boundaries. The following example uses the string
``ai`` as the delimiter:

.. activecode:: ch09_split2
    
    song = "The rain in Spain..."
    wds = song.split('ai')
    print(wds)

Notice that the delimiter doesn't appear in the result.

The inverse of the ``split`` method is ``join``.  You choose a
desired **separator** string, (often called the *glue*) 
and join the list with the glue between each of the elements.

.. activecode:: ch09_join

    wds = ["red", "blue", "green"]
    glue = ';'
    s = glue.join(wds)
    print(s)
    print(wds)

    print("***".join(wds))
    print("".join(wds))


The list that you glue together (``wds`` in this example) is not modified.  Also, 
you can use empty glue or multi-character strings as glue.


Summary
=======

This chapter introduced a lot of new ideas.  The following summary 
may prove helpful in remembering what you learned.

.. glossary::

    indexing (``[]``)
        Access a single character in a string using its position (starting from
        0), or a single item from a list.  Example: ``'This'[2]`` evaluates to ``'i'``.
        Example: ``[10, 20, 'hello'][1]`` evaluates to ``20``

    length function (``len``)
        Returns the number of characters in a string or a list.  Example:
        ``len('happy')`` evaluates to ``5``.
        Example: ``len([10, 20 'hello'])`` evaluates to 3

    slicing (``[:]``)
        A *slice* is a substring of a string or a list. Example: ``'bananas and
        cream'[3:6]`` evaluates to ``ana`` (so does ``'bananas and
        cream'[1:4]``).
        Example: ``[10, 20, 'hello', 'goodbye'][1:3]`` evaluates to ``[20, 'hello']``

    string comparison (``>, <, >=, <=, ==, !=``)
        The six common comparision operators work with strings, evaluating according to
        `lexigraphical order
        <http://en.wikipedia.org/wiki/Lexicographic_order>`__.  Examples:
        ``'apple' < 'banana'`` evaluates to ``True``.  ``'Zeta' < 'Appricot'``
        evaluates to ``False``.  ``'Zebra' <= 'aardvark'`` evaluates to
        ``True`` because all upper case letters precede lower case letters.

    in and not in operator (``in``, ``not in``)
        The ``in`` operator tests whether one string is contained
        inside another string.  Examples: ``'heck' in "I'll be checking for
        you."`` evaluates to ``True``.  ``'cheese' in "I'll be checking for
        you."`` evaluates to ``False``.

    collection data type
        A data type in which the values are made up of components, or elements,
        that are themselves values.

    dot notation
        Use of the **dot operator**, ``.``, to access methods and attributes of an object.

    immutable
        A compound data type whose elements can not be assigned new values.

    index
        A variable or value used to select a member of an ordered collection, such as
        a character from a string, or an element from a list.

    whitespace
        Any of the characters that move the cursor without printing visible
        characters. The constant ``string.whitespace`` contains all the
        white-space characters.
        
    aliases
        Multiple variables that contain references to the same object.

    clone
        To create a new object that has the same value as an existing object.
        Copying a reference to an object creates an alias but doesn't clone the
        object.

    delimiter
        A character or string used to indicate where a string should be split.

    element
        One of the values in a list (or other sequence). The bracket operator
        selects elements of a list.

    mutable data type
        A data type in which the elements can be modified. All mutable types
        are compound types. Lists are mutable data types; strings are not.

    object
        A thing to which a variable can refer.

        


Exercises
=========

1.

    .. tabbed:: q1

        .. tab:: Question

            What is the result of each of the following:
        
            a. 'Python'[1]
            #. "Strings are sequences of characters."[5]
            #. len("wonderful")
            #. 'Mystery'[:4]
            #. 'p' in 'Pineapple'
            #. 'apple' in 'Pineapple'
            #. 'pear' not in 'Pineapple'
            #. 'apple' > 'pineapple'
            #. 'pineapple' < 'Peach'

        .. tab:: Answer

            a. 'Python'[1] evaluates to 'y'
            #. 'Strings are sequences of characters.'[5] evaluates to 'g'
            #. len('wonderful') evaluates to 9
            #. 'Mystery'[:4] evaluates to 'Myst'
            #. 'p' in 'Pineapple' evaluates to True
            #. 'apple' in 'Pineapple' evaluates to True
            #. 'pear' not in 'Pineapple' evaluates to True
            #. 'apple' > 'pineapple' evaluates to False
            #. 'pineapple' < 'Peach' evaluates to False

#.  
   .. tabbed:: q2
   
      .. tab:: Question
   
         Write code that asks the user to type something and deletes all occurrences of the word "like".
         
         .. actex:: ex_3_1
         
      .. tab:: Answer
      
         .. activecode:: q2_answer
            
            x = raw_input("Enter some text that overuses the word like")
            y = x.replace("like", "")
            print y


#.  
   .. tabbed:: q3
   
      .. tab:: Question

         Write code that asks the user to type something and removes all the vowels from it, then prints it out.

         .. actex:: ex_3_2


#.  
   .. tabbed:: q4

      .. tab:: Question
      
         Write code that transforms the list ``[3, 6, 9]`` into the list ``[3, 0, 9]`` and then prints it out
   
      .. actex:: ex_3_3

         w = [3, 6, 9]
         # add code that changes w
         
