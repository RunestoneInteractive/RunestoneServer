..  Copyright (C)  Paul Resnick, Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".
    
..  shortname:: Strings
..  description:: Introduction to the string data type, operators, and methods.

.. qnum::
   :prefix: str-
   :start: 1

.. _sequences_chap:

Sequences
=========

So far we have seen built-in types like: ``int``, ``float``, 
``bool``, and ``str``. 
``int``, ``float``, and
``bool`` are considered to be simple or primitive or atomic data types because their values are not composed
of any smaller parts.  They cannot be broken down.

On the other hand, strings and lists are different from the others because they
are made up of smaller pieces.  In the case of strings, they are made up of smaller
strings each containing one **character**.  

Types that are comprised of smaller pieces are called **collection data types**.
Depending on what we are doing, we may want to treat a collection data type as a
single entity (the whole), or we may want to access its parts. This ambiguity is useful.

In this chapter we will examine operations that can be performed on sequences, such as picking 
out individual elements or subsequences (called slices) or computing their length. In addition, we'll
examine some special functions that are defined only for strings, and we'll find out one importance
difference between strings and lists, that lists can be changed (or mutated) while strings are immutable.


Strings
=======

.. index:: compound data type, character, subscript operator, index

Strings can be defined as sequential collections of characters.  This means that the individual characters
that make up a string are in a particular order from left to right.

A string that contains no characters, often referred to as the **empty string**, is still considered to be a string.  
It is simply a sequence of zero characters and is represented by '' or "" 
(two single or two double quotes with nothing in between).

.. index:: string operations, concatenation

Operations on Strings
---------------------

In general, you cannot perform mathematical operations on strings, even if the
strings look like numbers. The following are illegal (assuming that ``message``
has type string):

.. sourcecode:: python
    
    message - 1   
    "Hello" / 123   
    message * "Hello"   
    "15" + 2

Interestingly, the ``+`` operator does work with strings, but for strings, the
``+`` operator represents **concatenation**, not addition.  Concatenation means
joining the two operands by linking them end-to-end. For example:

.. activecode:: ch08_add
    :nocanvas:

    fruit = "banana"
    bakedGood = " nut bread"
    print(fruit + bakedGood)

The output of this program is ``banana nut bread``. The space before the word
``nut`` is part of the string and is necessary to produce the space between
the concatenated strings.  Take out the space and run it again.

The ``*`` operator also works on strings.  It performs repetition. For example,
``'Fun'*3`` is ``'FunFunFun'``. One of the operands has to be a string and the
other has to be an integer.

.. activecode:: ch08_mult
    :nocanvas:

    print("Go"*6)

    x = "Blue"
    print(x * 3)

    print("Go" * 3 + x)

    print(("Go " + x + "  ") * 3)

This interpretation of ``+`` and ``*`` makes sense by analogy with
addition and multiplication. Just as ``4*3`` is equivalent to ``4+4+4``, we
expect ``"Go"*3`` to be the same as ``"Go"+"Go"+"Go"``, and it is.  Note also in the last
example that the order of operations for ``*`` and ``+`` is the same as it was for arithmetic.
The repetition is done before the concatenation.  If you want to cause the concatenation to be
done first, you will need to use parentheses.

**Check your understanding**

.. mchoicemf:: test_question8_1_1 
   :answer_a: python rocks
   :answer_b: python
   :answer_c: pythonrocks
   :answer_d: Error, you cannot add two strings together.
   :correct: c
   :feedback_a: Concatenation does not automatically add a space.
   :feedback_b: The expression s+t is evaluated first, then the resulting string is printed.
   :feedback_c: Yes, the two strings are glued end to end.
   :feedback_d: The + operator has different meanings depending on the operands, in this case, two strings.


   What is printed by the following statements?
   
   .. code-block:: python

      s = "python"
      t = "rocks"
      print(s+t)



.. mchoicemf:: test_question8_1_2
   :answer_a: python!!!
   :answer_b: python!python!python!
   :answer_c: pythonpythonpython!
   :answer_d: Error, you cannot perform concatenation and repetition at the same time.
   :correct: a
   :feedback_a: Yes, repetition has precedence over concatenation
   :feedback_b: Repetition is done first.
   :feedback_c: The repetition operator is working on the excl variable.
   :feedback_d: The + and * operator are defined for strings as well as numbers.


   What is printed by the following statements?
   
   .. code-block:: python
 
      s = "python"
      excl = "!"
      print(s+excl*3)




Index Operator: Working with the Characters of a String
-------------------------------------------------------

