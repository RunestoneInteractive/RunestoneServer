..  Copyright (C)  Brad Miller, David Ranum
    This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.


The Knight’s Tour Problem
~~~~~~~~~~~~~~~~~~~~~~~~~

Another classic problem that we can use to illustrate a second common
graph algorithm is called the “knight’s tour.” The knight’s
tour puzzle is played on a chess board with a single chess piece, the
knight. The object of the puzzle is to find a sequence of moves that
allow the knight to visit every square on the board exactly once. One
such sequence is called a “tour.” The knight’s tour puzzle has
fascinated chess players, mathematicians and computer scientists alike
for many years. The upper bound on the number of possible legal tours
for an eight-by-eight chessboard is known to be
:math:`1.305 \times 10^{35}`; however, there are even more possible
dead ends. Clearly this is a problem that requires some real brains,
some real computing power, or both.

Although researchers have studied many different algorithms to solve the
knight’s tour problem, a graph search is one of the easiest to
understand and program. Once again we will solve the problem using two
main steps:

-  Represent the legal moves of a knight on a chessboard as a graph.

-  Use a graph algorithm to find a path of length
   :math:`rows \times columns - 1` where every vertex on the graph is
   visited exactly once.

