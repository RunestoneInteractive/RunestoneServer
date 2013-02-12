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

class FocalFish(Schooler):

    def getNewHeading(self):
        swarmSize = len(Schooler.swarm)



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