..  Copyright (C)  Brad Miller, David Ranum
    This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.


Exploring a Maze
----------------

In this section we will look at a problem that has relevance to the
expanding world of robotics: How do you find your way out of a maze? If you have
a Roomba vacuum cleaner for your dorm room (don’t all college students?)
you will wish that you could reprogram it using what you have learned in
this section. The problem we want to solve is to help our turtle find
its way out of a virtual maze. The maze problem has roots as deep as the
Greek myth about Theseus who was sent into a maze to kill the minotaur.
Theseus used a ball of thread to help him find his way back out again
once he had finished off the beast. In our problem we will assume that
our turtle is dropped down somewhere into the middle of the maze and
must find its way out. Look at :ref:`Figure 2 <fig_mazescreen>` to get an idea of
where we are going in this section.

.. _fig_mazescreen:

.. figure:: Figures/maze.png
   :align: center

   Figure 2: The Finished Maze Search Program


To make it easier for us we will assume that our maze is divided up into
“squares.” Each square of the maze is either open or occupied by a
section of wall. The turtle can only pass through the open squares of
the maze. If the turtle bumps into a wall it must try a different
direction. The turtle will require a systematic procedure to find its
way out of the maze. Here is the procedure:

-  From our starting position we will first try going North one square
   and then recursively try our procedure from there.

-  If we are not successful by trying a Northern path as the first step
   then we will take a step to the South and recursively repeat our
   procedure.

-  If South does not work then we will try a step to the West as our
   first step and recursively apply our procedure.

-  If North, South, and West have not been successful then apply the
   procedure recursively from a position one step to our East.

-  If none of these directions works then there is no way to get out of
   the maze and we fail.

Now, that sounds pretty easy, but there are a couple of details to talk
about first. Suppose we take our first recursive step by going North. By
following our procedure our next step would also be to the North. But if
the North is blocked by a wall we must look at the next step of the
procedure and try going to the South. Unfortunately that step to the
south brings us right back to our original starting place. If we apply
the recursive procedure from there we will just go back one step to the
North and be in an infinite loop. So, we must have a strategy to
remember where we have been. In this case we will assume that we have a
bag of bread crumbs we can drop along our way. If we take a step in a
certain direction and find that there is a bread crumb already on that
square, we know that we should immediately back up and try the next
direction in our procedure. As we will see when we look at the code for
this algorithm, backing up is as simple as returning from a recursive
function call.

As we do for all recursive algorithms let us review the base cases. Some
of them you may already have guessed based on the description in the
previous paragraph. In this algorithm, there are four base cases to
consider:

#. The turtle has run into a wall. Since the square is occupied by a
   wall no further exploration can take place.

#. The turtle has found a square that has already been explored. We do
   not want to continue exploring from this position or we will get into
   a loop.

#. We have found an outside edge, not occupied by a wall. In other words
   we have found an exit from the maze.

#. We have explored a square unsuccessfully in all four directions.

For our program to work we will need to have a way to represent the
maze. To make this even more interesting we are going to use the turtle
module to draw and explore our maze so we can watch this algorithm in
action. The maze object will provide the following methods for us to use
in writing our search algorithm:

-  ``__init__`` Reads in a data file representing a maze, initializes
   the internal representation of the maze, and finds the starting
   position for the turtle.

-  ``drawMaze`` Draws the maze in a window on the screen.

-  ``updatePosition`` Updates the internal representation of the maze
   and changes the position of the turtle in the window.

-  ``isExit`` Checks to see if the current position is an exit from the
   maze.

The ``Maze`` class also overloads the index operator ``[]`` so that our
algorithm can easily access the status of any particular square.

Let’s examine the code for the search function which we call
``searchFrom``. The code is shown in :ref:`Listing 3 <lst_mazesearch>`. Notice
that this function takes three parameters: a maze object, the starting
row, and the starting column. This is important because as a recursive
function the search logically starts again with each recursive call.

.. _lst_mazesearch:

.. highlight:: python
    :linenothreshold: 5
    
**Listing 3**