The **indexing operator** (Python uses square brackets to enclose the index) 
selects a single character from a string.  The characters are accessed by their position or 
index value.  For example, in the string shown below, the 14 characters are indexed left to right 
from postion 0 to position 13.  


.. image:: Figures/indexvalues.png
   :alt: index values

It is also the case that the positions are named from right to left using negative numbers where -1 is the rightmost
index and so on.
Note that the character at index 6 (or -8) is the blank character.


.. activecode:: chp08_index1
    
    school = "Luther College"
    m = school[2]
    print(m)
    
    lastchar = school[-1]
    print(lastchar)

The expression ``school[2]`` selects the character at index 2 from ``school``, and creates a new
string containing just this one character. The variable ``m`` refers to the result. 

The letter at index zero of ``"Luther College"`` is ``L``.  So at
position ``[2]`` we have the letter ``t``.

If you want the zero-eth letter of a string, you just put 0, or any expression
with the value 0, in the brackets.  Give it a try.

The expression in brackets is called an **index**. An index specifies a member
of an ordered collection.  In this case the collection of characters in the string. The index
*indicates* which character you want. It can be any integer
expression so long as it evaluates to a valid index value.

Note that indexing returns a *string* --- Python has no special type for a single character.
It is just a string of length 1.

**Check your understanding**

.. mchoicemf:: test_question8_2_1
   :answer_a: t
   :answer_b: h
   :answer_c: c
   :answer_d: Error, you cannot use the [ ] operator with a string.
   :correct: b
   :feedback_a: Index locations do not start with 1, they start with 0.
   :feedback_b: Yes, index locations start with 0.
   :feedback_c: s[-3] would return c, counting from right to left.
   :feedback_d: [ ] is the index operator


   What is printed by the following statements?
      
   .. code-block:: python
   
      s = "python rocks"
      print(s[3])




.. mchoicemf:: test_question8_2_2
   :answer_a: tr
   :answer_b: t0
   :answer_c: ps
   :answer_d: nn
   :answer_e: Error, you cannot use the [ ] operator with the + operator.
   :correct: b
   :feedback_a: Yes, t is at postion 2, counting left to right starting from 0; and s at -4, counting right to left starting from -1.
   :feedback_b: Almost. For -4 you count from right to left, starting with -1. 
   :feedback_c: p is at location 0, not 2.
   :feedback_d: n is at location 5, not 2.
   :feedback_e: [ ] operator returns a string that can be concatenated with another string.


   What is printed by the following statements?
   
   .. code-block:: python
   
      s = "python rocks"
      print(s[2] + s[-4])


.. note::
   Why does counting start at 0 going from left to right, but at -1 going from right to left? Well, indexing starting at 0
   has a long history in computer science having to do with some low-level implementation details that we won't
   go into. For indexing from right to left, it might seem natural to do the analgous thing
   and start at -0. Unfortunately, -0 is the same as 0, so s[-0] can't be the last item. Remember we
   said that programming languages are formal languages where details matter and
   everything is taken literally?

Operations and Strings
----------------------

Python provides many built-in computations that you can perform on strings. There
are three different ways of invoking computations on objects. In addition to
operators (like ``+`` and ``*``), there are method invocations and function invocations. You 
will first learn some specific examples. Later in the course, you will understand
all the details of the differences.

String Methods
--------------

The "dot notation" is the way we connect an object to one of its attributes or
to invoke a method on that object. There are a wide variety of methods for string objects.  
Try the following program.

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
change the original.  You can also consult the `Python documentation for strings <http://docs.python.org/2.7/library/stdtypes.html#string-methods>`_.

.. activecode:: ch08_methods1

    ss = "    Hello, World    "

    els = ss.count("l")
    print(els)

    print("***"+ss.strip()+"***")
    print("***"+ss.lstrip()+"***")
    print("***"+ss.rstrip()+"***")

    news = ss.replace("o", "***")
    print(news)


.. activecode:: ch08_methods2


    food = "banana bread"
    print(food.capitalize())

    print("*"+food.center(25)+"*")
    print("*"+food.ljust(25)+"*")     #stars added to show bounds
    print("*" +food.rjust(25)+"*")

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
      print(s[1]*s.index("n"))


.. index::
    single: len function
    single: function; len
    single: runtime error
    single: negative index
    single: index; negative

Length
------

The ``len`` function, when applied to a string, returns the number of characters in a string.

.. activecode:: chp08_len1
    
    fruit = "Banana"
    print(len(fruit))
    

To get the last letter of a string, you might be tempted to try something like
this:

