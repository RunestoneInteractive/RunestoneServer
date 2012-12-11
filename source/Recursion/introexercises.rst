Glossary
--------

.. glossary::

    base case
        A branch of the conditional statement in a recursive function that does
        not give rise to further recursive calls.

    immutable data type
        A data type which cannot be modified.  Assignments to elements or
        slices of immutable types cause a runtime error.

    infinite recursion
        A function that calls itself recursively without ever reaching the base
        case. Eventually, an infinite recursion causes a runtime error.

    mutable data type
        A data type which can be modified. All mutable types are compound
        types.  Lists and dictionaries (see next chapter) are mutable data
        types; strings and tuples are not.

    recursion
        The process of calling the function that is already executing.

    recursive call
        The statement that calls an already executing function.  Recursion can
        even be indirect --- function `f` can call `g` which calls `h`, 
        and `h` could make a call back to `f`.

    recursive definition
        A definition which defines something in terms of itself. To be useful
        it must include *base cases* which are not recursive. In this way it
        differs from a *circular definition*.  Recursive definitions often
        provide an elegant way to express complex data structures.



Programming Exercises
---------------------

#. Write a recursive function to compute the factorial of a number.

   .. actex:: ex_rec_1

#. Write a recursive function to reverse a list.

   .. actex:: ex_rec_2
   
#. Modify the recursive tree program using one or all of the following
   ideas:

   -  Modify the thickness of the branches so that as the ``branchLen``
      gets smaller, the line gets thinner.

   -  Modify the color of the branches so that as the ``branchLen`` gets
      very short it is colored like a leaf.

   -  Modify the angle used in turning the turtle so that at each branch
      point the angle is selected at random in some range. For example
      choose the angle between 15 and 45 degrees. Play around to see
      what looks good.

   -  Modify the ``branchLen`` recursively so that instead of always
      subtracting the same amount you subtract a random amount in some
      range.

   If you implement all of the above ideas you will have a very
   realistic looking tree.
   
   .. actex:: ex_rec_3

#. Find or invent an algorithm for drawing a fractal mountain. Hint: One
   approach to this uses triangles again.

   .. actex:: ex_rec_4

#. Write a recursive function to compute the Fibonacci sequence. How
   does the performance of the recursive function compare to that of an
   iterative version?

   .. actex:: ex_rec_5

#. Using the turtle graphics module, write a recursive program to
   display a Hilbert curve.

   .. actex:: ex_rec_6
   
#. Using the turtle graphics module, write a recursive program to
   display a Koch snowflake.

   .. actex:: ex_rec_7
