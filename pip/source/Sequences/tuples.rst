..  Copyright (C)  Paul Resnick, Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

..  shortname:: Tuples
..  description:: Tuples as immutable sequences, as a way to return multiple values.

.. qnum::
   :prefix: tuples-
   :start: 1
   
.. _tuples_chap:

.. index::
    single: tuples
    single: tuples; mutability
    single: mutability; tuples
    
Tuples
------

So far you have seen two types of sequential collections: strings, which are made up of
characters; and lists, which are made up of elements of any type.  One of the
differences we noted is that the elements of a list can be modified, but the
characters in a string cannot. In other words, strings are **immutable** and
lists are **mutable**.

A **tuple**, like a list, is a sequence of items of any type. Unlike lists,
however, tuples are immutable.  The printed representation of a tuple is a comma-separated 
sequence of values, enclosed in parentheses. In other words, the representation
is just like lists, except with parentheses () instead of square brackets [].

One way to create a tuple is to write an expression, enclosed in parentheses,
that consists of multiple other expressions, separated by commas.

.. sourcecode:: python

    julia = ("Julia", "Roberts", 1967, "Duplicity", 2009, "Actress", "Atlanta, Georgia")

Tuples are useful for representing what other languages often call *records* ---
some related information that belongs together, like your student record.  There is
no description of what each of these *fields* means, but we can guess.  A tuple
lets us "chunk" together related information and use it as a single thing.

Tuples support the same sequence operations as strings and
lists. 
For example, the index operator selects an element from a tuple.

As with strings, if we try to use item assignment to modify one of the elements of the
tuple, we get an error.

.. sourcecode:: python

    julia[0] = 'X'
    TypeError: 'tuple' object does not support item assignment

Of course, even if we can't modify the elements of a tuple, we can make a variable
reference a new tuple holding different information.  To construct the new tuple,
it is convenient that we can slice parts of the old tuple and join up the
bits to make the new tuple.  So ``julia`` has a new recent film, and we might want
to change her tuple.  We can easily slice off the parts we want and concatenate them with
the new tuple.

.. activecode:: ch09_tuple1


    julia = ("Julia", "Roberts", 1967, "Duplicity", 2009, "Actress", "Atlanta, Georgia")
    print(julia[2])
    print(julia[2:6])

    print(len(julia))

    julia = julia[:3] + ("Eat Pray Love", 2010) + julia[5:]
    print(julia)


To create a tuple with a single element (but you're probably not likely
to do that too often), we have to include the final comma, because without
the final comma, Python treats the ``(5)`` below as an integer in parentheses:

.. activecode:: chp09_tuple2

    tup = (5,)
    print(type(tup))

    x = (5)
    print(type(x))
 

.. index::
    single: assignment; tuple 
    single: tuple; assignment  

Tuple Packing
-------------

Wherever python expects a single value, if multiple expressions are provided, separated
by commas, they are automatically **packed** into a tuple. For example, we could
have omitted the parentheses when first assigning a tuple to the variable julia.

.. sourcecode:: python

    julia = ("Julia", "Roberts", 1967, "Duplicity", 2009, "Actress", "Atlanta, Georgia")
    # or equivalently
    julia = "Julia", "Roberts", 1967, "Duplicity", 2009, "Actress", "Atlanta, Georgia"
    

.. index::
    single: tuple; return value 

**Check your understanding**

.. mchoicema:: test_questiontuples_1
   :answer_a: print(julia['city'])
   :answer_b: print(julia[-1])
   :answer_c: print(julia(-1))
   :answer_d: print(julia(6))
   :answer_e: print(julia[7])
   :correct: b
   :feedback_a: julia is a tuple, not a dictionary; indexes must be integers
   :feedback_b: [-1] picks out the last item in the sequence
   :feedback_c: Index into tuples using square brackets. julia(-1) will try to treat julia as a function call, with -1 as the parameter value.
   :feedback_d: Index into tuples using square brackets. julia(-1) will try to treat julia as a function call, with -1 as the parameter value.
   :feedback_e: Indexing starts at 0. You want the seventh item, which is julia[6]

   Which of the following statements will output Atlanta, Georgia

Tuples as Return Values
-----------------------

Functions can return tuples as return values. This is very useful --- we often want to
know some batsman's highest and lowest score, or we want to find the mean and the standard 
deviation, or we want to know the year, the month, and the day, or if we're doing some
some ecological modeling we may want to know the number of rabbits and the number
of wolves on an island at a given time.  In each case, a function (which 
can only return a single value), can create a single tuple holding multiple elements. 

For example, we could write a function that returns both the area and the circumference
of a circle of radius r.

.. activecode:: chp09_tuple3

    
    def circleInfo(r):
        """ Return (circumference, area) of a circle of radius r """
        c = 2 * 3.14159 * r
        a = 3.14159 * r * r
        return (c, a)

    print(circleInfo(10))

Again, we can take advantage of packing to make the code look a little more readable on line 4

.. activecode:: chp09_tuple3a

    
    def circleInfo(r):
        """ Return (circumference, area) of a circle of radius r """
        c = 2 * 3.14159 * r
        a = 3.14159 * r * r
        return c, a

    print(circleInfo(10))




Tuple Assignment with unpacking
-------------------------------

Python has a very powerful **tuple assignment** feature that allows a tuple of variable names 
on the left of an assignment to be assigned values from a tuple
on the right of the assignment. Another ay to think of this is that the tuple of values
is **unpacked** into the variable names.

.. sourcecode:: python

    (name, surname, birth_year, movie, movie_year, profession, birth_place) = julia

