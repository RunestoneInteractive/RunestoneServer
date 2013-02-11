__author__ = 'millbr02'

import turtle
import random
from math import cos, radians

swarmSize = 25
t = turtle.Turtle()
win = turtle.Screen()
t.speed(10)

swarm = []

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
        minangle = 999
        for j in range(swarmSize):
            if i != j:
                head = swarm[i].towards(swarm[j])-swarm[i].heading()
                infront = cos(radians(head))
                if infront > 0:
                    if head < minangle:
                        minangle = head
        if minangle == 999:
            newhead.append(swarm[i].heading())
        else:
            newhead.append(minangle+swarm[i].heading())

    for i in range(swarmSize):
        swarm[i].setheading(newhead[i])
        swarm[i].forward(10)

win.exitonclick()