::

    def searchFrom(maze, startRow, startColumn):
        maze.updatePosition(startRow, startColumn)
       #  Check for base cases:
       #  1. We have run into an obstacle, return false
       if maze[startRow][startColumn] == OBSTACLE :
            return False
        #  2. We have found a square that has already been explored
        if maze[startRow][startColumn] == TRIED:
            return False
        # 3. Success, an outside edge not occupied by an obstacle
        if maze.isExit(startRow,startColumn):
            maze.updatePosition(startRow, startColumn, PART_OF_PATH)
            return True
        maze.updatePosition(startRow, startColumn, TRIED)

        # Otherwise, use logical short circuiting to try each 
        # direction in turn (if needed)
        found = searchFrom(maze, startRow-1, startColumn) or \
                searchFrom(maze, startRow+1, startColumn) or \
                searchFrom(maze, startRow, startColumn-1) or \
                searchFrom(maze, startRow, startColumn+1)
        if found:
            maze.updatePosition(startRow, startColumn, PART_OF_PATH)
        else:
            maze.updatePosition(startRow, startColumn, DEAD_END)
        return found

As you look through the algorithm you will see that the first thing the
code does (line 2) is call ``updatePosition``. This is simply to help
you visualize the algorithm so that you can watch exactly how the turtle
explores its way through the maze. Next the algorithm checks for the
first three of the four base cases: Has the turtle run into a wall (line
5)? Has the turtle circled back to a square already explored (line 8)?
Has the turtle found an exit (line 11)? If none of these conditions is
true then we continue the search recursively.

You will notice that in the recursive step there are four recursive
calls to ``searchFrom``. It is hard to predict how many of these
recursive calls will be used since they are all connected by ``or``
statements. If the first call to ``searchFrom`` returns ``True`` then
none of the last three calls would be needed. You can interpret this as
meaning that a step to ``(row-1,column)`` (or North if you want to think
geographically) is on the path leading out of the maze. If there is not
a good path leading out of the maze to the North then the next recursive
call is tried, this one to the South. If South fails then try West, and
finally East. If all four recursive calls return false then we have
found a dead end. You should download or type in the whole program and
experiment with it by changing the order of these calls.

The code for the ``Maze`` class is shown in :ref:`Listing 4 <lst_maze>`, :ref:`Listing 5 <lst_maze1>`, and :ref:`Listing 6 <lst_maze2>`. 
The ``__init__`` method takes the name of a file as its
only parameter. This file is a text file that represents a maze by using
“+” characters for walls, spaces for open squares, and the letter “S” to
indicate the starting position. :ref:`Figure 3 <fig_exmaze>` is an example of a
maze data file. The internal representation of the maze is a list of
lists. Each row of the ``mazelist`` instance variable is also a list.
This secondary list contains one character per square using the
characters described above. For the data file in :ref:`Figure 3 <fig_exmaze>` the
internal representation looks like the following:

.. highlight:: python
    :linenothreshold: 500

::

    [ ['+','+','+','+',...,'+','+','+','+','+','+','+'],
      ['+',' ',' ',' ',...,' ',' ',' ','+',' ',' ',' '],
      ['+',' ','+',' ',...,'+','+',' ','+',' ','+','+'],
      ['+',' ','+',' ',...,' ',' ',' ','+',' ','+','+'],
      ['+','+','+',' ',...,'+','+',' ','+',' ',' ','+'],
      ['+',' ',' ',' ',...,'+','+',' ',' ',' ',' ','+'],
      ['+','+','+','+',...,'+','+','+','+','+',' ','+'],
      ['+',' ',' ',' ',...,'+','+',' ',' ','+',' ','+'],
      ['+',' ','+','+',...,' ',' ','+',' ',' ',' ','+'],
      ['+',' ',' ',' ',...,' ',' ','+',' ','+','+','+'],
      ['+','+','+','+',...,'+','+','+',' ','+','+','+']]

The ``drawMaze`` method uses this internal representation to draw the
initial view of the maze on the screen.

.. _fig_exmaze:


Figure 3: An Example Maze Data File

::
    
      ++++++++++++++++++++++
      +   +   ++ ++     +   
      + +   +       +++ + ++
      + + +  ++  ++++   + ++
      +++ ++++++    +++ +  +
      +          ++  ++    +
      +++++ ++++++   +++++ +
      +     +   +++++++  + +
      + +++++++      S +   +
      +                + +++
      ++++++++++++++++++ +++


The ``updatePosition`` method, as shown in :ref:`Listing 5 <lst_maze1>` uses the
same internal representation to see if the turtle has run into a wall.
It also updates the internal representation with a “.” or “-” to
indicate that the turtle has visited a particular square or if the
square is part of a dead end. In addition, the ``updatePosition`` method
uses two helper methods, ``moveTurtle`` and ``dropBreadCrumb``, to
update the view on the screen.

