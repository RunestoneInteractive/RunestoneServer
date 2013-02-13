.. This document is Licensed Creative Commons:
   Attribution, Share Alike by Brad Miller, Luther College 2013

Swarming Intelligence
=====================

This week's post is inspired by the book *Kill Decision*by Daniel Suarez.
Suarez is a relatively new Techno-Thriller author, and I love his books.  In this book, unmanned drones already exist.  How do these drones know what to do?  How to fight?  Thats the scary part, get their fighting instincts from some of the fiercest killers on the planet... Weaver ants.  The female protagonist studies the social structure of ants, however unknown forces have taken her algorithm to implant in unmanned drones.

.. raw:: html

   <iframe width="420" height="315" src="http://www.youtube.com/embed/9liT8epLnAQ" frameborder="0" allowfullscreen></iframe>

This video shows you everything you need to understand about how ants are attracted to pheromones and will sense the pheromones and move toward them.  In the video the blue blobs are patches of food, and the purple blog is the nest.  When ants find food they head back to the nest, but they also leave behind a trail of pheromones that other ants can follow.  the stronger the scent the whiter the trail.  YOu can see how quickly the majority of the ants get to the strongest trail.  In the case of drones in the book getting food equals killing people and tearing apart things.

The rest of the story you'll have to read for yourself.  Now I'm reading *Avogadro Corp* which features Collaborative Filtering, which as the topic of my PhD thesis.  Maybe another post in the works...

The ant intelligence in *Kill Decision* got me to thinking about swarming algorithms and whether or not I could implemented something really simple in Python.  Although there are many `swarming algorithms <http://en.wikipedia.org/wiki/Swarm_intelligence>`_ that are used to solve really hard problems I'm going to go with something simple and graphical.

First Example
-------------

Here's a simple example Suppose you have a bird or a fish and the only rule they have for where to go next is to head directly for the fish or bird that is "most directly in their line of vision."

The procedure for this is pretty easy.  Lets iterate through all the other organisms around us.

1. Eliminate all of those that are behind us.  Lets assume that our organisms can only see things in front of them.
2. Of all the things in front of us choose the one that is most closely aligned with our own heading.
3. Change our heading to go directly toward that organism.


Here is a first try at implementing, and graphically showing the algorithm I've just described.

.. activecode:: follow_the_leader

    import turtle
    import random
    from math import cos, radians

    swarmSize = 25
    t = turtle.Turtle()
    win = turtle.Screen()
    win.setworldcoordinates(-600,-600,600,600)
    t.speed(10)
    win.tracer(15)

    swarm = []


    def getNewHeading(i):
        minangle = 999
        for j in range(swarmSize):
            if i != j:
                head = swarm[i].towards(swarm[j]) - swarm[i].heading()
                infront = cos(radians(head))
                if infront > 0:
                    if head < minangle:
                        minangle = head
        return minangle

    for i in range(swarmSize):
        nt = turtle.Turtle()
        swarm.append(nt)
        nt.up()
        nt.setheading(random.randrange(360))
        nt.setpos(random.randrange(-300,300),random.randrange(-300,300))
        nt.down()

    for turn in range(100):
        newhead = []
        for i in range(swarmSize):
            minangle = getNewHeading(i)
            if minangle == 999:
                newhead.append(swarm[i].heading())
            else:
                newhead.append(minangle+swarm[i].heading())

        for i in range(swarmSize):
            swarm[i].setheading(newhead[i])
            swarm[i].forward(10)

    win.exitonclick()


An Object Oriented Implementation
---------------------------------

.. activecode:: second_try

    from turtle import Turtle, Screen
    import random
    from math import cos, radians


    class Schooler(Turtle):
        swarm = []

        def __init__(self):
            Turtle.__init__(self)
            self.up()
            self.setheading(random.randrange(360))
            self.setpos(random.randrange(-300,300),random.randrange(-300,300))
            self.down()
            self.newHead = None
            Schooler.swarm.append(self)

        def getNewHeading(self):
            minangle = 999
            swarmSize = len(Schooler.swarm)
            for j in range(swarmSize):
                if self != Schooler.swarm[j]:
                    head = self.towards(Schooler.swarm[j]) - self.heading()
                    infront = cos(radians(head))
                    if infront > 0:
                        if head < minangle:
                            minangle = head
            if minangle == 999:
                self.newHead = self.heading()
            else:
                self.newHead = minangle+self.heading()

        def setHeadingAndMove(self):
            self.setheading(self.newHead)
            self.newHead = None
            self.forward(10)


    def main():
        swarmSize = 25
        t = Turtle()
        win = Screen()
        win.setworldcoordinates(-600,-600,600,600)
        t.speed(10)
        t.hideturtle()
        win.tracer(15)

        for i in range(swarmSize):
            Schooler()

        for turn in range(100):
            for schooler in Schooler.swarm:
                schooler.getNewHeading()

            for schooler in Schooler.swarm:
                schooler.setHeadingAndMove()

        win.exitonclick()


    main()





References
~~~~~~~~~~

.. _Boids: http://www.red3d.com/cwr/boids/

