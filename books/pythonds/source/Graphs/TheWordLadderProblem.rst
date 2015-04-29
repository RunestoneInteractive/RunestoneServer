..  Copyright (C)  Brad Miller, David Ranum
    This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.


The Word Ladder Problem
~~~~~~~~~~~~~~~~~~~~~~~

To begin our study of graph algorithms let’s consider the following
puzzle called a word ladder. Transform the word “FOOL” into the word
“SAGE”. In a word ladder puzzle you must make the change occur gradually
by changing one letter at a time. At each step you must transform one
word into another word, you are not allowed to transform a word into a
non-word. The word ladder puzzle was invented in 1878 by Lewis Carroll,
the author of *Alice in Wonderland*. The following sequence of words
shows one possible solution to the problem posed above.

::

 FOOL
 POOL
 POLL
 POLE
 PALE
 SALE
 SAGE        
 
There are many variations of the word ladder puzzle. For example you
might be given a particular number of steps in which to accomplish the
transformation, or you might need to use a particular word. In this
section we are interested in figuring out the smallest number of
transformations needed to turn the starting word into the ending word.

Not surprisingly, since this chapter is on graphs, we can solve this
problem using a graph algorithm. Here is an outline of where we are
going:

-  Represent the relationships between the words as a graph.

-  Use the graph algorithm known as breadth first search to find an
   efficient path from the starting word to the ending word.