.. activecode:: chp08_len2
    
    fruit = "Banana"
    sz = len(fruit)
    last = fruit[sz]       # ERROR!
    print(last)

That won't work. It causes the runtime error
``IndexError: string index out of range``. The reason is that there is no
letter at index position 6 in ``"Banana"``. 
Since we started counting at zero, the six indexes are
numbered 0 to 5. To get the last character, we have to subtract 1 from
``length``.  Give it a try in the example above.

.. activecode:: ch08_len3
    
    fruit = "Banana"
    sz = len(fruit)
    lastch = fruit[sz-1]
    print(lastch)

.. Alternatively, we can use **negative indices**, which count backward from the
.. end of the string. The expression ``fruit[-1]`` yields the last letter,
.. ``fruit[-2]`` yields the second to last, and so on.  Try it!

Typically, a Python programmer will access the last character by combining the
two lines of code from above.


.. sourcecode:: python
    
    lastch = fruit[len(fruit)-1]

**Check your understanding**

.. mchoicemf:: test_question8_4_1
   :answer_a: 11
   :answer_b: 12
   :correct: b
   :feedback_a: The blank space counts as a character.
   :feedback_b: Yes, there are 12 characters in the string.


   What is printed by the following statements?
   
   .. code-block:: python
   
      s = "python rocks"
      print(len(s))



.. mchoicemf:: test_question8_4_2
   :answer_a: o
   :answer_b: r
   :answer_c: s
   :answer_d: Error, len(s) is 12 and there is no index 12.
   :correct: b
   :feedback_a: Take a look at the index calculation again, len(s)-5.
   :feedback_b: Yes, len(s) is 12 and 12-5 is 7.  Use 7 as index and remember to start counting with 0.
   :feedback_c: s is at index 11
   :feedback_d: You subtract 5 before using the index operator so it will work.


   What is printed by the following statements?
   
   .. code-block:: python
   
      s = "python rocks"
      print(s[len(s)-5])

.. note::
   You can leave out len(s) entirely in the above expression and get the same 
   result using negative indexing (i.e., try replacing the last line with
   ``print(s[-5])``. This offers another intuition for why negative indexing
   starts at -1 rather than at -0.

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
to the m'th character, *including the first* but *excluding the last*. 
In other words,  start with the character at index n and
go up to but *do not include* the character at index m.

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


.. index:: mutable, immutable, runtime error

Strings are Immutable
---------------------

One final thing that makes strings different from some other Python collection types is that
you are not allowed to modify the individual characters in the collection.  It is tempting to use the ``[]`` operator on the left side of an assignment,
with the intention of changing a character in a string.  For example, in the following code, we would like to change the first letter of ``greeting``.

.. activecode:: cg08_imm1
    
    greeting = "Hello, world!"
    greeting[0] = 'J'            # ERROR!
    print(greeting)

Instead of producing the output ``Jello, world!``, this code produces the
runtime error ``TypeError: 'str' object does not support item assignment``.

Strings are **immutable**, which means you cannot change an existing string. The
best you can do is create a new string that is a variation on the original.

.. activecode:: ch08_imm2
    
    greeting = "Hello, world!"
    newGreeting = 'J' + greeting[1:]
    print(newGreeting)
    print(greeting)            # same as it was

The solution here is to concatenate a new first letter onto a slice of
``greeting``. This operation has no effect on the original string.

**Check your understanding**

.. mchoicemf:: test_question8_7_1
   :answer_a: Ball
   :answer_b: Call
   :answer_c: Error
   :correct: c
   :feedback_a: Assignment is not allowed with strings.
   :feedback_b: Assignment is not allowed with strings.
   :feedback_c: Yes, strings are immutable.

   What is printed by the following statements:
   
   .. code-block:: python

      s = "Ball"
      s[0] = "C"
      print(s)



.. index::
    single: in operator
    single: operator; in
    
.. _sequences-in-operator:

The ``in`` and ``not in`` operators
-----------------------------------

The ``in`` operator tests if one string is a substring of another:

.. activecode:: chp8_in1
    
    print('p' in 'apple')
    print('i' in 'apple')
    print('ap' in 'apple')
    print('pa' in 'apple')

Note that a string is a substring of itself, and the empty string is a 
substring of any other string. (Also note that computer scientists 
like to think about these edge cases quite carefully!) 

.. activecode:: chp8_in2
    
    print('a' in 'a')
    print('apple' in 'apple')
    print('' in 'a')
    print('' in 'apple')
    
The ``not in`` operator returns the logical opposite result of ``in``.

.. activecode:: chp8_in3

    print('x' not in 'apple')



.. index:: module, string module, dir function, dot notation, function type,
           docstring

Character classification
------------------------

It is often helpful to examine a character and test whether it is upper- or
lowercase, or whether it is a character or a digit. The ``string`` module
provides several constants that are useful for these purposes. One of these,
``string.digits`` is equivalent to "0123456789".  It can be used to check if a character
is a digit using the ``in`` operator.

The string ``string.ascii_lowercase`` contains all of the ascii letters that the system
considers to be lowercase. Similarly, ``string.ascii_uppercase`` contains all of the
uppercase letters. ``string.punctuation`` comprises all the characters considered
to be punctuation. You can't actually run the code below in the browser (sorry, limitation of our environment, not
*all* of python has been implemented.) But the comments indicate what would be produced; later in the
semester you'll have facilities for actually executing it.

