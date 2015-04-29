..  Copyright (C)  Brad Miller, David Ranum
    This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.


Big-O Notation
~~~~~~~~~~~~~~

When trying to characterize an algorithm’s efficiency in terms of
execution time, independent of any particular program or computer, it is
important to quantify the number of operations or steps that the
algorithm will require. If each of these steps is considered to be a
basic unit of computation, then the execution time for an algorithm can
be expressed as the number of steps required to solve the problem.
Deciding on an appropriate basic unit of computation can be a
complicated problem and will depend on how the algorithm is implemented.

A good basic unit of computation for comparing the summation algorithms
shown earlier might be to count the number of assignment statements
performed to compute the sum. In the function ``sumOfN``, the number of
assignment statements is 1 (:math:`theSum = 0`)
plus the value of *n* (the number of times we perform
:math:`theSum=theSum+i`). We can denote this by a function, call it T,
where :math:`T(n)=1 + n`. The parameter *n* is often referred to as
the “size of the problem,” and we can read this as “T(n) is the time
it takes to solve a problem of size n, namely 1+n steps.”

In the summation functions given above, it makes sense to use the number
of terms in the summation to denote the size of the problem. We can then
say that the sum of the first 100,000 integers is a bigger instance of
the summation problem than the sum of the first 1,000. Because of this,
it might seem reasonable that the time required to solve the larger case
would be greater than for the smaller case. Our goal then is to show how
the algorithm’s execution time changes with respect to the size of the
problem.

Computer scientists prefer to take this analysis technique one step
further. It turns out that the exact number of operations is not as
important as determining the most dominant part of the :math:`T(n)`
function. In other words, as the problem gets larger, some portion of
the :math:`T(n)` function tends to overpower the rest. This dominant
term is what, in the end, is used for comparison. The **order of
magnitude** function describes the part of :math:`T(n)` that increases
the fastest as the value of *n* increases. Order of magnitude is often
called **Big-O** notation (for “order”) and written as
:math:`O(f(n))`. It provides a useful approximation to the actual
number of steps in the computation. The function :math:`f(n)` provides
a simple representation of the dominant part of the original
:math:`T(n)`.

In the above example, :math:`T(n)=1+n`. As *n* gets large, the
constant 1 will become less and less significant to the final result. If
we are looking for an approximation for :math:`T(n)`, then we can drop
the 1 and simply say that the running time is :math:`O(n)`. It is
important to note that the 1 is certainly significant for
:math:`T(n)`. However, as *n* gets large, our approximation will be
just as accurate without it.

As another example, suppose that for some algorithm, the exact number of
steps is :math:`T(n)=5n^{2}+27n+1005`. When *n* is small, say 1 or 2,
the constant 1005 seems to be the dominant part of the function.
However, as *n* gets larger, the :math:`n^{2}` term becomes the most
important. In fact, when *n* is really large, the other two terms become
insignificant in the role that they play in determining the final
result. Again, to approximate :math:`T(n)` as *n* gets large, we can
ignore the other terms and focus on :math:`5n^{2}`. In addition, the
coefficient :math:`5` becomes insignificant as *n* gets large. We
would say then that the function :math:`T(n)` has an order of
magnitude :math:`f(n)=n^{2}`, or simply that it is :math:`O(n^{2})`.

Although we do not see this in the summation example, sometimes the
performance of an algorithm depends on the exact values of the data
rather than simply the size of the problem. For these kinds of
algorithms we need to characterize their performance in terms of best
case, **worst case**, or **average case** performance. The worst case
performance refers to a particular data set where the algorithm performs
especially poorly. Whereas a different data set for the exact same
algorithm might have extraordinarily good performance. However, in most
cases the algorithm performs somewhere in between these two extremes
(average case). It is important for a computer scientist to understand
these distinctions so they are not misled by one particular case.


A number of very common order of magnitude functions will come up over
and over as you study algorithms. These are shown in :ref:`Table 1 <tbl_fntable>`. In
order to decide which of these functions is the dominant part of any
:math:`T(n)` function, we must see how they compare with one another
as *n* gets large.

.. _tbl_fntable: 

.. table:: **Table 1: Common Functions for Big-O**

    ================= =============
             **f(n)**      **Name**
    ================= =============
          :math:`1`      Constant
     :math:`\log n`   Logarithmic
          :math:`n`        Linear
    :math:`n\log n`    Log Linear
      :math:`n^{2}`     Quadratic
      :math:`n^{3}`         Cubic
      :math:`2^{n}`   Exponential
    ================= =============


:ref:`Figure 1 <fig_graphfigure>` shows graphs of the common
functions from :ref:`Table 1 <tbl_fntable>`. Notice that when *n* is small, the
functions are not very well defined with respect to one another. It is
hard to tell which is dominant. However, as *n* grows, there is a
definite relationship and it is easy to see how they compare with one
another.

.. _fig_graphfigure:

.. figure:: Figures/newplot.png

   Figure 1: Plot of Common Big-O Functions


As a final example, suppose that we have the fragment of Python code
shown in :ref:`Listing 2 <lst_dummycode>`. Although this program does not really do
anything, it is instructive to see how we can take actual code and
analyze performance.

.. _lst_dummycode:

**Listing 2**

::

    a=5
    b=6
    c=10
    for i in range(n):
       for j in range(n):
          x = i * i
          y = j * j
          z = i * j
    for k in range(n):
       w = a*k + 45
       v = b*b
    d = 33

The number of assignment operations is the sum of four terms. The first
term is the constant 3, representing the three assignment statements at
the start of the fragment. The second term is :math:`3n^{2}`, since
there are three statements that are performed :math:`n^{2}` times due
to the nested iteration. The third term is :math:`2n`, two statements
iterated *n* times. Finally, the fourth term is the constant 1,
representing the final assignment statement. This gives us
:math:`T(n)=3+3n^{2}+2n+1=3n^{2}+2n+4`. By looking at the exponents,
we can easily see that the :math:`n^{2}` term will be dominant and
therefore this fragment of code is :math:`O(n^{2})`. Note that all of
the other terms as well as the coefficient on the dominant term can be
ignored as *n* grows larger.

.. _fig_graphfigure2:

.. figure:: Figures/newplot2.png

   Figure 2: Comparing :math:`T(n)` with Common Big-O Functions


:ref:`Figure 2 <fig_graphfigure2>` shows a few of the common Big-O functions as they
compare with the :math:`T(n)` function discussed above. Note that
:math:`T(n)` is initially larger than the cubic function. However, as
n grows, the cubic function quickly overtakes :math:`T(n)`. It is easy
to see that :math:`T(n)` then follows the quadratic function as
:math:`n` continues to grow.


.. admonition:: Self Check

   Write two Python functions to find the minimum number in a list.  The first function should compare each number to every other number on the list. :math:`O(n^2)`.  The second function should be linear :math:`O(n)`.


.. video::  findMinVid
   :controls:
   :thumb: ../_static/function_intro.png

   http://media.interactivepython.org/pythondsVideos/findmin.mov
   http://media.interactivepython.org/pythondsVideos/findmin.webm
