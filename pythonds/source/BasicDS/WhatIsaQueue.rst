..  Copyright (C)  Brad Miller, David Ranum
    This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.


What Is a Queue?
~~~~~~~~~~~~~~~~

A queue is an ordered collection of items where the addition of new
items happens at one end, called the “rear,” and the removal of existing
items occurs at the other end, commonly called the “front.” As an
element enters the queue it starts at the rear and makes its way toward
the front, waiting until that time when it is the next element to be
removed.

The most recently added item in the queue must wait at the end of the
collection. The item that has been in the collection the longest is at
the front. This ordering principle is sometimes called **FIFO**,
**first-in first-out**. It is also known as “first-come first-served.”

The simplest example of a queue is the typical line that we all
participate in from time to time. We wait in a line for a movie, we wait
in the check-out line at a grocery store, and we wait in the cafeteria
line (so that we can pop the tray stack). Well-behaved lines, or queues,
are very restrictive in that they have only one way in and only one way
out. There is no jumping in the middle and no leaving before you have
waited the necessary amount of time to get to the front.
:ref:`Figure 1 <fig_qubasicqueue>` shows a simple queue of Python data objects.

.. _fig_qubasicqueue:

.. figure:: Figures/basicqueue.png
   :align: center

   Figure 1: A Queue of Python Data Objects


Computer science also has common examples of queues. Our computer
laboratory has 30 computers networked with a single printer. When
students want to print, their print tasks “get in line” with all the
other printing tasks that are waiting. The first task in is the next to
be completed. If you are last in line, you must wait for all the other
tasks to print ahead of you. We will explore this interesting example in
more detail later.

In addition to printing queues, operating systems use a number of
different queues to control processes within a computer. The scheduling
of what gets done next is typically based on a queuing algorithm that
tries to execute programs as quickly as possible and serve as many users
as it can. Also, as we type, sometimes keystrokes get ahead of the
characters that appear on the screen. This is due to the computer doing
other work at that moment. The keystrokes are being placed in a
queue-like buffer so that they can eventually be displayed on the screen
in the proper order.