.. activecode:: seq_char_classification
    
    print(string.ascii_lowercase)
    print(string.ascii_uppercase)
    print(string.digits)
    print(string.punctuation)
    x = "a"
    y = "A"
    print(x in string.ascii_lowercase)  # True
    print(x in string.ascii_uppercase)  # False
    print(y in string.ascii_lowercase)  # False
    print(y in string.ascii_uppercase)  # True


For more information consult the ``string`` module documentation (see `Global Module Index <http://docs.python.org/py3k/py-modindex.html>`_).


.. note::

   This workspace is provided for your convenience.  You can use this activecode window to try out anything you like.

   .. activecode:: scratch_08_04

Lists
=====

A **list** is a sequential collection of Python data values, where each value is identified by an
index. The values that make up a list are called its **elements**. Lists are
similar to strings, which are ordered collections of characters, except that the
elements of a list can have any type and for any one list, the items can be of different types.

.. index:: list

List Values
-----------

There are several ways to create a new list.  The simplest is to enclose the
elements in square brackets ( ``[`` and ``]``).

.. sourcecode:: python
    
    [10, 20, 30, 40]
    ["spam", "bungee", "swallow"]

The first example is a list of four integers. The second is a list of three
strings. As we said above, the elements of a list don't have to be the same type.  

As you would expect, we can also assign list values to variables and pass lists as parameters to functions.  


**Check your understanding**

.. mchoicemf:: test_question9_1_1 
   :answer_a: False
   :answer_b: True
   :correct: a
   :feedback_a: Yes, unlike strings, lists can consist of any type of Python data.
   :feedback_b: Lists are heterogeneous, meaning they can have different types of data.

   A list can contain only integer items.

.. index:: list index, index

List Length
-----------

As with strings, the function ``len`` returns the length of a list (the number
of items in the list).  However, since lists can have items which are themselves sequences (e.g., strings), 
it important to note that ``len`` only returns the top-most length.

.. activecode:: chp09_01a

    alist =  ["hello", 2.0, 5]
    print(len(alist))
    print(len(alist[0]))

Note that ``alist[0]`` is the string ``"hello"``, which has length 5. 

**Check your understanding**

.. mchoicemf:: test_question9_2_1 
   :answer_a: 4
   :answer_b: 5
   :correct: b
   :feedback_a: len returns the actual number of items in the list, not the maximum index value.
   :feedback_b: Yes, there are 5 items in this list.

   What is printed by the following statements?
   
   .. code-block:: python

     alist = [3, 67, "cat", 3.14, False]
     print(len(alist))
   
   
Accessing Elements
------------------

The syntax for accessing the elements of a list is the same as the syntax for
accessing the characters of a string.  We use the index operator ( ``[]`` -- not to
be confused with an empty list). The expression inside the brackets specifies
the index. Remember that the indices start at 0.  Any integer expression can be used
as an index and as with strings, negative index values will locate items from the right instead
of from the left.

Try to predict what will be printed out by the following code, and then run it to check your
prediction. (Actually, it's a good idea to always do that with the code examples. You 
will learn much more if you force yourself to make a prediction before you see the output.)

.. activecode:: chp09_02
    
    numbers = [17, 123, 87, 34, 66, 8398, 44]
    print(numbers[2])
    print(numbers[9-8])
    print(numbers[-2])
    print(numbers[len(numbers)-1])
    
  
List Membership
---------------

``in`` and ``not in`` are boolean operators that test membership in a sequence. We
used them previously with strings and they also work here.

.. activecode:: chp09_4
    
    fruit = ["apple","orange","banana","cherry"]

    print("apple" in fruit)
    print("pear" in fruit)

