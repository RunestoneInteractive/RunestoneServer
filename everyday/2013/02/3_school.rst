.. This document is Licensed Creative Commons:
   Attribution, Share Alike by Brad Miller, Luther College 2013

A Better Flocking Implementation
================================

Last time we looked at a  follow-the-leader kind of implementation of a flocking algorithm. It was kind of fun to watch, and it may even have reminded you of some ants.  This time around lets look at an implementation of something a little better.  To remind you, here are the rules we set out for a better simulation.

1.  Move in the same direction as your closest neighbors.
2.  Don't stray off by yourself - stay close
3.  But not too close.  Avoid collisions with your neighbors.

This diagram illustrates the rules nicely:

.. image:: focalfish.png

In the diagram you can see that you can classify all the other organisms (Fish) into one of three zones:  1) Zone of repulsion, 2) zone of alignment, and 3) zone of attraction.

1.  In the zone of repulsion the current fish will seek to move itself away from its neighbors.  You might think of doing this by finding the midpoint of all the neighbors, finding the heading to go towards that midpoint, and then doing going in the opposite direction.

2.   In the zone of alignment, the fish would want to align its heading with the average heading of all the fish in the zone.  You might average the headings of all the other fish in this zone to get your own heading.

3. In the zone of attraction you might calculate the midpoint of all the fish in the zone and then head toward that point.

To implement the rules, we will continue to explore the power of inheritance.  In fact to make this completely new simulation we will make our new simulation inherit from ``Schooler`` and we will simply implement a new version of ``getNewHeading``.

.. sourcecode:: python

   class FocalFish(Schooler):
   repulse = 10
   align = 50
   attract = 600

   def getNewHeading(self):
       repulsion = []
       alignment = []
       attraction = []

       for other in Schooler.swarm:
           if self != other:
               dist = self.distance(other)
               if dist <= self.repulse:
                   repulsion.append(other)
               elif dist <= self.align:
                   alignment.append(other)
               elif dist <= self.attract:
                   attraction.append(other)

       self.newHead = self.heading()
       if repulsion:
           x = 0
           y = 0
           for o in repulsion:
               x = x + o.xcor()
               y = y + o.ycor()

           self.newHead = self.towards(x/len(repulsion),y/len(repulsion)) + 180

       elif alignment:
           hs = self.heading()
           for other in alignment:
               hs = hs + other.heading()
           self.newHead = hs // (len(alignment)+1)

       elif attraction:
           x = 0
           y = 0
           for o in attraction:
               x = x + o.xcor()
               y = y + o.ycor()
           self.newHead = self.towards(x/len(attraction),y/len(attraction))



The general flow of the code above is to first create three lists of fish, those in the zone of repulsion, those in the zone of alignment, and those in the zone of attraction.  The rest of the function asks the questions:

* Do I (``self``) have fish in my zone of repulsion?  If so then I'll move away from the spot that would be the center of all of those fish.

* If there are no fish in my zone of repulsion are there any fish in my zone of alignment?  If so, then I will change my heading to match the average heading of all the other fish in my zone of alignment.

* Finally if there are no fish in my zone of alignment or my zone of repulsion, lets see if there are fish in my zone of attraction.  If there are then I'll change my heading to head towards the middle of the fish in my zone of attraction.

Notice that this implementation makes one possible interpretation of the rules, which is that you only make a move based on the fish in the closest zone.  Other interpretations are possible, for example you might calculate a new heading taking into consideration fish in all three zones and then make your new heading the average of those different options.  You will see that you get very different behavior if you make those changes.

Here is the complete source so that you can run this new simulation.  But I encourage you to try to make the changes to incorporate feedback from all three zones of fish.

