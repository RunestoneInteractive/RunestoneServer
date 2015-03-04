..  Copyright (C)  Brad Miller, David Ranum
    This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.


Discussion Questions
--------------------

#. Draw the graph corresponding to the following adjacency matrix.

.. figure:: Figures/adjMatEX.png
   :align: center


#. Draw the graph corresponding to the following list of edges.

   .. table:: 

           +--------+------+--------+
           | from   | to   | cost   |
           +========+======+========+
           | 1      | 2    | 10     |
           +--------+------+--------+
           | 1      | 3    | 15     |
           +--------+------+--------+
           | 1      | 6    | 5      |
           +--------+------+--------+
           | 2      | 3    | 7      |
           +--------+------+--------+
           | 3      | 4    | 7      |
           +--------+------+--------+
           | 3      | 6    | 10     |
           +--------+------+--------+
           | 4      | 5    | 7      |
           +--------+------+--------+
           | 6      | 4    | 5      |
           +--------+------+--------+
           | 5      | 6    | 13     |
           +--------+------+--------+

#. Ignoring the weights, perform a breadth first search on the graph
   from the previous question.

#. What is the Big-O running time of the ``buildGraph`` function?

#. Derive the Big-O running time for the topological sort algorithm.

#. Derive the Big-O running time for the strongly connected components
   algorithm.

#. Show each step in applying Dijkstra’s algorithm to the graph shown above.

#. Using Prim’s algorithm, find the minimum weight spanning tree for the
   graph shown above.

#. Draw a dependency graph illustrating the steps needed to send an
   email. Perform a topological sort on your graph.

#. Derive an expression for the base of the exponent used in expressing
   the running time of the knights tour.

#. Explain why the general DFS algorithm is not suitable for solving the
   knights tour problem.

#. What is the Big-O running time for Prim’s minimum spanning tree
   algorithm?