**Check your understanding**

.. mchoicemf:: test_question9_4_1
   :answer_a: True
   :answer_b: False
   :correct: a
   :feedback_a: Yes, 'cat' is an item in the list alist.
   :feedback_b: There are 5 items in the list, 'cat' is one of them. 
   
   What is printed by the following statements?
   
   .. code-block:: python

     alist = [3, 67, "cat", 3.14, False]
     print("cat" in alist)


.. mchoicemf:: test_question9_4_2
   :answer_a: True
   :answer_b: False
   :correct: b
   :feedback_a: "at" is in "cat", but it is not in alist
   :feedback_b: Yes, "at" is not in the top level item, alist.  It is in one of the elements of alist.
   
   What is printed by the following statements?
   
   .. code-block:: python

     alist = [3, 67, "cat", 3.14, False]
     print("at" in alist)



Concatenation and Repetition
----------------------------

Again, as with strings, the ``+`` operator concatenates lists.  
Similarly, the ``*`` operator repeats the items in a list a given number of times.

.. activecode:: chp09_5

    fruit = ["apple","orange","banana","cherry"]
    print([1,2] + [3,4])
    print(fruit+[6,7,8,9])

    print([0] * 4)


It is important to see that these operators create new lists from the elements of the operand lists.  
If you concatenate a list with 2 items and a list with 4 items, you will get a new list with 6 items 
(not a list with two sublists).  Similarly, repetition of a list of 2 items 4 times will give a list 
with 8 items.

One way for us to make this more clear is to run a part of this example in codelens.  
As you step thru the code, you will see the variables being created and the lists that they refer to.  
Pay particular attention to the fact that when ``newlist`` is created by the statement 
``newlist = fruit + numlist``, it refers to a completely new list formed by making copies of the items from ``fruit`` and ``numlist``.  You can see this very clearly in the codelens object diagram.  The objects are different.



.. codelens:: chp09_concatid

    fruit = ["apple","orange","banana","cherry"]
    numlist = [6,7]

    newlist = fruit + numlist

    zeros = [0] * 4


**Check your understanding**

.. mchoicemf:: test_question9_5_1
   :answer_a: 6
   :answer_b: [1,2,3,4,5,6]
   :answer_c: [1,3,5,2,4,6]
   :answer_d: [3,7,11]
   :correct: c
   :feedback_a: Concatenation does not add the lengths of the lists.
   :feedback_b: Concatenation does not reorder the items. 
   :feedback_c: Yes, a new list with all the items of the first list followed by all those from the second.
   :feedback_d: Concatenation does not add the individual items.
   
   What is printed by the following statements?
   
   .. code-block:: python

     alist = [1,3,5]
     blist = [2,4,6]
     print(alist + blist)

   
   
.. mchoicemf:: test_question9_5_2
   :answer_a: 9
   :answer_b: [1,1,1,3,3,3,5,5,5]
   :answer_c: [1,3,5,1,3,5,1,3,5]
   :answer_d: [3,9,15]
   :correct: c
   :feedback_a: Repetition does not multiply the lengths of the lists.  It repeats the items.
   :feedback_b: Repetition does not repeat each item individually.
   :feedback_c: Yes, the items of the list are repeated 3 times, one after another.
   :feedback_d: Repetition does not multiply the individual items.
   
   What is printed by the following statements?
   
   .. code-block:: python

     alist = [1,3,5]
     print(alist * 3)

   

List Slices
-----------

The slice operation we saw with strings also work on lists.  Remember that the first index is the starting point for the slice and the second number is one index past the end of the slice (up to but not including that element).  Recall also
that if you omit the first index (before the colon), the slice starts at the
beginning of the sequence. If you omit the second index, the slice goes to the
end of the sequence.

.. activecode:: chp09_6
    
    a_list = ['a', 'b', 'c', 'd', 'e', 'f']
    print(a_list[1:3])
    print(a_list[:4])
    print(a_list[3:])
    print(a_list[:])

**Check your understanding**

.. mchoicemf:: test_question9_6_1
   :answer_a: [ [ ], 3.14, False]
   :answer_b: [ [ ], 3.14]
   :answer_c: [ [56, 57, "dog"], [ ], 3.14, False]
   :correct: a
   :feedback_a: Yes, the slice starts at index 4 and goes up to and including the last item.
   :feedback_b: By leaving out the upper bound on the slice, we go up to and including the last item.
   :feedback_c: Index values start at 0.
   
   What is printed by the following statements?
   
   .. code-block:: python
   
     alist = [3, 67, "cat", [56, 57, "dog"], [ ], 3.14, False]
     print(alist[4:])



