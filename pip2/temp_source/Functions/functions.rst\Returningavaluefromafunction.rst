..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Returning a value from a function
---------------------------------

Not only can you pass a parameter value into a function, a function can also 
produce a value. You have already seen this in some previous functions that
you have used. For example, ``len`` takes a list or string as a parameter value
and returns a number, the length of that list or string. ``range`` takes an integer
as a parameter value and returns a list containing all the numbers from 0 up to
that parameter value.

Functions that return values are sometimes called **fruitful functions**.
In many other languages, a chunk that doesn't return a value is called a **procedure**,
but we will stick here with the Python way of also calling it a function, or if we want
to stress it, a *non-fruitful* function.

.. image:: Figures/blackboxfun.png


How do we write our own fruitful function?  Let's start by creating a very simple
mathematical function that we will call ``square``.  The square function will take one number
as a parameter and return the result of squaring that number.  Here is the
black-box diagram with the Python code following.


.. image:: Figures/squarefun.png

.. activecode:: ch04_square

    def square(x):
        y = x * x
        return y

    toSquare = 10
    result = square(toSquare)
    print("The result of " + str(toSquare) + " squared is " + str(result))


The **return** statement is followed by an expression which is evaluated.  Its
result is returned to the caller as the "fruit" of calling this function.
Because the return statement can contain any Python expression we could have
avoided creating the **temporary variable** ``y`` and simply used
``return x*x``.
Try modifying the square function above to see that this works just the same.
On the other hand, using **temporary variables** like ``y`` in the program above makes
debugging
easier.  These temporary variables are referred to as **local variables**.

Notice something important here. The name of the variable we pass as an
argument --- ``toSquare`` --- has nothing to do with the name of the formal parameter
--- ``x``.  It is as if  ``x = toSquare`` is executed when ``square`` is called.
It doesn't matter what the value was named in
the caller (the place where the function was invoked). 
Inside ``square``, it's name is ``x``.  You can see this very clearly in
codelens, where the global variables and the local variables for the square
function are in separate boxes.

.. codelens:: ch04_clsquare

    def square(x):
        y = x * x
        return y

    toSquare = 10
    squareResult = square(toSquare)


There is one more aspect of function return values that should be noted.  
All Python functions return the value ``None`` unless there is an explicit return statement with
a value other than ``None.``
Consider the following common mistake made by beginning Python
programmers.  As you step through this example, pay very close attention to the return
value in the local variables listing.  Then look at what is printed when the
function returns.


.. codelens:: ch04_clsquare_bad

    def square(x):
        y = x * x
        print(y)   # Bad! should use return instead!

    toSquare = 10
    squareResult = square(toSquare)
    print("The result of " + str(toSquare) + " squared is " + str(squareResult))

The problem with this function is that even though it prints the value of the square, 
that value will not be returned to the place
where the call was done.  Since line 6 uses the return value as the right hand 
side of an assignment statement, the evaluation of the 
function will be ``None``.  In this case, ``squareResult`` will refer to that 
value after the assignment statement and therefore the result printed in line 7 is incorrect.  
Typically, functions will return values that can be printed or processed in some other way by the caller.

A return statement, once executed, immediately terminates execution of a function, even if it is not the
last statement in the function. In the following code, when line 3 executes, the
value 5 is returned and assigned to the variable x, then printed. Lines 4 and 5 
never execute. Run the following code and try making some modifications of
it to make sure you understand why "there" and 10 never print out.

.. activecode:: functions_5a

   def weird():
      print("here")
      return(5)
      print("there")
      return(10)
      
   x= weird()
   print(x)

So far, we have just seen return values being assigned to variables. For example, 
we had the line ``squareResult = square(toSquare)``. As with all assignment statements,
the right hand side is executed first. It invokes the square function, passing in a
parameter value 10 (the current value of toSquare). That returns a value 100, which
completes the evaluation of the right-hand side of the assignment. 100 is then assigned
to the variable squareResult. In this case, the function invocation was the entire expression
that was evaluated.

Function invocations, however, can also be used as part of more complicated expressions. 
For example, ``squareResult = 2 * square(toSquare)``. In this case, the value 100 is
returned and is then multiplied by 2 to produce the value 200. When python evaluates an expression
like ``x * 3``, it substitutes the current value of x into the expression and then
does the multiplication. When python evaluates an expression like ``2 * square(toSquare)``, it substitutes
the return value 100 for entire function invocation and then does the multiplication.

