..  Copyright (C)  Brad Miller, David Ranum
    This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.


Strongly Connected Components
-----------------------------

For the remainder of this chapter we will turn our attention to some
extremely large graphs. The graphs we will use to study some additional
algorithms are the graphs produced by the connections between hosts on
the Internet and the links between web pages. We will begin with web
pages.

Search engines like Google and Bing exploit the fact that the pages on
the web form a very large directed graph. To transform the World Wide
Web into a graph, we will treat a page as a vertex, and the hyperlinks
on the page as edges connecting one vertex to another.
:ref:`Figure 30 <fig_cshome>` shows a very small part of the graph produced by
following the links from one page to the next, beginning at Luther
College’s Computer Science home page. Of course, this graph could be
huge, so we have limited it to web sites that are no more than 10 links
away from the CS home page.

.. _fig_cshome:

.. figure:: Figures/cshome.png
   :align: center

   Figure 30: The Graph Produced by Links from the Luther Computer Science Home Page      



If you study the graph in :ref:`Figure 30 <fig_cshome>` you might make some
interesting observations. First you might notice that many of the other
web sites on the graph are other Luther College web sites. Second, you
might notice that there are several links to other colleges in Iowa.
Third, you might notice that there are several links to other liberal
arts colleges. You might conclude from this that there is some
underlying structure to the web that clusters together web sites that
are similar on some level.

One graph algorithm that can help find clusters of highly interconnected
vertices in a graph is called the strongly connected components
algorithm (**SCC**). We formally define a **strongly connected
component**, :math:`C`, of a graph :math:`G`, as the largest subset
of vertices :math:`C \subset V` such that for every pair of vertices
:math:`v, w \in C` we have a path from :math:`v` to :math:`w` and
a path from :math:`w` to :math:`v`. :ref:`Figure 27 <fig_scc1>` shows a simple
graph with three strongly connected components. The strongly connected
components are identified by the different shaded areas.

.. _fig_scc1:
        
.. figure:: Figures/scc1.png
   :align: center

   Figure 31: A Directed Graph with Three Strongly Connected Components


Once the strongly connected components have been identified we can show
a simplified view of the graph by combining all the vertices in one
strongly connected component into a single larger vertex. The simplified
version of the graph in :ref:`Figure 31 <fig_scc1>` is shown in :ref:`Figure 32 <fig_scc2>`.

.. _fig_scc2:

.. figure:: Figures/scc2.png
   :align: center

   Figure 32: The Reduced Graph


Once again we will see that we can create a very powerful and efficient
algorithm by making use of a depth first search. Before we tackle the
main SCC algorithm we must look at one other definition. The
transposition of a graph :math:`G` is defined as the graph
:math:`G^T` where all the edges in the graph have been reversed. That
is, if there is a directed edge from node A to node B in the original
graph then :math:`G^T` will contain and edge from node B to node A.
:ref:`Figure 33 <fig_tpa>` and :ref:`Figure 34 <fig_tpb>` show a simple graph and its transposition.



    
.. _fig_tpa:


.. figure:: Figures/transpose1.png
   :align: center

   Figure 33: A Graph :math:`G`
          
.. _fig_tpb:


.. figure:: Figures/transpose2.png
   :align: center

   Figure 34: Its Transpose :math:`G^T`


Look at the figures again. Notice that the graph in
:ref:`Figure 33 <fig_tpa>` has two strongly connected components. Now look at 
:ref:`Figure 34 <fig_tpb>`. Notice that it has the same two strongly connected
components.

We can now describe the algorithm to compute the strongly connected
components for a graph.

#. Call ``dfs`` for the graph :math:`G` to compute the finish times
   for each vertex.

#. Compute :math:`G^T`.

#. Call ``dfs`` for the graph :math:`G^T` but in the main loop of DFS
   explore each vertex in decreasing order of finish time.

#. Each tree in the forest computed in step 3 is a strongly connected
   component. Output the vertex ids for each vertex in each tree in the
   forest to identify the component.

Let's trace the operation of the steps described above on the example
graph in :ref:`Figure 31 <fig_scc1>`. :ref:`Figure 35 <fig_sccalga>` shows the starting and
finishing times computed for the original graph by the DFS algorithm.
:ref:`Figure 36 <fig_sccalgb>` shows the starting and finishing times computed by
running DFS on the transposed graph.

 
.. _fig_sccalga:

.. figure:: Figures/scc1a.png
   :align: center
   
   Figure 35: Finishing times for the original graph :math:`G`     


     
.. _fig_sccalgb:

.. figure:: Figures/scc1b.png
   :align: center
   
   Figure 36: Finishing times for :math:`G^T`
    


Finally, :ref:`Figure 37 <fig_sccforest>` shows the forest of three trees produced
in step 3 of the strongly connected component algorithm. You will notice
that we do not provide you with the Python code for the SCC algorithm,
we leave writing this program as an exercise.

          
.. _fig_sccforest:

.. figure:: Figures/sccforest.png
   :align: center
   
   Figure 37: Strongly Connected Components