.. index:: mutable, item assignment, immutable
    
Lists are Mutable
-----------------

Unlike strings, lists are **mutable**.  This means we can change an item in a list by accessing
it directly as part of the assignment statement. Using the indexing operator (square brackets) on the left side of an assignment, we can
update one of the list items.

.. activecode:: ch09_7
    
    fruit = ["banana", "apple", "cherry"]
    print(fruit)

    fruit[0] = "pear"
    fruit[-1] = "orange"
    print(fruit)


An
assignment to an element of a list is called **item assignment**. Item
assignment does not work for strings.  Recall that strings are immutable.

Here is the same example in codelens so that you can step thru the statements and see the changes to the list elements.

.. codelens:: item_assign
    
    fruit = ["banana", "apple", "cherry"]

    fruit[0] = "pear"
    fruit[-1] = "orange"



By combining assignment with the slice operator we can update several elements at once.

.. activecode:: ch09_8
    
    alist = ['a', 'b', 'c', 'd', 'e', 'f']
    alist[1:3] = ['x', 'y']
    print(alist)

We can also remove elements from a list by assigning the empty list to them.

.. activecode:: ch09_9
    
    alist = ['a', 'b', 'c', 'd', 'e', 'f']
    alist[1:3] = []
    print(alist)

We can even insert elements into a list by squeezing them into an empty slice at the
desired location.

.. activecode:: ch09_10
    
    alist = ['a', 'd', 'f']
    alist[1:1] = ['b', 'c']
    print(alist)
    alist[4:4] = ['e']
    print(alist)


**Check your understanding**

.. mchoicemf:: test_question9_7_1
   :answer_a: [4,2,True,8,6,5]
   :answer_b: [4,2,True,6,5]
   :answer_c: Error, it is illegal to assign
   :correct: b
   :feedback_a: Item assignment does not insert the new item into the list.
   :feedback_b: Yes, the value True is placed in the list at index 2.  It replaces 8.
   :feedback_c: Item assignment is allowed with lists.  Lists are mutable.
   
   What is printed by the following statements?
   
   .. code-block:: python

     alist = [4,2,8,6,5]
     alist[2] = True
     print(alist)


.. index:: del statement, statement; del

List Deletion
-------------

Using slices to delete list elements can be awkward and therefore error-prone.
Python provides an alternative that is more readable.
The ``del`` statement removes an element from a list by using its position.

.. activecode:: ch09_11
    
    a = ['one', 'two', 'three']
    del a[1]
    print(a)

    alist = ['a', 'b', 'c', 'd', 'e', 'f']
    del alist[1:5]
    print(alist)

As you might expect, ``del`` handles negative indices and causes a runtime
error if the index is out of range.
In addition, you can use a slice as an index for ``del``.
As usual, slices select all the elements up to, but not including, the second
index.


.. note::

    This workspace is provided for your convenience.  You can use this activecode window to try out anything you like.

    .. activecode:: scratch_09_01




.. index:: is operator, objects and values

Objects and References
----------------------

If we execute these assignment statements,

.. sourcecode:: python
    
    a = "banana"
    b = "banana"

we know that ``a`` and ``b`` will refer to a string with the letters
``"banana"``. But we don't know yet whether they point to the *same* string.

There are two possible ways the Python interpreter could arrange its internal states:

.. image:: Figures/refdiag1.png
   :alt: List illustration 

or


.. image:: Figures/refdiag2.png
   :alt: List illustration

In one case, ``a`` and ``b`` refer to two different string objects that have the same
value. In the second case, they refer to the same object. Remember that an object is something a variable can
refer to.

We can test whether two names refer to the same object using the *is*
operator.  The *is* operator will return true if the two references are to the same object.  In other words, the references are the same.  Try our example from above.

.. activecode:: chp09_is1

    a = "banana"
    b = "banana"

    print(a is b)

The answer is ``True``.  This tells us that both ``a`` and ``b`` refer to the same object, and that it
is the second of the two reference diagrams that describes the relationship. 
Since strings are *immutable*, Python optimizes resources by making two names
that refer to the same string value refer to the same object.

This is not the case with lists.  Consider the following example.  Here, ``a`` and ``b`` refer to two different lists, each of which happens to have the same element values.

.. activecode:: chp09_is2
    
    a = [81,82,83]
    b = [81,82,83]

    print(a is b)

    print(a == b)  

The reference diagram for this example looks like this:

