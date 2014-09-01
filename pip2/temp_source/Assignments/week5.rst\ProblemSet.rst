..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Problem Set
-----------

**Due:** **Friday, February 7, 5 pm**

**Instructions:** Write the code you want to save in the provided boxes, and click **save** for each one. 
The last code you have saved for each one by the deadline is what will be graded.


1. (2 points) Warm up exercises on calling functions

.. tabbed:: q1

   .. tab:: Question

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

   
   .. tab:: Answer
 
       .. actex:: ps_4_1a
   
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
         print(add_em_up(range(21)))
         
         # Write code that invokes the longer function to determine
         # whether "supercalifragilisticexpialidocious" or "antidisestablishmentariansim" is longer
         print(longer("supercalifragilisticexpialidocious", "antidisestablishmentariansim"))    

2. (2 points) Warm up exercises on defining functions

.. tabbed:: q12

   .. tab:: Question
 
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
   
   .. tab:: Answer
   
      .. actex:: ps_4_2a
      
         # Define a function square that takes a number and returns that number multiplied by itself
         def square(x):
             return x*x
         
         # Define a function is_prefix that takes two strings and returns True if the
         # first one is a prefix of the second one, False otherwise.
         def is_prefix(x, y):
             if (len(x) <= len(y)):
                 return x == y[:len(x)]
             else:
                 return False         
                 
         print(square(3))
         #should be 9
         
         print(is_prefix("He", "Hello"))
         # should be True
         print(is_prefix("He", "I said Hello"))
         # should be False

In the next few questions, you'll build components and then a complete program
that lets people play Hangman. Below is an image from the middle of a game.

.. image:: Figures/HangmanSample.JPG

3. (2 points) Define the blanked function

.. tabbed:: q3

   .. tab:: Question

      .. actex:: ps_4_3
   
         # define the function blanked(). 
         # It takes a word and a string of letters that have been revealed.
         # It should return a string with the same number of characters as
         # the original word, but with the unrevealed characters replaced by _ 
               
         
         print(blanked("Hello", "el"))
         #should output _ell_
   
   .. tab:: Answer
   
   
      .. actex:: ps_4_3a
   
         # define the function blanked(). 
         # It takes a word and a string of letters that have been revealed.
         # It should return a string with the same number of characters as
         # the original word, but with the unrevealed characters replaced by _ 
               
         def blanked(word, revealed_letters):
             res = ""
             for c in word:
                 if c in revealed_letters:
                     res = res + c
                 else:
                     res = res + "_"
             return res
         
         print(blanked("Hello", "el"))
         #should output _ell_
   
4. (2 points) Define the health_prompt function

.. tabbed:: q4

   .. tab:: Question

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
   
   .. tab:: Answer
   
      .. actex:: ps_4_4a
   
         #define the function health_prompt(). The first parameter is the current
         #health and the second the maximum health. It should return a string with + signs for
         #the current health and - signs for the health that has been lost
         
         def health_prompt(h, max_h):
            remaining_h = max_h-h
            return("health: " + "+"*h + "-"*remaining_h) 
         
         
         print(health_prompt(3, 7))
         #this should produce the output
         #health: +++----
         
         print(health_prompt(0, 4))
         #this should produce the output
         #health: ----

     
5. (2 points) Cut and paste your two function definitions at the top of this code. Then replace the line with a comment that says to invoke the function game_state_prompt. Run the code to play the game with a friend! Feel free to change max_health if you want to make the game easier or harder to win. For fun, feel free to replace your output_health function with something that produces cool ASCII art of a hangman. (Try Googling "Hangman ASCII art".)

.. tabbed:: q5

   .. tab:: Question

      .. actex:: ps_4_5
   
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
   
   .. tab:: Answer
   
      .. actex:: ps_4_5a
   
         def health_prompt(h, max_h):
             remaining_h = max_h-h
             return("health: " + "+"*h + "-"*remaining_h) 
         
         def blanked(word, revealed_letters):
             res = ""
             for c in word:
                 if c in revealed_letters:
                     res = res + c
                 else:
                     res = res + "_"
             return res
         
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
                 prompt = game_state_prompt(feedback, health, max_health, to_guess, guesses_so_far)
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
         
         import sys #don't worry about this line; yo'll understand it next week
         sys.setExecutionLimit(60000)     # let the game take up to a minute, 60 * 1000 milliseconds
