Introducing Processing
======================

Its been more than a month since my last post.  Second semester has been busier than I expected, leaving less time for writing than I had hoped.  Now, I am a big fan of turtle graphics.  It is great for teaching introductory programming, and works especially well with younger students.  However it has its limitations, and I've been wishing for a while now that there was another graphics system that I could incorporate into Skulpt and the Runestone toolset.  Last weekend, I got sucked into a bit of hacking that has turned out better than I had ever hoped.

I've certainly heard about the processing language over the last several years but I've never taken the time to look into it, or any of the derivative implementations such as processing-js, pyprocessing, or the like.  Finally I decided to take a peek a few weeks ago, and I was immediately hooked.  Since then I've been working on making processing-js accessable as a module from our browser based implementation of Python known as Skulpt.  Here's a quick example of a simple program that is animated and interacts with the mouse.  Just click the run button and move your mouse around in the canvas.


A Simple Animation
------------------

.. activecode:: pjs-1

    from processing import *
    from math import sin

    X = 30
    Y = 30
    radius = 30

    def setup():
        strokeWeight(10)
        frameRate(20)
        size(400,300)

    def draw():
        global X, Y, radius
        delay = 16
        background(100)
        stroke(255)
        fill(0,121,184)
        X += (mouse.x-X)/delay;
        Y += (mouse.y-Y)/delay;
        radius = radius + sin(environment.frameCount / 4)

        ellipse(X,Y,radius,radius)

    def keyPressed():
        print('A key was pressed', keyboard.key)
        exitp()

    run()


Programs that use the processing module all have a similar structure to them.

The ``setup`` function can be used to initialize the size of the canvas, along with the frameRate and things like stroke color and stroke weight.

The ``draw`` function contains all of the real drawing, which can also be done by functions called from draw.  Once ``run`` is called, the draw function is called n times per second according the the value set by the ``frameRate`` function.  In our example the frameRate is set to 20.  This will continue to loop forever, or until ``exit`` is called.  Quite often you will write a program that varies over time.  For this you can use the environment.frameCount value.  Every time draw is called the frameCount is incremented by one.

If you want to write a program that only draws a picture one time, and then exits you can call the ``noLoop`` function from ``setup``.


Using Processing With Your Own Classes
--------------------------------------

Here is another example that may have a bit more interest to it.  Lets look at some balls bouncing around inside the container of the canvas.

.. activecode:: pjs-2

    from processing import *
    from random import randrange
    from math import *
    import sys

    numBalls = 25;
    spring = 0.05;
    gravity = 0.03;
    sys.setExecutionLimit(120000)

    def setup():
      size(300, 400);
      noStroke()
      smooth()
      frameRate(24)

    def draw():
      background(0);
      for i in range(numBalls):
        balls[i].collide()
        balls[i].move()
        balls[i].display()
      if environment.frameCount > 1500:
        noLoop()


    class Ball:

      def __init__(self, xin, yin, din, idin):
        self.x = xin;
        self.y = yin;
        self.vx = 0.0
        self.vy = 0.0
        self.diameter = din;
        self.id = idin;
        self.others = []
        self.color = (randrange(255),randrange(255),randrange(255))

      def makeOthers(self):
        self.others = [x for x in balls if x != self]

      def collide(self):
        for i in range(numBalls-1):
          dx = self.others[i].x - self.x
          dy = self.others[i].y - self.y
          distance = sqrt(dx*dx + dy*dy)
          minDist = self.others[i].diameter/2 + self.diameter/2;
          if distance < minDist:
            angle = atan2(dy, dx);
            targetX = self.x + cos(angle) * minDist;
            targetY = self.y + sin(angle) * minDist;
            ax = (targetX - self.others[i].x) * spring;
            ay = (targetY - self.others[i].y) * spring;
            self.vx -= ax;
            self.vy -= ay;
            self.others[i].vx += ax;
            self.others[i].vy += ay;

      def move(self):
        self.vy += gravity;
        self.x += self.vx;
        self.y += self.vy;
        if (self.x + self.diameter/2 > environment.width):
          self.x = environment.width - self.diameter/2;
          self.vx += -0.9; 
        elif self.x - self.diameter/2 < 0:
          self.x = self.diameter/2;
          self.vx *= -0.9

        if self.y + self.diameter/2 > environment.height:
          self.y = environment.height - self.diameter/2
          self.vy *= -0.9

        elif self.y - self.diameter/2 < 0:
          self.y = self.diameter/2
          self.vy *= -0.9
      
      def display(self):
        fill(self.color[0],self.color[1],self.color[2])
        ellipse(self.x, self.y, self.diameter, self.diameter)


    balls = [Ball(randrange(400), randrange(400), randrange(20, 40), x) for x in range(numBalls)]
    for b in balls:
      b.makeOthers()


    run()

Recursion
---------

And finally, here is an example that illustrates recursion quite nicely.  It also illustrates a way to use the `HSB <http://en.wikipedia.org/wiki/File:Hsl-hsv_models.svg>`_ color system (Hue Saturation, Brightness).  This system is handy when you want to use one number to take you through the ROY G BIV color rainbow from 0 to 360 where 0 is red and 360 is back to red again.  Run this example and then try changing it to add two more recursive calls that put more circles above and below the center line.

.. activecode::  pjs-3

    from processing import *

    def setup():
        size(400,400)
        noStroke()
        smooth()
        colorMode(HSB,100)
        frameRate(1)

    def draw():
        level = environment.frameCount % 8 + 1
        drawCircle(200,200,170,level)

    def drawCircle(x, y, radius, level):
        tt = 100/level
        fill(tt,65,90)
        ellipse(x, y, radius*2, radius*2)
        if level > 1:
            level = level - 1
            drawCircle(x - radius / 2, y, radius/2, level)
            drawCircle(x + radius / 2, y, radius/2, level)

    run()


Images
------

Images are also really easy to work with in processing.  You can place them anywhere you like on the canvas, and then play with individual pixels.  Here's a simple color negative program apllied to my friend Goldy Gopher.

.. activecode:: pjs-4

    from processing import *
    gg = ''

    def setup():
        global gg
        size(300,300)
        gg = loadImage('../../_static/goldygopher.png')
        noLoop()

    def draw():
        image(gg,0,0)
        image(gg,100,100)
        for i in range(gg.width):
            for j in range(gg.height):
                p = get(i,j)
                r = red(p)
                g = green(p)
                b = blue(p)
                p = color(255-r,255-b,255-g)
                set(i,j,p)

    run()

I'm looking forward to updating parts of How to think like a computer scientist, as well as Problem Solving with Aglorithms and Data Structures using Python with this new ability to create fun visual effects.

Until I get the processing module fully documented you can use `This as a guide <http://processingjs.org/reference/>`_  Most of the things are implemented, but if you run into something that is missing or that does not work, please let me know.  Until this gets a lot more use I'm considering it beta quality.