.. image:: Figures/refdiag3.png
   :alt: Reference diagram for equal different lists 

``a`` and ``b`` have the same value but do not refer to the same object.

There is one other important thing to notice about this reference diagram.  The variable ``a`` is a reference to a **collection of references**.  Those references actually refer to the integer values in the list.  In other words, a list is a collection of references to objects.  Interestingly, even though ``a`` and ``b`` are two different lists (two different collections of references), the integer object ``81`` is shared by both.  Like strings, integers are also immutable so Python optimizes and lets everyone share the same object.

Here is the example in codelens.  Pay particular attention to the `id` values.

.. codelens:: chp09_istrace
    :showoutput:
    
    a = [81,82,83]
    b = [81,82,83]

    print(a is b)
    print(a == b)

.. index:: aliases

Aliasing
--------

Since variables refer to objects, if we assign one variable to another, both
variables refer to the same object:

.. activecode:: listalias1
    
    a = [81, 82, 83]
    b = a
    print(a is b)
    
In this case, the reference diagram looks like this:

.. image:: Figures/refdiag4.png
   :alt: State snapshot for multiple references (aliases) to a list 

Because the same list has two different names, ``a`` and ``b``, we say that it
is **aliased**. Changes made with one alias affect the other.  In the codelens example below, you can see that ``a`` and ``b`` refer
to the same list after executing the assignment statement ``b = a``.


.. codelens:: chp09_is3
    :showoutput:
    
    a = [81,82,83]
    b = [81,82,83]

    print(a == b)
    print(a is b)

    b = a
    print(a == b)
    print(a is b)

    b[0] = 5
    print(a)
    


Although this behavior can be useful, it is sometimes unexpected or
undesirable. In general, it is safer to avoid aliasing when you are working
with mutable objects. Of course, for immutable objects, there's no problem.
That's why Python is free to alias strings and integers when it sees an opportunity to
economize.

**Check your understanding**

.. mchoicemf:: test_question9_10_1
   :answer_a: [4,2,8,6,5]
   :answer_b: [4,2,8,999,5]
   :correct: b
   :feedback_a: blist is not a copy of alist, it is a reference to the list alist refers to.
   :feedback_b: Yes, since alist and blist both reference the same list, changes to one also change the other.
   
   What is printed by the following statements?
   
   .. code-block:: python

     alist = [4,2,8,6,5]
     blist = alist
     blist[3] = 999
     print(alist)


.. index:: clone

Cloning Lists
-------------

If we want to modify a list and also keep a copy of the original, we need to be
able to make a copy of the list itself, not just the reference. This process is
sometimes called **cloning**, to avoid the ambiguity of the word copy.

The easiest way to clone a list is to use the slice operator.

Taking any slice of ``a`` creates a new list. In this case the slice happens to
consist of the whole list.

.. codelens:: chp09_is4
    :showoutput:
    
    a = [81,82,83]

    b = a[:]       # make a clone using slice
    print(a == b)
    print(a is b)

    b[0] = 5

    print(a)
    print(b)

Now we are free to make changes to ``b`` without worrying about ``a``.  Again, we can clearly see in codelens that ``a`` and ``b`` are entirely different list objects.



**Check your understanding**

.. mchoicemf:: test_question9_12_1
   :answer_a: [4,2,8,999,5,4,2,8,6,5]
   :answer_b: [4,2,8,999,5]
   :answer_c: [4,2,8,6,5]
   :correct: c
   :feedback_a: print(alist) not print(blist)
   :feedback_b: blist is changed, not alist.
   :feedback_c: Yes, alist was unchanged by the assignment statement. blist was a copy of the references in alist.
   
   What is printed by the following statements?
   
   .. code-block:: python

     alist = [4,2,8,6,5]
     blist = alist * 2
     blist[3] = 999
     print(alist)


.. index:: list; append

List Methods
------------

The dot operator can also be used to access built-in methods of list objects.  
``append`` is a list method which adds the argument passed to it to the end of
the list. Continuing with this example, we show several other list methods.  Many of them are
easy to understand.  

.. activecode:: chp09_meth1

    mylist = []
    mylist.append(5)
    mylist.append(27)
    mylist.append(3)
    mylist.append(12)
    print(mylist)

    mylist.insert(1, 12)
    print(mylist)
    print(mylist.count(12))

    print(mylist.index(3))
    print(mylist.count(5))

    mylist.reverse()
    print(mylist)

    mylist.sort()
    print(mylist)

    mylist.remove(5)
    print(mylist)

    lastitem = mylist.pop()
    print(lastitem)
    print(mylist)

