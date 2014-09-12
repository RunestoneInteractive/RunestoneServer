..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

.. _iteration_chap:

Introduction: Iteration
=======================

A basic building block of all programs is to be able to repeat some code
over and over again.  In computing, we refer to this repetitive execution as **iteration**.  In this section, we will explore some mechanisms for basic iteration.

With collections (lists and strings), a lot of computations involve processing one item at a time.  
For strings this means that we would like to process one character at a time.
Often we start at the beginning, select each character in turn, do something
to it, and continue until the end. This pattern of processing is called a
**traversal**, or **iteration over the characters**. Similarly, we can process each of the items in a list, one at a time,
**iteration over the items in the list**.

.. index:: for loop

