..  Copyright (C)  Brad Miller, David Ranum
    This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.


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
      :nocodelens:

#. Find or invent an algorithm for drawing a fractal mountain. Hint: One
   approach to this uses triangles again.
   
   .. actex:: ex_rec_4
      :nocodelens:

#. Write a recursive function to compute the Fibonacci sequence. How
   does the performance of the recursive function compare to that of an
   iterative version?
   
   .. actex:: ex_rec_5

#. Implement a solution to the Tower of Hanoi using three stacks to keep
   track of the disks.
   
   .. actex:: ex_rec_6

#. Using the turtle graphics module, write a recursive program to
   display a Hilbert curve.
   
   .. actex:: ex_rec_7
      :nocodelens:

#. Using the turtle graphics module, write a recursive program to
   display a Koch snowflake.
   
   .. actex:: ex_rec_8
      :nocodelens:

#. Write a program to solve the following problem: You have two jugs: a
   4-gallon jug and a 3-gallon jug. Neither of the jugs have markings on
   them. There is a pump that can be used to fill the jugs with water.
   How can you get exactly two gallons of water in the 4-gallon jug?

   .. actex:: ex_rec_9

#. Generalize the problem above so that the parameters to your solution
   include the sizes of each jug and the final amount of water to be
   left in the larger jug.
   
   .. actex:: ex_rec_10

#. Write a program that solves the following problem: Three missionaries
   and three cannibals come to a river and find a boat that holds two
   people. Everyone must get across the river to continue on the
   journey. However, if the cannibals ever outnumber the missionaries on
   either bank, the missionaries will be eaten. Find a series of
   crossings that will get everyone safely to the other side of the
   river.
   
   .. actex:: ex_rec_11

#. Modify the Tower of Hanoi program using turtle graphics to animate
   the movement of the disks. Hint: You can make multiple turtles and
   have them shaped like rectangles.

   .. actex:: ex_rec_12
      :nocodelens:

#. Pascal’s triangle is a number triangle with numbers arranged in
   staggered rows such that 

   .. math::
      a_{nr} = {n! \over{r! (n-r)!}}
   
   This equation is the equation for a binomial coefficient. You can
   build Pascal’s triangle by adding the two numbers that are diagonally
   above a number in the triangle. An example of Pascal’s triangle is
   shown below.

   ::

                         1
                       1   1
                     1   2   1
                   1   3   3   1
                 1   4   6   4   1

   Write a program that prints out Pascal’s triangle. Your program
   should accept a parameter that tells how many rows of the triangle to
   print.
   
   .. actex:: ex_rec_13

