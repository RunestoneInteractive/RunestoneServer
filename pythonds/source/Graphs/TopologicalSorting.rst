..  Copyright (C)  Brad Miller, David Ranum
    This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.


Topological Sorting
-------------------

To demonstrate that computer scientists can turn just about anything
into a graph problem, let’s consider the difficult problem of stirring
up a batch of pancakes. The recipe is really quite simple: 1 egg, 1 cup
of pancake mix, 1 tablespoon oil, and :math:`3 \over 4` cup of milk.
To make pancakes you must heat the griddle, mix all the ingredients
together and spoon the mix onto a hot griddle. When the pancakes start
to bubble you turn them over and let them cook until they are golden
brown on the bottom. Before you eat your pancakes you are going to want
to heat up some syrup. :ref:`Figure 27 <fig_pancakes>` illustrates this process as
a graph.


.. _fig_pancakes:

.. figure:: Figures/pancakes.png
   :align: center

   Figure 27: The Steps for Making Pancakes       



The difficult thing about making pancakes is knowing what to do first.
As you can see from :ref:`Figure 27 <fig_pancakes>` you might start by heating the
griddle or by adding any of the ingredients to the pancake mix. To help
us decide the precise order in which we should do each of the steps
required to make our pancakes we turn to a graph algorithm called the
**topological sort**.

A topological sort takes a directed acyclic graph and produces a linear
ordering of all its vertices such that if the graph :math:`G` contains
an edge :math:`(v,w)` then the vertex :math:`v` comes before the
vertex :math:`w` in the ordering. Directed acyclic graphs are used in
many applications to indicate the precedence of events. Making pancakes
is just one example; other examples include software project schedules,
precedence charts for optimizing database queries, and multiplying
matrices.

The topological sort is a simple but useful adaptation of a depth first
search. The algorithm for the topological sort is as follows:

#. Call ``dfs(g)`` for some graph ``g``. The main reason we want to call
   depth first search is to compute the finish times for each of the
   vertices.

#. Store the vertices in a list in decreasing order of finish time.

#. Return the ordered list as the result of the topological sort.

:ref:`Figure 28 <fig_pancakesDFS>` shows the depth first forest constructed by
``dfs`` on the pancake-making graph shown in :ref:`Figure 26 <fig_pancakes>`.

.. _fig_pancakesDFS:

.. figure:: Figures/pancakesDFS.png
   :align: center

   Figure 28: Result of Depth First Search on the Pancake Graph
          



Finally, :ref:`Figure 29 <fig_pancakesTS>` shows the results of applying the
topological sort algorithm to our graph. Now all the ambiguity has been
removed and we know exactly the order in which to perform the pancake
making steps.

.. _fig_pancakesTS:

.. figure:: Figures/pancakesTS.png
   :align: center

   Figure 29: Result of Topological Sort on Directed Acyclic Graph
          



