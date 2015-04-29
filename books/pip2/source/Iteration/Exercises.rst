Exercises
=========


1. (You'll work on on this one in class. Feel free to start thinking about it.) In Robert McCloskey's
   book *Make Way for Ducklings*, the names of the ducklings are Jack, Kack, Lack,
   Mack, Nack, Ouack, Pack, and Quack.  This loop tries to output these names in order.

.. sourcecode:: python

   prefixes = "JKLMNOPQ"
   suffix = "ack"

   for p in prefixes:
       print p + suffix


Of course, that's not quite right because Ouack and Quack are misspelled.
Can you fix it?

.. actex:: ex_8_2


2. Get the user to enter some text and print it out in reverse. (Hint: we did this as well as capitalizing
in one of the earlier exercises. But first see if you can generate the answer without looking back.)

.. actex:: ex_8_5


3. Get the user to enter some text and print out True if it's a palindrome, False otherwise. (Hint: reuse
some of your code from the last question. The == operator compares two values to see if they are the same)

.. actex:: ex_8_6
