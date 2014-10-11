..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Anonymous functions with lambda expressions
-------------------------------------------

To further drive home the idea that we are passing a function object as a parameter
to the sorted object, let's see an alternative notation for creating a function,
a **lambda expression**. The syntax of a lambda expression is the word "lambda" followed
by parameter names, separated by commas but not inside (parentheses), followed 
by a colon and then an expression. ``lambda arguments: expression`` yields a function object. 
This unnamed object behaves like a function object defined with  

.. sourcecode:: python

    def fname(arguments):
        return expression
        
Consider the following code

.. activecode:: sort_7

    def f(x):
        return x - 1
    
    print f
    print type(f)
    print f(3)
    
    print lambda x: x-2
    print type(lambda x: x-2)
    print (lambda x: x-2)(6)
    
Note the paralells between the two. At line 4, f is bound to a function object. Its printed representation
is "<function f>". At line 8, the lambda expression produces a function object. Because it is
unnamed (anonymous), its printed representation doesn't include a name for it, "<function <lambda>>". Both are of type
'function'.

A function, whether named or anonymous, can be called by placing parentheses () after it.
In this case, because there is one parameter, there is one value in parentheses. This
works the same way for the named function and the anonymous function produced by the lambda
expression. The lambda expression had to go in parentheses just for the purposes
of grouping all its contents together. Without the extra parentheses around it on line 10, 
the interpreter would group things differently and make a function of x that returns x - 2(6).

Some students find it more natural to work with lambda expressions than to refer to a function
by name. Others find the syntax of lambda expressions confusing. It's up to you
which version you want to use. In all the examples below, both ways of doing it will
be illustrated.

Below, sorting on absolute value has been rewritten using lambda notation and the built-in function abs.

.. activecode:: sort_8

    L1 = [1, 7, 4, -2, 3]
    
    print "About to call sorted"
    L2 = sorted(L1, key=lambda x: abs(x))
    print "Finished execution of sorted"
    print L2

Of course, it's unnecessary to make an anonymous function that takes an input and just calls an existing function on it. That's equivalent to just providing the existing function as a lambda expression. You may find, however, that the lambda expression above helps you understand what sorted does with the function that is passed in: it calls the function on each of the items in the list that is passed to sorted. Make sure you understand why the code above and the code immediately below cause the list to be sorted the same way. 

.. activecode:: sort_8a  

    L1 = [1, 7, 4, -2, 3]
    
    print "About to call sorted"
    L2 = sorted(L1, key=abs)
    print "Finished execution of sorted"
    print L2


.. mchoicemf:: test_questionsort_1
   :answer_a: descending order, from 7 down to -2
   :answer_b: ascending order, from -2 up to 7
   :answer_c: the original order of L1
   :correct: a
   :feedback_a: 7 is decorated with -7, so it is first; -2 is decorated with 2, so it is last 
   :feedback_b: -x produces the negative of x
   :feedback_c: sorted changes the order

   Describe what the sort order will be for this.
   
   .. code-block:: python 

    L1 = [1, 7, 4, -2, 3]
     
    print sorted(L1, key = lambda x: -x)

.. mchoicemf:: test_questionsort_2
   :answer_a: descending order, from 7 down to -2
   :answer_b: ascending order, from -2 up to 7
   :answer_c: the original order of L1
   :correct: b
   :feedback_a: The True value for the reverse parameter says to reverse the order 
   :feedback_b: The True value for the reverse parameter says to reverse the order
   :feedback_c: sorted changes the order

   Describe what the sort order will be for this.
   
   .. code-block:: python 

    L1 = [1, 7, 4, -2, 3]
     
    print sorted(L1, key = lambda x: -x, reverse = True)

