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

Week 5: ends February 7
=======================

For this week you have the following graded activities:

1. Do the multiple choice questions and exercises in the textbook chapters, including the ones at the bottom of the chapters, below the glossary. Don't forget to click **Save** for each of the exercises.

   * Before Tuesday's class:      
      * :ref:`Functions <functions_chap>` 
   
   * Before Thursday's class:
      * Local and global variables (not available yet)

#. Turn in the reading response, by 8 PM the night before your registered section meets.

   * Read *The Most Human Human*, Chapters 6 and 7
   * :ref:`Reading response 4 <response_4>`

#. Save answers to the exercises in Problem Set 4:

   * :ref:`Problem Set 4 <problem_set_4>`



.. _response_4:

Reading Response
----------------

**Due 8PM the night before your section meets**

Don't forget to click **save**.
   
Question 1. Is informatics a "Master Discipline" in the sense that Christian says Philosophy is? Why or why not?

.. actex:: rr_4_1

   # Fill in your response in between the triple quotes
   """

   """

Question 2. Have you ever faked being able to do something? Did you get caught? What helped you get caught/not get caught?

.. actex:: rr_4_2

   # Fill in your response in between the triple quotes
   """

   """

Question 3. What would you like to talk about in section this week?

.. actex:: rr_4_3

   # Fill in your response in between the triple quotes
   """

   """

.. _problem_set_4:

Problem Set
-----------

**Due:** **Friday, February 7, 5 pm**

**Instructions:** Write the code you want to save in the provided boxes, and click **save** for each one. 
The last code you have saved for each one by the deadline is what will be graded.


1. (2 points) Warm up exercises on calling functions

   .. actex:: ps_4_1

      def add_em_up(L):
         sum = 0
         for x in L:
            sum = sum + x
         return sum
         
      def longer(x, y):
         if len(x) > len(y):
            return x
         elif len(x) < len(y):
            return y
         else:
            return "same length"

      # Write code that invokes add_em_up in order to compute the sum of the
      # numbers from 1 through 20 (hint: try printing range(21))
      
      # Write code that invokes the longer function to determine 
      # whether "supercalifragilisticexpialidocious" or "antidisestablishmentariansim" is longer

#. (2 points) Warm up exercises on defining functions

   .. actex:: ps_4_2
   
      # Define a function square that takes a number and returns that number multiplied by itself
      
      # Define a function is_prefix that takes two strings and returns True if the 
      # first one is a prefix of the second one, False otherwise.
      
      print(square(3))
      #should be 9
      
      print(is_prefix("He", "Hello"))
      # should be True
      print(is_prefix("He", "I said Hello"))
      # should be False
   
#. (2 points) Define the blanked function

   .. actex:: ps_4_3

      # define the function blanked(). 
      # It takes a word and a string of letters that have been revealed.
      # It should return a string with the same number of characters as
      # the original word, but with the unrevealed characters replaced by _ 
            
      def blanked(word, revealed_letters):
      
      print(blanked("Hello", "el"))
      #should output _ell_
   
#. (2 points) Define the health_prompt function

   .. actex:: ps_4_4

      #define the function health_prompt(). The first parameter is the current
      #health and the second the maximum health. It should return a string with + signs for
      #the current health and - signs for the health that has been lost
      
      
      print(health_prompt(3, 7))
      #this should produce the output
      #health: +++----
      
      print(health_prompt(0, 4))
      #this should produce the output
      #health: ----

     
#. (2 points) Cut and paste your two function definitions at the top of this code. Then replace the line with a comment that says to invoke the function game_state_prompt. Run the code to play the game with a friend! Feel free to change max_health if you want to make the game easier or harder to win. For fun, feel free to replace your output_health function with something that produces cool ASCII art of a hangman. (Try Googling "Hangman ASCII art".)

   .. activecode:: ps_4_5

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
          to_guess = raw_input("What's the word to guess? (Don't let the player see it!)")
          to_guess = to_guess.upper() # everything in all capitals to avoid confusion
          guesses_so_far = ""
          game_over = False
      
          feedback = "let's get started"

          # Now interactively ask the user to guess
          while not game_over:
              # replace this comment with code that invokes game_state_prompt and assign the return value to the variable prompt
              next_guess = raw_input(prompt)
              next_guess = next_guess.upper()
              feedback = ""
              if len(next_guess) != 1:
                  feedback = "I only understand single letter guesses. Please try again."     
              elif next_guess in guesses_so_far:
                  feedback = "You already guessed that"
              else:
                  guesses_so_far = guesses_so_far + next_guess
                  if next_guess in to_guess:
                      if blanked(to_guess, guesses_so_far) == to_guess:
                          feedback = "Congratulations"
                          game_over = True
                      else:
                          feedback = "Yes, that letter is in the word"
                  else: # next_guess is not in the word to_guess
                      feedback = "Sorry, " + next_guess + " is not in the word."
                      health = health - 1
                      if health <= 0:
                          feedback = " Waah, waah, waah. Game over."
                          game_over= True
      
          print(feedback)
          print("The word was..." + to_guess)
      
      import sys #don't worry about this line; you'll understand it next week
      sys.setExecutionLimit(60000)     # let the game take up to a minute, 60 * 1000 milliseconds
      main()      
   
    