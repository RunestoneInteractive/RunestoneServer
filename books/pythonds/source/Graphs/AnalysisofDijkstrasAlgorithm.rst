..  Copyright (C)  Brad Miller, David Ranum
    This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.


Analysis of Dijkstra’s Algorithm
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Finally, let us look at the running time of Dijkstra’s algorithm. We
first note that building the priority queue takes :math:`O(V)` time
since we initially add every vertex in the graph to the priority queue.
Once the queue is constructed the ``while`` loop 
is executed once for every vertex since vertices are all added at the
beginning and only removed after that. Within that loop each call to
``delMin``, takes :math:`O(\log V)` time. Taken together that part of
the loop and the calls to delMin take :math:`O(V \log(V))`. The
``for`` loop is executed once for each edge in the
graph, and within the ``for`` loop the call to ``decreaseKey`` takes
time :math:`O(E\log(V)).` So the combined running time is :math:`O((V+E) \log(V)).`