This does the equivalent of seven assignment statements, all on one easy line.  
One requirement is that the number of variables on the left must match the number
of elements in the tuple. 

Once in a while, it is useful to swap the values of two variables.  With
conventional assignment statements, we have to use a temporary variable. For
example, to swap ``a`` and ``b``:

.. sourcecode:: python

    temp = a
    a = b
    b = temp

Tuple assignment solves this problem neatly:

.. sourcecode:: python

    (a, b) = (b, a)

The left side is a tuple of variables; the right side is a tuple of values.
Each value is assigned to its respective variable. All the expressions on the
right side are evaluated before any of the assignments. This feature makes
tuple assignment quite versatile.

Naturally, the number of variables on the left and the number of values on the
right have to be the same.

.. sourcecode:: python

    >>> (a, b, c, d) = (1, 2, 3)
    ValueError: need more than 3 values to unpack 

Python even provides a way to pass a single tuple to a function and have it be
unpacked for assignment to the named parameters. 

.. activecode:: cp09_tuple4

    def add(x, y):
        return x + y
        
    print(add(3, 4))
    z = (5, 4)
    print(add(*z)) # this line will cause the values to be unpacked
    print(add(z)) # this line causes an error

If you run this, you will be get an error caused by line 7, where it says that
the function add is expecting two parameters, but you're only passing one parameter
(a tuple). In line 6 you'll see that the tuple is unpacked and 5 is bound to x, 4 to y. 

Don't worry about mastering this idea yet. But later in the course, if you come
across some code that someone else has written that uses the * notation inside
a parameter list, come back and look at this again.

.. mchoicema:: test_questiontuples_2
   :answer_a: Make the last two lines of the function be "return x" and "return y"  
   :answer_b: Include the statement "return [x, y]" 
   :answer_c: Include the statement "return (x, y)"
   :answer_d: Include the statement "return x, y"
   :answer_e: It's not possible to return two values; make two functions that each compute one value.
   :correct: b,c,d
   :feedback_a: As soon as the first return statement is executed, the function exits, so the second one will never be executed; only x will be returned
   :feedback_b: return [x,y] is not the preferred method because it returns x and y in a list and you would have to manually unpack the values. But it is workable.
   :feedback_c: return (x, y) returns a tuple.
   :feedback_d: return x, y causes the two values to be packed into a tuple.
   :feedback_e: It is possible, and frequently useful, to have one function compute multiple values.

   If you want a function to return two values, contained in variables x and y, which of the following methods will work?

.. mchoicemf:: test_questiontuples_3
   :answer_a: You can't use different variable names on the left and right side of an assignment statement.
   :answer_b: At the end, x still has it's original value instead of y's original value.
   :answer_c: Actually, it works just fine!
   :correct: b
   :feedback_a: Sure you can; you can use any variable on the right-hand side that already has a value.
   :feedback_b: Once you assign x's value to y, y's original value is gone
   :feedback_c: Once you assign x's value to y, y's original value is gone

   Consider the following alternative way to swap the values of variables x and y. What's wrong with it?
   
   .. code-block:: python 
        
        # assume x and y already have values assigned to them
        y = x
        x = y   


Unpacking Dictionary Items
--------------------------

A dictionary consists of key-value pairs. When you call the items() method on 
a dictionary, you get back a list of key-value pairs. Each of those pairs is a
two-item tuple. (More generally, we refer to any two-item tuple as a **pair**).
You can iterate the key-value pairs.

.. activecode:: cp_09_tuple5

    d = {"k1": 3, "k2": 7, "k3": "some other value"}
    
    for p in d.items():
        print p[1]
        
Each time line 4 is executed, p will refer to one key-value pair from d. A pair is just
a tuple, so p[0] refers to the key and p[1] refers to the value.

That code is easier to read if we unpacked to the key-value pairs into 
two variable names.

.. activecode:: cp_09_tuple6

    d = {"k1": 3, "k2": 7, "k3": "some other value"}
    
    for (k, v) in d.items():
        print v

More generally, if you have a list of tuples that each has more than two items, and you iterate through
them with a for loop pulling out information from the tuples, the code will be far more readable if you unpack them
into separate variable names.

Glossary
--------

.. glossary::


    tuple
        A type of sequence, much like a list but immutable. A tuple is created
        by enclosing one or more values in parentheses, separated by commas.

    packing
        When multiple values are specified, separated by commas, they are
        packed into a tuple.
        
    unpacking
        When a tuple is assigned to a collection of variable names separated
        by commas, the tuple is unpacked and the separate values are assigned to each 
        of the variables.
        
    pair
        A tuple with exactly two items.
        
Exercises
---------

1. Fill in the left side of line 7 so that the following code runs without error

.. actex:: ex_tuples_1

    def circleInfo(r):
        """ Return (circumference, area) of a circle of radius r """
        c = 2 * 3.14159 * r
        a = 3.14159 * r * r
        return c, a

    #fill in this = circleInfo(10) 
    print("area is " + str(area))
    print("circumference is " + str(circ))

#. Use a for loop to print out the last name, year of birth, and city for each of the people

.. actex:: ex_tuples_2

    julia = ("Julia", "Roberts", 1967, "Duplicity", 2009, "Actress", "Atlanta, Georgia")
    claude = ("Claude", "Shannon", 1916, "A Mathematical Theory of Communication", 1948, "Mathematician", "Petoskey, Michigan")
    alan = ("Alan", "Turing", 1912, "Computing machinery and intelligence", 1950, "Mathematician", "London, England")
    
    people = [julia, claude, alan]
    
    
  