Finally, the ``isExit`` method uses the current position of the turtle
to test for an exit condition. An exit condition is whenever the turtle
has navigated to the edge of the maze, either row zero or column zero,
or the far right column or the bottom row.

.. _lst_maze:

**Listing 4**

.. highlight:: python
    :linenothreshold: 500

::

    class Maze:
        def __init__(self,mazeFileName):
            rowsInMaze = 0
            columnsInMaze = 0
            self.mazelist = []
            mazeFile = open(mazeFileName,'r')
            rowsInMaze = 0
            for line in mazeFile:
                rowList = []
                col = 0
                for ch in line[:-1]:
                    rowList.append(ch)
                    if ch == 'S':
                        self.startRow = rowsInMaze
                        self.startCol = col
                    col = col + 1
                rowsInMaze = rowsInMaze + 1
                self.mazelist.append(rowList)
                columnsInMaze = len(rowList)

            self.rowsInMaze = rowsInMaze
            self.columnsInMaze = columnsInMaze
            self.xTranslate = -columnsInMaze/2
            self.yTranslate = rowsInMaze/2
            self.t = Turtle(shape='turtle')
            setup(width=600,height=600)
            setworldcoordinates(-(columnsInMaze-1)/2-.5,
                                -(rowsInMaze-1)/2-.5,
                                (columnsInMaze-1)/2+.5,
                                (rowsInMaze-1)/2+.5)

.. _lst_maze1:

**Listing 5**

::

        def drawMaze(self):
            for y in range(self.rowsInMaze):
                for x in range(self.columnsInMaze):
                    if self.mazelist[y][x] == OBSTACLE:
                        self.drawCenteredBox(x+self.xTranslate,
                                             -y+self.yTranslate,
                                             'tan')
            self.t.color('black','blue')

        def drawCenteredBox(self,x,y,color):
            tracer(0)
            self.t.up()
            self.t.goto(x-.5,y-.5)
            self.t.color('black',color)
            self.t.setheading(90)
            self.t.down()
            self.t.begin_fill()
            for i in range(4):
                self.t.forward(1)
                self.t.right(90)
            self.t.end_fill()
            update()
            tracer(1)

        def moveTurtle(self,x,y):
            self.t.up()
            self.t.setheading(self.t.towards(x+self.xTranslate,
                                             -y+self.yTranslate))
            self.t.goto(x+self.xTranslate,-y+self.yTranslate)

        def dropBreadcrumb(self,color):
            self.t.dot(color)

        def updatePosition(self,row,col,val=None):
            if val:
                self.mazelist[row][col] = val
            self.moveTurtle(col,row)

            if val == PART_OF_PATH:
                color = 'green'
            elif val == OBSTACLE:
                color = 'red'
            elif val == TRIED:
                color = 'black'
            elif val == DEAD_END:
                color = 'red'
            else:
                color = None
                
            if color:
                self.dropBreadcrumb(color)

.. _lst_maze2:

**Listing 6**

::

       def isExit(self,row,col):
            return (row == 0 or
                    row == self.rowsInMaze-1 or
                    col == 0 or
                    col == self.columnsInMaze-1 )

       def __getitem__(self,idx):
            return self.mazelist[idx]


The complete program is shown in ActiveCode 1.  This program uses the data file ``maze2.txt`` shown below.
Note that it is a much more simple example file in that the exit is very close to the starting position of the turtle.

.. raw:: html

	<pre id="maze2.txt">
  ++++++++++++++++++++++
  +   +   ++ ++        +
        +     ++++++++++
  + +    ++  ++++ +++ ++
  + +   + + ++    +++  +
  +          ++  ++  + +
  +++++ + +      ++  + +
  +++++ +++  + +  ++   +
  +          + + S+ +  +
  +++++ +  + + +     + +
  ++++++++++++++++++++++
    </pre>

