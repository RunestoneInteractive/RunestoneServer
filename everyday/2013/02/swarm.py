__author__ = 'millbr02'

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
                    repulsion.append((dist,other))
                elif dist <= self.align:
                    alignment.append((dist,other))
                elif dist <= self.attract:
                    attraction.append((dist,other))

        if repulsion:
            repulsion.sort()
            nbr = repulsion[0][1]
            self.newHead = nbr.heading()+90

        elif alignment:
#            alignment.sort()
#            nbr = alignment[0][1]
#            self.newHead = (nbr.heading() + self.heading()) // 2
            hs = self.heading()
            for other in alignment:
                hs = hs + other[1].heading()
            self.newHead = hs // (len(alignment)+1)

        elif attraction:
            attraction.sort()
            nbr = attraction[0][1]
            self.newHead = self.towards(nbr)

        else:
            self.newHead = self.heading()



def main():
    swarmSize = 100
    t = Turtle()
    win = Screen()
    win.setworldcoordinates(-600,-600,600,600)
    t.speed(10)
    t.hideturtle()
    win.tracer(15)

    for i in range(swarmSize):
        FocalFish()

    for turn in range(1000):
        for schooler in Schooler.swarm:
            schooler.getNewHeading()

        for schooler in Schooler.swarm:
            schooler.setHeadingAndMove()

    win.exitonclick()


main()