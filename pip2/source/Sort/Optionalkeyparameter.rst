..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Optional key parameter
----------------------

If you want to sort things in some order other than the "natural" or or its reverse,
you can provide an additional parameter, the key parameter. For example, suppose
you want to sort a list of numbers based on their absolute value, so that -4 comes after 3?
Or suppose you have a dictionary with strings as the keys and numbers as the values. Instead
of sorting them in alphabetic order based on the keys, you might like to sort them in
order based on their values.

First, let's see an example, and then we'll dive into how it works.

First, let's define a function absolute that takes a number and returns its
absolute value. (Actually, python provides a built-in function ``abs`` that does
this, but we are going to define our own, for reasons that will be explained
in a minute.)

.. activecode:: sort_4

    L1 = [1, 7, 4, -2, 3]

    def absolute(x):
        if x >= 0:
            return x
        else:
            return -x
            
    print absolute(3)
    print absolute(-119)
    
    for y in L1:
        print absolute(y)
        

Now, we can pass the absolute function to L1 in order to specify that we want
the items sorted in order of their absolute value, rather than in order of 
their actual value.

.. activecode:: sort_5

    L1 = [1, 7, 4, -2, 3]
     
    def absolute(x):
        if x >= 0:
            return x
        else:
            return -x
            
    L2 = sorted(L1, key=absolute)
    print L2
    
    #or in reverse order
    print sorted(L1, reverse = True, key = absolute) 
     
What's really going on there? We've done something pretty strange. Before, all the
values we have passed as parameters have been pretty easy to understand: numbers, strings,
lists, Booleans, dictionaries. Here we have passed a function object: absolute
is a variable name whose value is the function. When we pass that function object,
it is *not* automatically invoked. Instead, it is just bound to the formal parameter
key of the function sorted.

We are not going to look at the source code for the built-in function sorted. But if
we did, we would find somewhere in its code a parameter named key with a default value of None. When a value is provided for that parameter in an invocation of the function sorted, it has to be a function. What the sorted function
does is call that key function once for each item in the list that's getting sorted.
It associates the result returned by that function (the absolute function in our case)
with the original value. Think of those associated values as being little post-it notes
that decorate the original values. The value 4 has a post-it note that says 4 on it,
but the value -2 has a post-it note that says 2 on it. Then the sorted function
rearranges the original items in order of the values written on their associated post-it notes.

To illustrate that the absolute function is invoked once on each item, during the execution
of sorted, I have added some print statements into the code.

.. activecode:: sort_6

    L1 = [1, 7, 4, -2, 3]
     
    def absolute(x):
        print "--- figuring out what to write on the post-it note for " + str(x)
        if x >= 0:
            return x
        else:
            return -x
    
    print "About to call sorted"
    L2 = sorted(L1, None, absolute)
    print "Finished execution of sorted"
    print L2

Note that this code never explicitly calls the absolute function at all. It passes
the absolute function as a parameter value to the sorted function. Inside the 
sorted function, whose code we haven't seen, that function gets invoked.

.. note::

   It is a little confusing that we are reusing the word *key* so many times. The name of the optional parameter is ``key``. We will usually pass a parameter value using the keyword parameter passing mechanism (see :ref:`chapter <keyword_pararams_chap>` to review). When we write ``key = some_function`` in the function invocation, the word key is there because it is the name of the parameter, specified in the definition of the sort function, not because we are using keyword-based parameter passing.