.. activecode:: focalfish_1

   from turtle import Turtle, Screen
   import random
   from math import cos, radians


   class Schooler(Turtle):
       swarm = []

       def __init__(self):
           Turtle.__init__(self)
           self.up()
           self.setheading(random.randrange(360))
           self.setpos(random.randrange(-200,200),random.randrange(-200,200))
           self.down()
           self.newHead = None
           Schooler.swarm.append(self)

       def getNewHeading(self):
           minangle = 999
           for other in Schooler.swarm:
               if self != other:
                   head = self.towards(other) - self.heading()
                   if cos(radians(head)) > 0:
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

   class FocalFish(Schooler):
       repulse = 10
       align = 50
       attract = 600

       def getNewHeading(self):
           repulsion = []
           alignment = []
           attraction = []

           for other in Schooler.swarm:
               if self != other:
                   dist = self.distance(other)
                   if dist <= self.repulse:
                       repulsion.append(other)
                   elif dist <= self.align:
                       alignment.append(other)
                   elif dist <= self.attract:
                       attraction.append(other)

           self.newHead = self.heading()
           if repulsion:
               x = 0
               y = 0
               for o in repulsion:
                   x = x + o.xcor()
                   y = y + o.ycor()

               self.newHead = self.towards(x/len(repulsion),y/len(repulsion)) + 180

           elif alignment:
               hs = self.heading()
               for other in alignment:
                   hs = hs + other.heading()
               self.newHead = hs // (len(alignment)+1)

           elif attraction:
               x = 0
               y = 0
               for o in attraction:
                   x = x + o.xcor()
                   y = y + o.ycor()
               self.newHead = self.towards(x/len(attraction),y/len(attraction))




   def main():
       swarmSize = 50
       t = Turtle()
       win = Screen()
       win.setworldcoordinates(-600,-600,600,600)
       t.speed(10)
       t.hideturtle()
       t.tracer(15)

       for i in range(swarmSize):
           FocalFish()

       for turn in range(300):
           for schooler in Schooler.swarm:
               schooler.getNewHeading()

           for schooler in Schooler.swarm:
               schooler.setHeadingAndMove()

       win.exitonclick()


   main()

Adding Obstacles
================

The final question to explore is what might happen if we add obstacles for our swarm to avoid and move around.  What we'll do is the following.  If an obstacle is imminent, that is it is within 40 units of our fish, and we are more or less headed for the obstacle.  Lets say that it is within 45 degrees of our heading as we go forward, we will compensate by turning away from the obstacle.  Obstacle avoidance will overrule all other schooling behavior.

To implement this lets make another subclass.  This time we will subclass ``FocalFish`` and call it ``ObstacleFish.``  Our obstacle fish will first check for any obstacles to avoid, if there is an obsacle we'll avoid it otherwise we will have the exact same behavior as ``FocalFish``.  We can make this happen using the following strategy.

.. sourcecode:: python

   class ObstacleFish(FocalFish):
       def getNewHeading(self):
           avoiding = False
           for o in Obstacle.obstacles:
               if self.inFrontOf(o) and self.distance(o) < 40:
                   angleTo = (self.towards(o) - self.heading())%360
                   if angleTo < 45:
                       print "taking leftward evasive ", angleTo
                       self.newHead = self.heading() - 25
                       avoiding = True
                   elif angleTo > 315:
                       self.newHead = self.heading() + 25
                       print "taking rightward evasive ", angleTo
                       avoiding = True
           if not avoiding:
               FocalFish.getNewHeading(self)


The key in this example is the line ``FocalFish.getNewHeading(self)``  This allows us to add our special behavior at the beginning, and if there is no obstacle to avoid we can delegate the calculation of our new heading to our parent class ``FocalFish``.  Python also provides us with a slightly simpler way of managing this delegation, with the ``super`` funciton.  In python 2.7 we could write: ``super(ObstacleFish,self).getNewHeading()`` This frees us from worrying about the exact superclass.  In Python3.3 its even easier:  ``super().getNewHeading()``.  Using ``super`` is particularly useful if your class has more than one parent.  We call this **Multiple Inheritance**, but at the beginner level this is almost never used, and writing ``FocalFish.getNewHeading(self)`` makes it crystal clear what Python is up to.  Besides, the Python implementation for the browser does not yet support super.

The last piece of the ObstacleFish program is the obstacle itself.  By this point, you may have a feel for whats coming:  A subclass of turtle with a round shape.

.. sourcecode:: python

   class Obstacle(Turtle):
       obstacles = []
       def __init__(self):
           Turtle.__init__(self)
           self.up()
           self.setpos(random.randrange(-200,200),random.randrange(-200,200))
           self.shape('circle')
           Obstacle.obstacles.append(self)


Now see if you can put all the pieces together and make this work for yourself.

.. actex:: obstacle_fish_1

As a final experiment think about what happens if a fish decides it wants to be a leader.  Maybe give any one fish a 1% chance of becoming a leader. Color this fish red and see how many other fish decide to follow.

.. actex:: leader_fish






