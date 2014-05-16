..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Implementation
--------------

Keeping in mind the definitions from the previous section, we can use
the following functions to create and manipulate a binary tree:

-  ``BinaryTree()`` creates a new instance of a binary tree.

-  ``getLeftChild()`` returns the binary tree corresponding to the left
   child of the current node.

-  ``getRightChild()`` returns the binary tree corresponding to the
   right child of the current node.

-  ``setRootVal(val)`` stores the object in parameter ``val`` in the
   current node.

-  ``getRootVal()`` returns the object stored in the current node.

-  ``insertLeft(val)`` creates a new binary tree and installs it as the
   left child of the current node.

-  ``insertRight(val)`` creates a new binary tree and installs it as the
   right child of the current node.

The key decision in implementing a tree is choosing a good internal
storage technique. Python allows us two very interesting possibilities,
so we will examine both before choosing one. The first technique we will
call “list of lists,” the second technique we will call “nodes and
references.”