There are two ways to use the ``pop`` method.  The first, with no parameter, will remove and return the
last item of the list.  If you provide a parameter for the position, ``pop`` will remove and return the
item at that position.  Either way the list is changed.

The following table provides a summary of the list methods shown above.  The column labeled
`result` gives an explanation as to what the return value is as it relates to the new value of the list.  The word
**mutator** means that the list is changed by the method but nothing is returned (actually ``None`` is returned).  A **hybrid** method is one that not only changes the list but also returns a value as its result.  Finally, if the result is simply a return, then the list
is unchanged by the method.

Be sure
to experiment with these methods to gain a better understanding of what they do.




==========  ==============  ============  ================================================
Method      Parameters       Result       Description
==========  ==============  ============  ================================================
append      item            mutator       Adds a new item to the end of a list
insert      position, item  mutator       Inserts a new item at the position given
pop         none            hybrid        Removes and returns the last item
pop         position        hybrid        Removes and returns the item at position
sort        none            mutator       Modifies a list to be sorted
reverse     none            mutator       Modifies a list to be in reverse order
index       item            return idx    Returns the position of first occurrence of item
count       item            return ct     Returns the number of occurrences of item
remove      item            mutator       Removes the first occurrence of item
==========  ==============  ============  ================================================


Details for these and others
can be found in the `Python Documentation <http://docs.python.org/py3k/library/stdtypes.html#sequence-types-str-bytes-bytearray-list-tuple-range>`_.

It is important to remember that methods like ``append``, ``sort``, 
and ``reverse`` all return ``None``.  They change the list; they don't produce a new list.
So, while we did reassignment to increment a number, as in ``x = x + 1``, doing the 
analogous thing with these operations will lose the entire list contents (see line 8 below).



.. activecode:: chp09_meth2

    mylist = []
    mylist.append(5)
    mylist.append(27)
    mylist.append(3)
    mylist.append(12)
    print(mylist)

    mylist = mylist.sort()   #probably an error
    print(mylist)

**Check your understanding**

.. mchoicemf:: test_question9_13_1
   :answer_a: [4,2,8,6,5,False,True]
   :answer_b: [4,2,8,6,5,True,False]
   :answer_c: [True,False,4,2,8,6,5]
   :correct: b
   :feedback_a: True was added first, then False was added last.
   :feedback_b: Yes, each item is added to the end of the list.
   :feedback_c: append adds at the end, not the beginning.
   
   What is printed by the following statements?
   
   .. code-block:: python

     alist = [4,2,8,6,5]
     alist.append(True)
     alist.append(False)
     print(alist)



.. mchoicemf:: test_question9_13_2
   :answer_a: [False,4,2,True,8,6,5]
   :answer_b: [4,False,True,2,8,6,5]
   :answer_c: [False,2,True,6,5]
   :correct: a
   :feedback_a: Yes, first True was added at index 2, then False was added at index 0.
   :feedback_b: insert will place items at the index position specified and move everything down to the right.
   :feedback_c: insert does not remove anything or replace anything.
   
   What is printed by the following statements?
   
   .. code-block:: python

     alist = [4,2,8,6,5]
     alist.insert(2,True)
     alist.insert(0,False)
     print(alist)


.. mchoicemf:: test_question9_13_3
   :answer_a: [4,8,6]
   :answer_b: [2,6,5]
   :answer_c: [4,2,6]
   :correct: c
   :feedback_a: pop(2) removes the item at index 2, not the 2 itself.
   :feedback_b: pop() removes the last item, not the first.
   :feedback_c: Yes, first the 8 was removed, then the last item, which was 5.
   
   What is printed by the following statements?
   
   .. code-block:: python

     alist = [4,2,8,6,5]
     temp = alist.pop(2)
     temp = alist.pop()
     print(alist)

   
   
.. mchoicemf:: test_question9_13_4
   :answer_a: [2,8,6,5]
   :answer_b: [4,2,8,6,5]
   :answer_c: 4
   :answer_d: None
   :correct: c
   :feedback_a: alist is now the value that was returned from pop(0).
   :feedback_b: pop(0) changes the list by removing the first item.
   :feedback_c: Yes, first the 4 was removed from the list, then returned and assigned to alist.  The list is lost.
   :feedback_d: pop(0) returns the first item in the list so alist has now been changed.
   
   What is printed by the following statements?
   
   .. code-block:: python

     alist = [4,2,8,6,5]
     alist = alist.pop(0)
     print(alist)



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
         
         print w 
   
