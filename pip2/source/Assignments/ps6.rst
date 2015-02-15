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


Activities through 2/22
=======================

You have the following graded activities:

1. Class prep. Don't forget: always access the textbook by clicking on the Textbook link from cTools, so that you'll be logged in and get credit for doing the prep.
   
   * Before Monday's class: 
      * Read :ref:`Optional and Keyword Parameters<optional_params_chap>`, and do the exercises in that chapter
   
   * Before Wednesday's class:
       * Read :ref:`Tuples<tuples_chap>`, and do the exercises in that chapter
       * Read :ref:`Nested Data Structures and Nested Iteration<nested_chap>`, and do the exercises in that chapter
 
2. Reading responses

   * By Tuesday midnight: 
      * Read `Tutorial on unix diff <http://www.computerhope.com/unix/udiff.htm>`_ (This will help you understand the section of "The Most Human Human" below).
      * Read *The Most Human Human*, Chapter 10, p.237-259.
      * Answer :ref:`Reading Response 7 <reading_response_7>`. 

3. Problem set **Due:** **Sunday, February 22**

   * Save answers to the exercises in Problem Set 6: :ref:`Problem Set 6 <problem_set_6>` 



Reading Response
----------------

.. _reading_response_7:

1. Suppose you write and edit a long text file over the course of several days, saving a new version every 15 minutes or so (``myfile1.txt``, ``myfile2.txt``, ``myfile3.txt``,...). Eventually, you have 100 different versions of the file. Now consider the whole directory containing all 100 versions of the file. Would it have a lot of redundancy? As a compression technique, how might you take advantage of the unix diff command in order to reduce the total amount of space required to store all 100 versions of the file?

2. Think about assigning entropy scores to people instead of documents. If you were to compute information entropy scores for all the students you've met since enrolling at the University of Michigan, which of them has the highest entropy and why? 

.. activecode:: rr_7_1

   # Fill in your response in between the triple quotes
   s = """

   """
   print s


Problem Set
-----------

.. _problem_set_6:

.. note::

   This is a transition week, as we start to move toward writing complete programs in text files and running them from the command prompt, rather than working on several stand-alone problems in a browser. Starting with the next problem set, you won't be able to write and run code in the browser. This week, to help you see how the two ways of running code are related, you will write the code you have done it for previous problem sets, and then also copy your answers into a code file and make the code file run from the command line. Read to the bottom to see the instructions for what to submit via cTools, in addition to saving your code in the usual way in the browser. 


1. Write three function calls to the function ``give_greeting``: 

   * one that will return the string ``Hello, SI106!!!``
   * one that will return the string ``Hello, world!!!``
   * and one that will return the string ``Hey, everybody!`` 

You may print the return values of those function calls, but you do not have to.

You can see the function definition in the code below, but that's only so you can understand exactly what the code is doing so you can choose how to call this function. Feel free to make comments to help yourself understand, but otherwise DO NOT change the function definition code! HINT: calling the function in different ways and printing the results, to see what happens, may be helpful!

.. activecode:: ps_6_1
   
   def give_greeting(greet_word="Hello",name="SI106",num_exclam=3):
      final_string = greet_word + ", " + name + "!"*num_exclam
      return final_string

   #### DO NOT change the function definition above this line (OK to add comments)

   # Write your three function calls below


2. Define a function called mult_both whose input is two integers, whose default parameter values are the integers 3 and 4, and whose return value is the two input integers multiplied together.

.. activecode:: ps_6_2

   # Write your code here

   ====

   import test
   print "\n---\n\n"
   print "Testing whether your function works as expected (calling the function mult_both)"
   test.testEqual(mult_both(), 12)
   test.testEqual(mult_both(5,10), 50)


3. Use a for loop to print the second element of each tuple in the list ``new_tuple_list``.

.. activecode:: ps_6_3

      new_tuple_list = [(1,2),(4, "umbrella"),("chair","hello"),("soda",56.2)]



4. You can get data from Facebook that has nested structures which represent posts, or users, or various other types of things on Facebook. We won't put any of our actual Facebook group data on this textbook, because it's publicly available on the internet, but here's a structure that is almost exactly the same as the real thing, with fake data. 

