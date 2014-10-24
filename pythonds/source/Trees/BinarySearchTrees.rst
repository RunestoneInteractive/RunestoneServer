..  Copyright (C)  Brad Miller, David Ranum
    Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Binary Search Trees
-------------------

We have already seen two different ways to get key-value pairs in a
collection. Recall that these collections implement the **map** abstract
data type. The two implementations of a map ADT we discussed were binary
search on a list and hash tables. In this section we will study **binary
search trees** as yet another way to map from a key to a value. In this
case we are not interested in the exact placement of items in the tree,
but we are interested in using the binary tree structure to provide for
efficient searching.

