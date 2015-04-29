..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Side Effects
------------

We say that the function changeit has a **side effect** on the list object that is passed to it.
Global variables are another way to have side effects. For example, similar to examples
you have seen above, we could make double have a side effect on the global variable y.

.. codelens:: function2_9
   
   def double(n):
      global y
      y = 2 * n
   
   y = 5
   double(y)
   print y

Side effects are sometimes convenient. For example, it may be convenient to have
a single dictionary that accumulates information, and pass it around to various
functions that might add to it or modify it.

However, programs that have side effects can be very difficult to debug. When an
object has a value that is not what you expected, it can be difficult to track
down exactly where in the code it was set. Wherever it is practical to do so, 
it is best to avoid side effects. The way to avoid using side effects is to use
return values instead.

Instead of modifying a global variable inside a function, pass the global variable's
value in as a parameter, and set that global variable to be equal to a value returned
from the function. For example, the following is a better version of the code 
above.

.. codelens:: function2_10
   
   def double(n):
      return 2 * n
   
   y = 5
   y = double(y)
   print y

You can use the same coding pattern to avoid confusing side effects with sharing
of mutable objects. To do that, explicitly make a copy of an object and pass the
copy in to the function. Then return the modified copy and reassign it to the 
original variable if you want to save the changes. The built-in ``list`` function, which
takes a sequence as a parameter and returns a new list, works to copy an existing
list. For dictionaries, you can similarly call the ``dict`` function, passing in a dictionary
to get a copy of the dictionary back as a return value.

.. codelens:: function2_11
      
   def changeit(lst):
      lst[0] = "Michigan"
      lst[1] = "Wolverines"
      return lst
      
   mylst = ['106', 'students', 'are', 'awesome']
   newlst = changeit(list(mylst))
   print mylst
   print newlst

In general, any lasting effect that occurs in a function, not through its return value,  is called a side effect. There are three ways to have side effects:

* Printing out a value. This doesn't change any objects or variable bindings, but it does have a potential lasting effect outside the function execution, because a person might see the output and be influenced by it.
* Changing the value of a mutable object.
* Changing the binding of a global variable.

