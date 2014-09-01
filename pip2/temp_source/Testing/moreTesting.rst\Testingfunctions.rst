..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Testing functions
-----------------

A function defines an operation that can be performed. If the function takes one or more parameters, it is supposed to work properly on a variety of possible inputs. Each test case will check whether the function works properly on **one set of possible inputs**. 

A useful function will do some combination of three things, given its input parameters:

* Return a value. For these, you will write **return value tests**.
* Modify the contents of some mutable object, like a list or dictionary. For these you will write **side effect tests**.
* Print something or write something to a file. Tests of whether a function generates the right printed output are beyond the scope of this testing framework; you won't write these tests.

Testing whether a function returns the correct value is the easiest test case to define. You simply check whether the result of invoking the function a particular input produces the particular output that you expect. If f is your function, and you think that it should transform inputs x and y into output z, then you could write a test as ``test.testEqual(f(x, y), z)``. Or, to give a more concrete example, if you have a function ``sqaure``, you could have a test case ``test.testEqual(square(3), 9)``. Call this a **return value test**. 

To test whether a function makes correct changes to a mutable object, you will need more than one line of code. You will first set the mutable object to some value, then run the function, then check whether the object has the expected value. An example follows. Call this a **side effect test** because you are checking to see whether the function invocation has had the correct side effect on the mutable object.

.. sourcecode:: python

   def update_counts(letters, counts_dict):
       for c in letters:
           if c in counts_dict:
               counts_dict[c] = counts_dict[c] + 1
           else:
               counts_dict[c] = 1
   
   counts_dict = {'a': 3, 'b': 2}
   update_counts("aaab", counts_dict)
   test.testEqual(counts_dict['a'], 6)
   test.testEqual(counts_dict['b'], 3)

Because each test checks whether a function works properly on specific inputs, the test cases will never be complete: in principle, a function might work properly on all the inputs that are tested in the test cases, but still not work properly on some other inputs. That's where the art of defining test cases comes in: you try to find specific inputs that are representative of all the important kinds of inputs that might ever be passed to the function.

The first test case that you define for a function should be an "easy" case, one that is prototypical of the kinds of inputs the function is supposed to handle. Additional test cases should handle "extreme" or unusual inputs. For example, if you are defining the "square" function, the first, easy case, might be an input like 3. Additional extreme or unusual inputs around which you create tests cases might be a negative number, 0, a floating point number, and a very, very large number.  