Notice that the stuff in the variable ``fb_data`` is basically a big nested dictionary, with dictionaries and lists, strings and integers, inside it as keys and values. (Later in the course we'll learn how to get this kind of thing directly FROM facebook, and then it will be a bit more complicated and have real information from our Facebook group.)

Follow the directions in the comments!

.. activecode:: ps_6_4

      # first, look through the data structure saved in the variable fb_data to get a sense for it.

      fb_data = {
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

      # Here are some questions to help you. You don't need to 
      # comment answers to these (we won't grade your answers)
      # but we suggest doing so! They 
      # may help you think through this big nested data structure.
      
      # What type is the structure saved in the variable fb_data?
      # What type does the expression fb_data["data"] evaluate to?
      # What about fb_data["data"][1]?
      # What about fb_data["data"][0]["from"]?
      # What about fb_data["data"][0]["id"]?

      # Now write a line of code to assign the value of the first 
      # message ("This problem might...")  in the big fb_data data 
      # structure to a variable called first_message. Do not hard code your answer! 
      # (That is, write it in terms of fb_data, so that it would work
      # with any content stored in the variable fb_data that has
      # the same structure as that of the fb_data we gave you.)


      ====

      import test
      print "testing whether variable first_message was set correctly"
      test.testEqual(first_message,fb_data["data"][0]["message"])



5. Here's a warm up exercise on defining and calling a function:

.. activecode:: ps_6_5

      # Define a function is_prefix that takes two strings and returns 
      # True if the first one is a prefix of the second one, 
      # False otherwise.



      # Here's a couple example function calls, printing the return value 
      # to show you what it is.
      print is_prefix("He","Hello") # should print True
      print is_prefix("Hi","Hello") # should print False
      print is_prefix("lo","Hello") # should print False
      
      ====
      
      import test
      try:
        print 'testing whether "Big" is a prefix of "Bigger"'
        test.testEqual(is_prefix("Big", "Bigger"), True)
        print 'testing whether "Bigger" is a prefix of "Big"'
        test.testEqual(is_prefix("Bigger", "Big"), False)
        print 'testing whether "ge" is a prefix of "Bigger"'
        test.testEqual(is_prefix("ge","Bigger"))
      except:
        print "Looks like the function is_prefix has not been defined or has an error"


6. Write code that repeatedly asks the user to input numbers. Keep going until the sum of the numbers is 21 or more. Print out the total. 

.. activecode:: ps_6_6

    # Write your code here!


7. Now, in the next few questions, you’ll build components and then a complete program that lets people play Hangman. Below is an image from the middle of a game...

.. image:: Figures/HangmanSample.JPG

See the flow chart below for a better understanding of what's happening in the code for the Hangman game overall.

.. image:: Figures/HangmanFlowchart.jpg

Your first task is just to understand the logic of the program, by matching up elements of the flow chart above with elements of the code below. In later problems, you'll fill in a few details that aren't fully implemented here.  For this question, write which lines of code go with which lines of the flow chart box, by answering the questions in comments at the bottom of this activecode box. 

(Note: you may find it helpful to run this program in order to understand it. It will tell you feedback about your last guess, but won't tell you where the correct letters were or how much health you have. Those are the improvements you'll make in later problems.)

.. activecode:: ps_6_7

  def blanked(word, guesses):
      return "blanked word"

  def health_prompt(x, y):
      return "health prompt"

  def game_state_prompt(txt ="Nothing", h = 6, m_h = 6, word = "HELLO", guesses = ""):
      res = "\n" + txt + "\n"
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

  # What line(s) of code do what's mentioned in box 1?

  # What line(s) of code do what's mentioned in box 2?

  # What line(s) of code do what's mentioned in box 3?

  # What line(s) of code do what's mentioned in box 4?

  # What line(s) of code do what's mentioned in box 5?

  # What line(s) of code do what's mentioned in box 6?

  # What line(s) of code do what's mentioned in box 7?

  # What line(s) of code do what's mentioned in box 8?

  # What line(s) of code do what's mentioned in box 9?

  # What line(s) of code do what's mentioned in box 10?

  # What line(s) of code do what's mentioned in box 11?

         
8. The next task you have is to create a correct version of the blanked function:

.. activecode:: ps_6_8

    # define the function blanked(). 
    # It takes a word and a string of letters that have been revealed.
    # It should return a string with the same number of characters as
    # the original word, but with the unrevealed characters replaced by _ 
         
    # a sample call to this function:
    print(blanked("hello", "elj"))
    #should output _ell_

    ====

    import test
    try:
        print "testing blanking of hello when e,l, and j have been guessed"
        test.testEqual(blanked("hello", "elj"), "_ell_")
        print "testing blanking of hello when nothing has been guessed"
        test.testEqual(blanked("hello", ""), "_____")
        print "testing blanking of ground when r and n have been guessed"
        test.testEqual(blanked("ground", "rn"), "_r__n_")
    except:
        print "The function blanked has not been defined yet or has an error."


9. Now you have to create a good version of the health_prompt() function.

.. activecode:: ps_6_9

    # Define the function health_prompt(). The first parameter should be the current
    # health and the second should be the the maximum health you can have. It should return a string 
    # with + signs for the current health, and - signs for the health that has been lost.




    print health_prompt(3, 7)
    #this statement should produce the output
    #health: +++----

    print health_prompt(0, 4)
    #this statement should produce the output
    #health: ----

    ====

    import test
    try:
        print "testing health_prompt(3, 7)"
        test.testEqual(health_prompt(3,7), "+++----")
        print "testing health_prompt(0, 4)"
        test.testEqual(health_prompt(0, 4), "----")
    except:
        print "The function health_prompt is not defined or has an error"

   
10. Now you have a fully functioning hangman program! Copy your two function definitions for the last two problems at the top of this code box and try playing the game with your friends. ** There is no solution for this problem, because if you paste in the correct functions, it will work correctly! This one's for fun -- nothing to be graded here.**

.. activecode:: ps_6_10
   
    def game_state_prompt(txt ="Nothing", h = 6, m_h = 6, word = "HELLO", guesses = ""):
        res = "\n" + txt + "\n"
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


11. Now you have to copy all your answers into a single file and run that file from the command prompt. 

   * From cTools, look in the Assignments tab, at PS 6. 
      * download ps6.py into whatever directory on your local machine that you used last week for saving and running python files
      * download test106.py into that same directory (very important!)
      
   * Follow the instructions in ps6.py, which repeat the instructions for the problems above. Feel free to copy your code from the browser.

   * Run your program from the command prompt and make sure all the tests pass. Then uncomment the last line and take a screenshot showing that the hangman game is playing correctly.

   * Submit your .py file and the screenshot via cTools.
   
All done!