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


Week 6: ends October 12
=======================

1. Do the multiple choice questions and exercises in the textbook chapters, including the ones at the bottom of the chapters, below the glossary. Don't forget to click Save for each of the exercises, and always access the textbook by clicking on the link from cTools, so that you'll be logged in.
   
   * Before Tuesday's class: 
      * Read :ref:`Optional and Keyword Parameters<optional_params_chap>`, and do the exercises in that chapter
      * Read `Blog post and demo of sliding window compression  <http://jvns.ca/blog/2013/10/24/day-16-gzip-plus-poetry-equals-awesome/>`_
   
   * Before Thursday's class:
       * Read :ref:`Tuples<tuples_chap>`, and do the exercises in that chapter
       * Read :ref:`Nested Data Structures and Nested Iteration<nested_chap>`, and do the exercises in that chapter
       * Read :ref:`Installing a Native Python Interpreter and Text Editor <install_python_chap>` and follow the instructions to set up for running python on your computer

 
#. Reading responses

   * By Monday midnight: 
      * Read `Tutorial on unix diff <http://www.computerhope.com/unix/udiff.htm>`_ (This will help you understand the section of "The Most Human Human" below).
      * Read *The Most Human Human*, Chapter 10, p.237-259.
      * Answer :ref:`Reading Response 7 <reading_response_7>`. 

#. Problem set **Due:** **Sunday, October 12 at 5 pm**

   * Do the :ref:`Native Python Interpreter and Text Editor part of Problem Set 6. <unix_pset6>`
   
   * Save answers to the exercises in Problem Set 6: :ref:`Problem Set 6 <problem_set_6>` 



Reading Response
----------------

.. _reading_response_7:

Suppose you write and edit a long text file over the course of several days, saving a new version every 15 minutes or so (``myfile1.txt``, ``myfile2.txt``, ``myfile3.txt``,...). Eventually, you have 100 different versions of the file. Now consider the whole directory containing all 100 versions of the file. Would it have a lot of redundancy? As a compression technique, how might you take advantage of the unix diff command in order to reduce the total amount of space required to store all 100 versions of the file?

.. activecode:: rr_7_2

   # Fill in your response in between the triple quotes
   s = """

   """
   print s



If you were to compute information entropy scores for all the students you've met since enrolling at the University of Michigan, which of them has the highest entropy and why? 

.. activecode:: rr_7_2

   # Fill in your response in between the triple quotes
   s = """

   """
   print s


Command Line Problems
---------------------

.. _unix_pset6:

Turn these in as screenshots via CTools in the Assignments tab!

#. Something that requires editing a file in the text editor and saving it as a new file name.

#. Something that requires running a diff command to show what's different between the two. (Save partic file with error in text editor, run it [see that errors are like the errors in the browser environment], fix it, run diff to see the difference, take screenshot.)

#. Something that requires running the native python interpreter on the program.


Problem Set
-----------

.. _problem_set_6:

1. Write three function calls to the function ``give_greeting``: 
one that will return the string ``Hello, SI106!!!``, 
one that will return the string ``Hello, world!!!``,
and one that will return the string ``Hey, everybody!``. 

You may print the return values of those function calls, but you do not have to.

You can see the function definition in the code below, but that's only so you can understand exactly what the code is doing so you can choose how to call this function. Feel free to make comments to help yourself understand, but otherwise DO NOT change the function definition code! HINT: calling the function in different ways and printing the results, to see what happens, may be helpful!

.. activecode:: ps_6_1
   
   def give_greeting(greet_word="Hello",name="SI106",num_exclam=3):
      final_string = greet_word + ", " + name + " " + "!"*num_exclam
      return final_string

   #### DO NOT change the function definition above this line (only comments are OK)

   # Write your three function calls below


#. Define a function called mult_both whose input is two integers, whose default parameter values are the integers 3 and 4, and whose return value is the two input integers multiplied together.

.. activecode:: ps_6_2:

   # Write your code here

   ====

   import test
   print "\n---\n\n"
   print "Testing whether your function works as expected (calling the function mult_both)"
   test.testEqual(mult_both(), 12)
   test.testEqual(mult_both(5,10), 50)



#. Print the second element of each tuple in the list ``new_tuple_list``.

.. activecode:: ps_6_3

   new_tuple_list = [(1,2),(4, "umbrella"),("chair","hello"),("soda",56.2)]


#. You can get data from Facebook that has nested structures which represent posts, or users, or various other types of things on Facebook. We won't put any of our actual Facebook group data on this textbook, because it's publicly available on the internet, but here's a structure that is almost exactly the same as the real thing, with fake data. 

