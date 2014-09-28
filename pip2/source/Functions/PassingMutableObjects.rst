..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Passing Mutable Objects
-----------------------

As you have seen, when a function (or method is invoked) and a parameter value is provided, a new
stack frame is created, and the parameter name is bound to the parameter value.
What happens when the value that is provided is a mutable object, like a list or dictionary?
Is the parameter name bound to a *copy* of the original object, or does it become an 
alias for exactly that object? In python, the answer is that it becomes an alias
for the original object. This answer matters  when the code block inside the function
definition causes some change to be made to the object (e.g., adding a key-value
pair to a dictionary or appending to a list). 

This sheds a little different light
on the idea of parameters being *local*. They *are* local in the sense that if you have a parameter
x inside a function and there is a global variable x, any reference to x inside
the function gets you the value of local variable x, not the global one. If you set 
``x = 3``, it changes the value of the local variable x, but when the function finishes
executing, that local x disappears, and so does the value 3. 

If, one the other hand, the local variable x points to a list ``[1, 3, 7]``,
setting ``x[2] = 0`` makes x still point to the same list, but changes the list's contents to ``[1, 3, 0]``.
The local variable x is discarded when the function completes execution, but the 
mutation to the list lives on if there is some other variable outside the function
that also is an alias for the same list.

Consider the following example.

.. activecode:: function2_7
   
   def double(y):
      y = 2 * y
   
   def changeit(lst):
      lst[0] = "Michigan"
      lst[1] = "Wolverines"

   y = 5
   double(y)
   print y
      
   mylst = ['106', 'students', 'are', 'awesome']
   changeit(mylst)
   print mylst

Try running it. Similar to examples we have seen before, running double does 
not change the global y. But
running changeit does change mylst. The explanation is above, about the sharing
of mutable objects. Try stepping through it in codelens to see the difference.

.. codelens:: function2_8
   
   def double(n):
      n = 2 * n
   
   def changeit(lst):
      lst[0] = "Michigan"
      lst[1] = "Wolverines"

   y = 5
   double(y)
   print y
      
   mylst = ['106', 'students', 'are', 'awesome']
   changeit(mylst)
   print mylst

