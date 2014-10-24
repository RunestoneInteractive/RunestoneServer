..  Copyright (C)  Brad Miller, David Ranum
    Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

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