Notice that the stuff in the variable ``fb_data`` is basically a big nested dictionary, with dictionaries and lists, strings and integers, inside it as keys and values. (Later in the course we'll learn how to get this kind of thing directly FROM facebook, and then it will be a bit more complicated and have real information from our Facebook group.)

Follow the directions in the comments!

.. activecode:: ps_6_4

   # first, look through the data structure saved in the variable fb_stuff to get a sense for it.

   fb_stuff = {
  "data": [
    {
      "id": "2253324325325123432madeup", 
      "from": {
        "id": "23243152523425madeup", 
        "name": "Jane Smith"
      }, 
      "to": {
        "data": [
          {
            "name": "Your Facebook Group", 
            "id": "432542543635453245madeup"
          }
        ]
      }, 
      "message": "This problem might use the accumulation pattern, like many problems do", 
      "type": "status", 
      "created_time": "2014-10-03T02:07:19+0000", 
      "updated_time": "2014-10-03T02:07:19+0000"
    }, 

    {
      "id": "2359739457974250975madeup", 
      "from": {
        "id": "4363684063madeup", 
        "name": "John Smythe"
      }, 
      "to": {
        "data": [
          {
            "name": "Your Facebook Group", 
            "id": "432542543635453245madeup"
          }
        ]
      }, 
      "message": "Here is a fun link about programming", 
      "type": "status", 
      "created_time": "2014-10-02T20:12:28+0000", 
      "updated_time": "2014-10-02T20:12:28+0000"
    }]
   }

   # Here are some questions to help you. You don't need to comment answers to these, but we suggest doing so! They may help you think through this big nested data structure.
   # What type is the structure saved in the variable fb_data?
   # What type does the expression fb_data["data"] evaluate to?
   # What about fb_data["data"][1]?
   # What about fb_data["data"][0]["from"]?
   # What about fb_data["data"][0]["id"]?

   # Now write a line of code to assign the value of the first message in the big fb_data data structure to a variable called first_message. Do not hard code your answer! (Write it in terms of fb_data.)


   ====

   import test
   test.testEqual(first_message,fb_data["data"][0]["message"])


#. Here's a warm up exercise on defining and calling a function:

.. activecode:: ps_6_5

   # Define a function is_prefix that takes two strings and returns True if the
   # first one is a prefix of the second one, False otherwise.



   # Here's a couple example function calls, printing the return value to show you what it is.
   print is_prefix("He","Hello") # should print True
   print is_prefix("Hi","Hello") # should print False


#. Now, in the next few questions, you’ll build components and then a complete program that lets people play Hangman. Below is an image from the middle of a game...

.. image:: Figures/HangmanSample.JPG

See the flow chart[LINK] for a better understanding of what's happening in the code for the Hangman game overall.

The first task you have to build part of the Hangman game follows:

.. activecode:: ps_6_6

   # define the function blanked(). 
   # It takes a word and a string of letters that have been revealed.
   # It should return a string with the same number of characters as
   # the original word, but with the unrevealed characters replaced by _ 
         
   # a sample call to this function:
   print(blanked("Hello", "el"))
   #should output _ell_


#. The second task to build part of the Hangman game:

.. activecode:: ps_6_7

   # define the function health_prompt(). The first parameter is the current
   # health and the second is the the maximum health you can have. It should return a string 
   # with + signs for the current health, and - signs for the health that has been lost.




   print(health_prompt(3, 7))
   #this should produce the output
   #health: +++----

   print(health_prompt(0, 4))
   #this should produce the output
   #health: ----


#. Here's almost all of the Hangman game code. Paste your definition of the functions ``blanked`` and ``health_prompt`` at the start of this code. Then you can play when you run the program..! 

.. activecode:: ps_6_8

   # Here's where you should paste your function definitions.



   def game_state_prompt(txt, h, m_h, word, guesses):
       res = txt + "\n"
       res = res + health_prompt(h, m_h) + "\n"
       if guesses != "":
           res = res + "Guesses so far: " + guesses.upper() + "\n"
       else:
           res = res + "No guesses so far" + "\n"
       res = res + "Word: " + blanked(word, guesses) + "\n"

       return(res)

   def main():
       max_health = 3
       health = max_health
       secret_word = raw_input("What's the word to guess? (Don't let the player see it!)")
       secret_word = secret_word.upper() # everything in all capitals to avoid confusion
       guesses_so_far = ""
       game_over = False

       feedback = "let's get started"

       # Now interactively ask the user to guess
       while not game_over:
           # replace this comment with code that invokes game_state_prompt and assign the return value to the variable prompt
           prompt = game_state_prompt(feedback, health, max_health, secret_word, guesses_so_far)
           next_guess = raw_input(prompt)
           next_guess = next_guess.upper()
           feedback = ""
           if len(next_guess) != 1:
               feedback = "I only understand single letter guesses. Please try again."
           elif next_guess in guesses_so_far:
               feedback = "You already guessed that"
           else:
               guesses_so_far = guesses_so_far + next_guess
               if next_guess in secret_word:
                   if blanked(secret_word, guesses_so_far) == secret_word:
                       feedback = "Congratulations"
                       game_over = True
                   else:
                       feedback = "Yes, that letter is in the word"
               else: # next_guess is not in the word secret_word
                   feedback = "Sorry, " + next_guess + " is not in the word."
                   health = health - 1
                   if health <= 0:
                       feedback = " Waah, waah, waah. Game over."
                       game_over= True

       print(feedback)
       print("The word was..." + secret_word)

   import sys #don't worry about this line; you'll understand it next week
   sys.setExecutionLimit(60000)     # let the game take up to a minute, 60 * 1000 milliseconds
   main()


#. Look at the code for the Hangman game, below. (This code does NOT have your functions in it, so all the line numbers will be the same.) Then look at the flow chart. Write which lines of code go with which lines of the flow chart box, by answering the questions in comments below.

.. activecode:: ps_6_9

   # What line(s) of code do what's mentioned in box 1?

   # What line(s) of code do what's mentioned in box 2?

   # What line(s) of code do what's mentioned in box 3?

   # What line(s) of code do what's mentioned in box 4?

   # What line(s) of code do what's mentioned in box 5?

   # What line(s) of code do what's mentioned in box 6?

   # What line(s) of code do what's mentioned in box 7?

   # What line(s) of code do what's mentioned in box 8?

   # What line(s) of code do what's mentioned in box 9?