To reiterate, when executing a line of code ``squareResult = 2 * square(toSquare)``, the python
interpreter does these steps:

   #. It's an assignment statement, so evaluate the right-hand side expression ``2 * square(toSquare)``.
   #. Look up the values of the variables square and toSquare: square is a function object and toSquare is 10
   #. Pass 10 as a parameter value to the function, get back the return value 100
   #. Substitute 100 for square(toSquare), so that the expression now reads ``2 * 100``
   #. Assign 200 to variable ``squareResult``

**Check your understanding**

.. mchoicemf:: test_questionfunctions_2_1
   :answer_a: You should never use a print statement in a function definition.
   :answer_b: You should not have any statements in a function after the return statement.  Once the function gets to the return statement it will immediately stop executing the function.
   :answer_c: You must calculate the value of x+y+z before you return it.
   :answer_d: A function cannot return a number.
   :correct: b
   :feedback_a: Although you should not mistake print for return, you may include print statements inside your functions.
   :feedback_b: This is a very common mistake so be sure to watch out for it when you write your code!
   :feedback_c: Python will automatically calculate the value x+y+z and then return it in the statement as it is written
   :feedback_d: Functions can return any legal data, including (but not limited to) numbers, strings, lists, dictionaries, etc.

   What is wrong with the following function definition:

   .. code-block:: python

     def addEm(x, y, z):
         return x+y+z
         print('the answer is', x+y+z)


.. mchoicemf:: test_questionfunctions_2_2
   :answer_a: The value None
   :answer_b: The value of x+y+z
   :answer_c: The string 'x+y+z'
   :correct: a
   :feedback_a: We have accidentally used print where we mean return.  Therefore, the function will return the value None by default.  This is a VERY COMMON mistake so watch out!  This mistake is also particularly difficult to find because when you run the function the output looks the same.  It is not until you try to assign its value to a variable that you can notice a difference.
   :feedback_b: Careful!  This is a very common mistake.  Here we have printed the value x+y+z but we have not returned it.  To return a value we MUST use the return keyword.
   :feedback_c: x+y+z calculates a number (assuming x+y+z are numbers) which represents the sum of the values x, y and z.

   What will the following function return?

   .. code-block:: python

    def addEm(x, y, z):
        print(x+y+z)

.. mchoicemf:: test_questionfunctions_2_3
   :answer_a: 25
   :answer_b: 50
   :answer_c: 25 + 25
   :correct: b
   :feedback_a: It squares 5 twice, and adds them together
   :feedback_b: The two return values are added together
   :feedback_c: The two results are substituted into the expression and then it is evaluated. The returned values are integers in this case, not strings
   
   
   What will the following code output?
   
   .. code-block:: python

       def square(x):
           y = x * x
           return y
           
       print(square(5) + square(5))

.. mchoicemf:: test_questionfunctions_2_4
   :answer_a: 8
   :answer_b: 16
   :answer_c: Error: can't put a function invocation inside parentheses
   :correct: b
   :feedback_a: It squares 2, yielding the value 4. But that doesn't mean the next value multiplies 2 and 4.
   :feedback_b: It squares 2, yielding the value 4. 4 is then passed as a value to square again, yeilding 16.
   :feedback_c: This is a more complicated expression, but still valid. The expression square(2) is evaluated, and the return value 4 substitutes for square(2) in the expression.   
   
   What will the following code output?
   
   .. code-block:: python 

       def square(x):
           y = x * x
           return y
           
       print(square(square(2)))

.. mchoicemf:: test_questionfunctions_2_5
   :answer_a: 1
   :answer_b: Yes
   :answer_c: First one was longer
   :answer_d: Second one was at least as long
   :answer_e: Error
   :correct: c
   :feedback_a: cyu2 returns the value 1, but that's not what prints.
   :feedback_b: "Yes" is longer, but that's not what prints.
   :feedback_c: cyu2 returns the value 1, which is assigned to z.
   :feedback_d: cyu2 returns the value 1, which is assigned to z.
   :feedback_e: what do you think will cause an error.
   
   What will the following code output?
   
   .. code-block:: python 

       def cyu2(s1, s2):
           x = len(s1)
           y = len(s2)
           return x-y
           
       z = cyu2("Yes", "no")
       if z > 0:
           print("First one was longer")
       else:
           print("Second one was at least as long")
 
.. mchoicemf:: test_questionfunctions_2_6
   :answer_a: square
   :answer_b: g
   :answer_c: a number
   :correct: b
   :feedback_a: Before executing square, it has to figure out what value to pass in, so g is executed first
   :feedback_b: g has to be executed and return a value in order to know what paramater value to provide to x.
   :feedback_c: square and g both have to execute before the number is printed.   
   
   Which will print out first, square, g, or a number?
   
   .. code-block:: python 

       def square(x):
           print("square")
           return x*x
           
       def g(y):
           print("g")
           return y + 3
           
       print(square(g(2)))


