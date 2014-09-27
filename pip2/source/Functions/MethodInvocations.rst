..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Method Invocations
------------------

.. note:

   This section is a review of material you have already seen, but it may be helpful to look at it again now that you're focusing on functions and function calls.

There is one other special type of function called a **method**, which is invoked slightly differently. Some
object types have methods defined for them. You have already seen some methods that operate on strings (e.g., ``find``, ``index``, ``split``, ``join``) and on 
lists (e.g., ``append``, ``pop``). 

We will not learn about how define methods until later 
in the course, when we cover Classes. But it's worth getting a basic understanding now
of how methods are invoked. To invoke a method, the syntax is ``<expr>.<methodname>(<additional parameter values>)``.

The expression to the left of the dot should evaluate to an object of the right type, an object
for which <methodname> is defined. The method will be applied to that object (that object
will be a parameter value passed to the function/method.) If the method takes additional parameters (some do, some don't),
additional expressions that evaluate to values are included inside the parentheses.

For example, let's look at an invocation of the split method.

.. activecode:: functions2_1

   y = "This is a sentence"
   z = y.split()
   print type(z)
   print len(z)
   print z
   for w in z:
      print w
      
The split method operates on a string. Because it is a method rather than a
regular function, the string it operates on appears to the left of the period, 
rather than inside the parentheses. The split method always returns a list.
On line 2, that returned value is assigned to the variable z.

The split method actually takes an optional extra parameter. If no value is provided
inside the parentheses, the split method chops up the list whenever it encounters
and whitespace (a space, a tab, or a newline). But you can specifying a character
or character string to split on. Try putting "s" inside the parentheses on line 2
above, make a prediction about what the output will be, and then check it. Try
some other things inside the parentheses.

Note that the thing to the left of the period can be any expression, not just a variable name.
It can even be a return value from some other function call or method invocation. For
example, if we want to remove the s and t characters from a string, we can do it all on
one line as show below.

.. activecode:: functions2_2

   print "This is a sentence".replace("s", "").replace("t", "")
 
What's going on there? Start reading left to right. "This is a sentence" is a string, and 
the replace method is invoked on it. Two additional parameter values are provided, "s", and and
empty string. So, in the sentence, all occurrences of "s" are replaced with the empty string. A new 
string is returned, "Thi i a entence." There is another period followed by the word replace, so
the replace method is called again on that string, returning the shorter string, which is printed.


