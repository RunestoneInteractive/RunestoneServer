..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

What Are Linear Structures?
---------------------------

We will begin our study of data structures by
considering four simple but very powerful concepts. Stacks, queues,
deques, and lists are examples of data collections whose items are
ordered depending on how they are added or removed. Once an item is
added, it stays in that position relative to the other elements that
came before and came after it. Collections such as these are often
referred to as **linear data structures**.

Linear structures can be thought of as having two ends. Sometimes these
ends are referred to as the “left” and the “right” or in some cases the
“front” and the “rear.” You could also call them the “top” and the
“bottom.” The names given to the ends are not significant. What
distinguishes one linear structure from another is the way in which
items are added and removed, in particular the location where these
additions and removals occur. For example, a structure might allow new
items to be added at only one end. Some structures might allow items to
be removed from either end.

These variations give rise to some of the most useful data structures in
computer science. They appear in many algorithms and can be used to
solve a variety of important problems.