.. activecode:: completemaze
    :caption: Complete Maze Solver
    :nocodelens:
    :timelimit: off

    import turtle

    PART_OF_PATH = 'O'
    TRIED = '.'
    OBSTACLE = '+'
    DEAD_END = '-'

    class Maze:
        def __init__(self,mazeFileName):
            rowsInMaze = 0
            columnsInMaze = 0
            self.mazelist = []
            mazeFile = open(mazeFileName,'r')
            rowsInMaze = 0
            for line in mazeFile:
                rowList = []
                col = 0
                for ch in line[:-1]:
                    rowList.append(ch)
                    if ch == 'S':
                        self.startRow = rowsInMaze
                        self.startCol = col
                    col = col + 1
                rowsInMaze = rowsInMaze + 1
                self.mazelist.append(rowList)
                columnsInMaze = len(rowList)

            self.rowsInMaze = rowsInMaze
            self.columnsInMaze = columnsInMaze
            self.xTranslate = -columnsInMaze/2
            self.yTranslate = rowsInMaze/2
            self.t = turtle.Turtle()
            self.t.shape('turtle')
            self.wn = turtle.Screen()
            self.wn.setworldcoordinates(-(columnsInMaze-1)/2-.5,-(rowsInMaze-1)/2-.5,(columnsInMaze-1)/2+.5,(rowsInMaze-1)/2+.5)

        def drawMaze(self):
            self.t.speed(10)
            self.wn.tracer(0)        
            for y in range(self.rowsInMaze):
                for x in range(self.columnsInMaze):
                    if self.mazelist[y][x] == OBSTACLE:
                        self.drawCenteredBox(x+self.xTranslate,-y+self.yTranslate,'orange')
            self.t.color('black')
            self.t.fillcolor('blue')
            self.wn.update()
            self.wn.tracer(1)

        def drawCenteredBox(self,x,y,color):
            self.t.up()
            self.t.goto(x-.5,y-.5)
            self.t.color(color)
            self.t.fillcolor(color)
            self.t.setheading(90)
            self.t.down()
            self.t.begin_fill()
            for i in range(4):
                self.t.forward(1)
                self.t.right(90)
            self.t.end_fill()

        def moveTurtle(self,x,y):
            self.t.up()
            self.t.setheading(self.t.towards(x+self.xTranslate,-y+self.yTranslate))
            self.t.goto(x+self.xTranslate,-y+self.yTranslate)

        def dropBreadcrumb(self,color):
            self.t.dot(10,color)

        def updatePosition(self,row,col,val=None):
            if val:
                self.mazelist[row][col] = val
            self.moveTurtle(col,row)

            if val == PART_OF_PATH:
                color = 'green'
            elif val == OBSTACLE:
                color = 'red'
            elif val == TRIED:
                color = 'black'
            elif val == DEAD_END:
                color = 'red'
            else:
                color = None

            if color:
                self.dropBreadcrumb(color)

        def isExit(self,row,col):
            return (row == 0 or
                    row == self.rowsInMaze-1 or
                    col == 0 or
                    col == self.columnsInMaze-1 )
        
        def __getitem__(self,idx):
            return self.mazelist[idx]


    def searchFrom(maze, startRow, startColumn):
        # try each of four directions from this point until we find a way out.
        # base Case return values:
        #  1. We have run into an obstacle, return false
        maze.updatePosition(startRow, startColumn)
        if maze[startRow][startColumn] == OBSTACLE :
            return False
        #  2. We have found a square that has already been explored
        if maze[startRow][startColumn] == TRIED or maze[startRow][startColumn] == DEAD_END:
            return False
        # 3. We have found an outside edge not occupied by an obstacle
        if maze.isExit(startRow,startColumn):
            maze.updatePosition(startRow, startColumn, PART_OF_PATH)
            return True
        maze.updatePosition(startRow, startColumn, TRIED)
        # Otherwise, use logical short circuiting to try each direction 
        # in turn (if needed)
        found = searchFrom(maze, startRow-1, startColumn) or \
                searchFrom(maze, startRow+1, startColumn) or \
                searchFrom(maze, startRow, startColumn-1) or \
                searchFrom(maze, startRow, startColumn+1)
        if found:
            maze.updatePosition(startRow, startColumn, PART_OF_PATH)
        else:
            maze.updatePosition(startRow, startColumn, DEAD_END)
        return found


    myMaze = Maze('maze2.txt')
    myMaze.drawMaze()
    myMaze.updatePosition(myMaze.startRow,myMaze.startCol)

    searchFrom(myMaze, myMaze.startRow, myMaze.startCol)

.. admonition:: Self Check

   Modify the maze search program so that the calls to searchFrom are in a different order.  Watch the program run. Can you explain why the behavior is different?  Can you predict what path the turtle will follow for a given change in order?
