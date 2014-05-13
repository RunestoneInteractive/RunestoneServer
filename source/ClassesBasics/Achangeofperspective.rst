..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

A change of perspective
-----------------------

Throughout the earlier chapters, we wrote functions and called them using a syntax such as ``drawCircle(tess)``.  This suggests that the
function is the active agent. It says something like, *"Hey, drawCircle!  
Here's a turtle object for you to use to draw with."*

In object-oriented programming, the objects are considered the active agents. 
For example, in our early introduction to turtles, we used
an object-oriented style. We said ``tess.forward(100)``, which 
asks the turtle to move itself forward by the given number of steps.
An
invocation like ``tess.circle()`` says *"Hey tess!
Please use your circle method!"*



This change in perspective is sometimes considered to be a more "polite" way to write programming instructions.  However, it may not initially
be obvious that it is useful. It turns out that often times shifting responsibility from 
the functions onto the objects makes it possible to write more versatile 
functions and makes it easier to maintain and reuse code.  

The most important advantage of the object-oriented style is that it
fits our mental chunking and real-life experience more accurately. 
In real life our ``cook`` method is part of our microwave oven --- we don't
have a ``cook`` function sitting in the corner of the kitchen, into which
we pass the microwave!  Similarly, we use the cellphone's own methods 
to send an sms, or to change its state to silent.  The functionality 
of real-world objects tends to be tightly bound up inside the objects 
themselves.  OOP allows us to accurately mirror this when we
organize our programs.
 
