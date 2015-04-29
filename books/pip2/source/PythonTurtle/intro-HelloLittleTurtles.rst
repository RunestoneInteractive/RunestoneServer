..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

.. _turtles_chap:

Hello Little Turtles!
=====================

.. index::
    single: module
    single: function
    single: function definition
    single: definition; function
    single: turtle module

.. video:: assignvid
    :controls:
    :thumb: ../_static/turtleintro.png

    http://media.interactivepython.org/thinkcsVideos/turtleintro.mov
    http://media.interactivepython.org/thinkcsVideos/turtleintro.webm



There are many *modules* in Python that provide very powerful features that we
can use in our own programs.  Some of these can send email or fetch web pages. Others allow us to perform complex mathematical calculations.
In this chapter we will introduce a module that allows us to create a data object called a **turtle** that can be used to draw pictures.

.. turtles and get them
.. turn left, etc.  Your turtle's tail is also endowed with the ability to leave
.. to draw shapes and patterns.

Turtle graphics, as it is known, is based on a very simple
metaphor. Imagine that you have a turtle that understands English.  You can
tell your turtle to do simple commands such as go forward and turn right.  As the turtle
moves around, if its tail is down touching the ground, it will
draw a line (leave a trail behind) as it moves.  If you tell your turtle to lift up its tail it can
still move around but will not leave a trail.  As you will see, you can make
some pretty amazing drawings with this simple capability.

.. note::

	The turtles are fun, but the real purpose of the chapter is to teach ourselves
	a little more Python and to develop our theme of *computational thinking*. You'll first do some things with the turtles, and then we'll summarize the concepts and syntax you've learned, in particular classes, instances, and method invocations.


.. index:: object, invoke, method, attribute, state, canvas

