:orphan:

..  Copyright (C) Paul Resnick.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

.. highlight:: python
    :linenothreshold: 500


Activities through 2/15
=======================

You have the following graded activities:

1. Class prep. Don't forget: always access the textbook by clicking on the Textbook link from cTools, so that you'll be logged in and get credit for doing the prep.
   
   * Before Monday's class: 
      * Read :ref:`Defining Functions<functions_chap>`, and do the exercises in that chapter
           
   
   * Before Wednesday's class:
       * Read :ref:`While loops<while_chap>`, and do the exercises in that chapter
       * Read :ref:`Installing a Native Python Interpreter and Text Editor <next_steps>` and follow the instructions to set up for running python on your computer
       
 
#. Reading responses

   * By Tuesday midnight: 
      * Read *The Most Human Human*, Chapter 10, p.219-237 only (you'll read the rest of the chapter next week). Note: we are skipping some of the other chapters.
      * Answer :ref:`Reading Response 6 <reading_response_6>`. 

#. Problem set **Due:** **Sunday, February 15 at 5 pm**

   * Do the :ref:`Native Python Interpreter and Text Editor part of Problem Set 5. <unix_pset5>`
      
   * Save answers to the exercises in Problem Set 5: :ref:`Problem Set 5 <problem_set_5>` 



Reading Response
----------------

.. _reading_response_6:

1. Compare a conversation that "stays in book" to one that doesn't. Which has more surprisal? Which would be easier to compress?
2. Give an example of compression other than the ones Christian addresses. Explain. Why? In what situations does this occur?

.. activecode:: rr_6_1

   # Fill in your response in between the triple quotes
   s = """

   """
   print s


.. _unix_pset5:

Native Python Interpreter and Text Editor
-----------------------------------------

Turn these in as screenshots via CTools in the Assignments tab!

#. Make a new file in your text editor, and save it as ``new_program.py``. (This is a Python program!)

#. In your ``new_program.py`` file, write the following code (copy it from here).

.. activecode:: example_code_ps6

   def cool_machine(x):
   	y = x**2 +7
   	print y

   z = 65.3
   print z + cool_machine(8)

Then, run the Python program in your native Python interpreter. You should get an error. Take a screenshot of this and upload it to CTools.

Make edits to this code so it will work (the only output should be 136.3), without an error, and then save it with a different name (``fixed_program.py``). Now, run unix ``diff`` on these two files. Take a screenshot of the output, and upload it to CTools.



.. _problem_set_5:

Problem Set
-----------

.. datafile:: timely_file.txt
	:hide:

	Autumn is interchangeably known as fall in the US and Canada, and is one of the four temperate seasons. Autumn marks the transition from summer into winter.
	Some cultures regard the autumn equinox as mid autumn while others, with a longer temperature lag, treat it as the start of autumn then. 
	In North America, autumn starts with the September equinox, while it ends with the winter solstice. 
	(Wikipedia)


3. Define a function called add_three, which takes one integer as input and returns that integer + 3.

.. activecode:: ps_5_3

    # Write your code here.
    # (The tests for this problem are going to try to CALL the function that you write!)

    ====

    import test
    try:
      print "testing if add_three(2) equals 5"
      test.testEqual(add_three(2),5)
      print "testing if add_three(33) equals 36"
      test.testEqual(add_three(33),36)
    except:
      print "The function add_three has not been defined yet, OR it hasn't been defined properly"


4. Write code **that will keep printing what the user inputs over and over until the user enters the string "quit".**

.. activecode:: ps_5_4

   # Write code here

   ====
   print "\n---\n\n"
   print "There are no tests for this problem"


5. Take a look at the code below. The function subtract_five is supposed to take one integer as input and return that integer - 5. You'll get an error if you run it as is. Change it so it works!

.. activecode:: ps_5_5

   def subtract_five(inp)
   	print inp - 5
	return None
    
   y = subtract_five(9) - 6

   ====

   print "\n---\n\n"
   import test
   try:
    print "testing if y is -2"
    test.testEqual(y, -2)
   except:
    print "The variable y was deleted or is not defined"

6. Here's another bit of code with a problem. Also, add comments about what's going on with the current code that causes a problem. Then, fix it so it calls change_amounts on some input and prints out the results.

.. activecode:: ps_5_6

    def change_amounts(yp):
	n = yp - 4
	return n * 7
    
    print yp
    
    ====
    
    print "\n---\n\n"
    print "There are no tests for this problem"


7. Define a function called change_amounts that takes one integer as input. If the input is larger than 10, it should return the input + 5. If the input is smaller than or equal to 10, it should return the input + 2.

.. activecode:: ps_5_7

    # We've started you off with the first line...
    def change_amounts(num_here):
       pass # delete this line and put in your own code for the body of the function.
    
    ====
    
    print "\n---\n\n"
    import test
    try:
      print "testing if change_amounts(9) equals 11"
      test.testEqual(change_amounts(9),11)
      print "testing if change_amounts(12) equals 17"
      test.testEqual(change_amounts(12),17)
    except:
      print "The function change_amounts has not been defined properly"

8. Given the string in the code below, write code to figure out what the most common word in the string is and assign that to the variable ``abc``. (Do not hard-code the right answer.) Hint: dictionaries will be useful here.

.. activecode:: ps_5_8

   s = "Will there really be such a thing as morning in the morning"
   # Write your code here...
    
   ====
    
   print "\n---\n\n"
   import test
   print "testing whether abc is set correctly"
   try:
     test.testEqual(abc, 'morning')
   except:
     print "The variable abc has not been defined"


9. We've given you another data file in this problem. It's called ``timely_file.txt``. Write code to figure out which is the most common word in the file. Again, save it in the variable ``abc``.

.. activecode:: ps_5_9
   :available_files: timely_file.txt

   # Write code here!
    
   ====
    
   print "\n---\n\n"
   import test
   try:
     print "testing whether abc is set correctly"
     test.testEqual(abc, 'the')
   except:
     print "The variable abc has not been defined"
