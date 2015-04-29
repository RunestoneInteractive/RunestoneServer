..  Copyright (C)  Brad Miller, David Ranum
    This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.


Vocabulary and Definitions
--------------------------

Now that we have looked at examples of trees, we will formally define a
tree and its components.

Node
    A node is a fundamental part of a tree. It can have a name, which we
    call the “key.” A node may also have additional information. We call
    this additional information the “payload.” While the payload
    information is not central to many tree algorithms, it is often
    critical in applications that make use of trees.

Edge
    An edge is another fundamental part of a tree. An edge connects two
    nodes to show that there is a relationship between them. Every node
    (except the root) is connected by exactly one incoming edge from
    another node. Each node may have several outgoing edges.

Root
    The root of the tree is the only node in the tree that has no
    incoming edges. In Figure :ref:`Figure 2 <fig_filetree>`, / is the root of the tree.

Path
    A path is an ordered list of nodes that are connected by edges. For
    example,
    Mammal :math:`\rightarrow` Carnivora :math:`\rightarrow` Felidae :math:`\rightarrow` Felis :math:`\rightarrow` Domestica
    is a path.

Children
    The set of nodes :math:`c` that have incoming edges from the same
    node to are said to be the children of that node. In Figure
    :ref:`Figure 2 <fig_filetree>`, nodes log/, spool/, and yp/ are the children of node
    var/.

Parent
    A node is the parent of all the nodes it connects to with outgoing
    edges. In :ref:`Figure 2 <fig_filetree>` the node var/ is the parent of nodes
    log/, spool/, and yp/.

Sibling
    Nodes in the tree that are children of the same parent are said to
    be siblings. The nodes etc/ and usr/ are siblings in the filesystem
    tree.

Subtree
    A subtree is a set of nodes and edges comprised of a parent and all
    the descendants of that parent.

Leaf Node
    A leaf node is a node that has no children. For example, Human and
    Chimpanzee are leaf nodes in :ref:`Figure 1 <fig_biotree>`.

Level
    The level of a node :math:`n` is the number of edges on the path
    from the root node to :math:`n`. For example, the level of the
    Felis node in :ref:`Figure 1 <fig_biotree>` is five. By definition, the level
    of the root node is zero.

Height
    The height of a tree is equal to the maximum level of any node in
    the tree. The height of the tree in :ref:`Figure 2 <fig_filetree>` is two.

With the basic vocabulary now defined, we can move on to a formal
definition of a tree. In fact, we will provide two definitions of a
tree. One definition involves nodes and edges. The second definition,
which will prove to be very useful, is a recursive definition.

*Definition One:* A tree consists of a set of nodes and a set of
edges that connect pairs of nodes. A tree has the following properties:

-  One node of the tree is designated as the root node.

-  Every node :math:`n`, except the root node, is connected by an edge
   from exactly one other node :math:`p`, where :math:`p` is the
   parent of :math:`n`.

-  A unique path traverses from the root to each node.

-  If each node in the tree has a maximum of two children, we say that
   the tree is a **binary tree**.

:ref:`Figure 3 <fig_nodeedgetree>` illustrates a tree that fits definition one.
The arrowheads on the edges indicate the direction of the connection.

.. _fig_nodeedgetree:

.. figure:: Figures/treedef1.png
   :align: center
   :alt: image

   Figure 3: A Tree Consisting of a Set of Nodes and Edges

*Definition Two:* A tree is either empty or consists of a root and zero
or more subtrees, each of which is also a tree. The root of each subtree
is connected to the root of the parent tree by an edge.
:ref:`Figure 4 <fig_recursivetree>` illustrates this recursive definition of a tree.
Using the recursive definition of a tree, we know that the tree in
:ref:`Figure 4 <fig_recursivetree>` has at least four nodes, since each of the
triangles representing a subtree must have a root. It may have many more
nodes than that, but we do not know unless we look deeper into the tree.

.. _fig_recursivetree:

.. figure:: Figures/TreeDefRecursive.png
   :align: center
   :alt: image

   Figure 4: A recursive Definition of a tree
