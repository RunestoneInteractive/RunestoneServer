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


Week 6: ends February 14
========================

For this week you have the following graded activities:

1. Do the multiple choice questions and exercises in the textbook chapters, including the ones at the bottom of the chapters, below the glossary. Don't forget to click **Save** for each of the exercises.

   * Before Tuesday's class:      
      * :ref:`Optional Parameters <optional_pararams_chap>`
      * :ref:`Tuples <tuples_chap>`
      * :ref:`Sorting <invoking_sort_chap>`
   
   * Before Thursday's class:
      * :ref:`Import Modules <modules_chap>`
      * :ref:`Test cases <simple_tests_chap>`
      * :ref:`Print vs. Return <print_vs_return>`


#. Turn in the reading response, by 8 PM the night before your registered section meets.

   * Read *The Most Human Human*, Chapters 8 and 9
   * :ref:`Reading response 5 <response_5>`

#. Save answers to the exercises in Problem Set 5:

   * :ref:`Problem Set 5 <problem_set_5>` (Coming soon.)

#. Supplemental exercises:

   * :ref:`In-class exercises Tuesday <session_10>`
   * :ref:`In-class exercises Thursday <session_11>`
   * :ref:`Exercise from discussion section <functions_review_5>`

.. _response_5:

Reading Response
----------------

**Due 8PM the night before your section meets**

Don't forget to click **save**.
   
Question 1. What is an example of a "maximax" conversation you've recently had? Explain (briefly).

.. actex:: rr_5_1

   # Fill in your response in between the triple quotes
   """

   """

Question 2. How would you instruct a computer to "get to know" a person? (Feel free to refer to topics from earlier weeks of discussion as well.)

.. actex:: rr_5_2

   # Fill in your response in between the triple quotes
   """

   """

Question 3. What's something from these chapters you found particularly interesting? Why? What would you like to address in section this week?

.. actex:: rr_5_3

   # Fill in your response in between the triple quotes
   """

   """




.. _problem_set_5:

Problem Set 5
-------------

This problem set builds from the previous problem set's solution. You will write
code that makes the next guess in a hangman game, instead of having a person do it.

A version of the **guess** function is provided. It picks a random letter from the alphabet and guesses it if (even if it was guessed previously!) But with more information, we can change the function to make a better guess that is more likely to be in the word.

You will have to write a new function, **better_guess**. The problem set will walk you through making a series of improvements to the
guess function. 

First, take a look at the game function that is provided.

Note that when game is called, no parameter values are provided, and so the default
values are used. With the parameter **manual** set to (assigned the value) True, lots of feedback is given and the user has to click OK to initiate each guess. 

But without the argument **manual** being set to (assigned the value) True, the game runs till it is completed, and only two things are returned: the number of guesses used and the minimum number of guesses that could have been used.

With the argument **better** set to False, the **guess** function, which is already defined in the provided code, is called. If the argument **better** is set to True, a different function (that you will define in a later exercise) will get called instead.

Try passing some different parameter values in the invocation of the function **game**, in order to see how it works. Remember, a function invocation is the same as a function call. (Remember the last problem in Problem Set 4 and all the examples from the textbook?)

In the code windows below, there is a big chunk of code that is provided to you that you should **not change**, except perhaps to add some print statements temporarily to figure out what it's doing. 

1. (1 point) Change the invocation of the function game at the bottom of the code below, so that the maximum number of wrong guesses is 3. 

.. actex:: ps5_1
    
    #### Don't change any of this provided code ######
    
    def guess(blanked, guessed_already, manual = True):
        """Return a single letter (upper case)"""
        # Initial version picks a letter completely at random,
        # without taking advantage of information from
        # blanked or what was guessed already
        alphabet = "abcdefghijklmnopqrstuvwxyz".upper()
        idx = random.randrange(0, 26)
        if manual:
            print("guess is " + alphabet[idx])
        return alphabet[idx]
        
    all_words = []
    f = open('words.txt', 'r')
    for l in f:
        all_words.append(l.strip().upper())
    f.close()
    
    import random
    
    
    def blanked(to_guess, revealed_letters):
        """Teturns blanked version of to_guess, with only revealed_letters showing""" 
        s = ""
        for ch in to_guess:
            if ch in revealed_letters:
                s += ch
            else:
                s += "_"
        return s
    
    def health_prompt(c_h, m_h):
        """Text representation of current health"""
        pos, rem = "+"*c_h, m_h - c_h
        return pos + "-"*rem
    
    def show_results(word, guess_count):
        """Results to show at end of game"""
        print "You got it in " + str(guess_count) + " guesses."
        if guess_count == len(set(list(word))):
            print "Awesome job."
        else:
            print "You could have gotten it in " + str(len(set(list(word)))) + " guesses..."
    
    def game_state_prompt(txt, h, m_h, word, guesses):
        """Returns a string showing current status of the game"""
        res = txt + "\n"
        res = res + health_prompt(h, m_h) + "\n"
        if guesses != "":
            res = res + "Guesses so far: " + guesses.upper() + "\n"
        else:
            res = res + "No guesses so far" + "\n"
        res = res + "Word: " + blanked(word, guesses) + "\n"
        return(res)
    
    #### GAMEPLAY
    
          
    def game(manual=True, better=False, max_health = 26):
        """Plays one game"""
        health = max_health
        to_guess = random.choice(all_words)
        to_guess = to_guess.upper() # everything in all capitals to avoid confusion
        guesses_so_far = ""
        game_over = False
    
        feedback = "let's get started"
    
        while not game_over:
            if manual:
                # give user a chance to see what happened on previous guess
                prompt = game_state_prompt(feedback, health, max_health, to_guess, guesses_so_far)
                full_prompt = prompt + "Enter (OK) to make the program guess again; anything else to quit\n"
                command = raw_input(full_prompt)
                if command != "":
                    # user entered a character, so (s)he wants to stop the game
                    return
            # call your function guess to pick a next letter
            if better:
                # call better_guess, which you will have to implement
                next_guess = better_guess(blanked(to_guess, guesses_so_far), guesses_so_far, manual)
            else:
                # call guess, which is provided
                next_guess = guess(blanked(to_guess, guesses_so_far), guesses_so_far, manual)
            # proceed as with last week to process the next_guess
            feedback = ""
            if len(next_guess) != 1:
                feedback = "I only understand single letter guesses. Please try again."     
            elif next_guess in guesses_so_far:
                feedback = "You already guessed " + next_guess
            else:
                guesses_so_far = guesses_so_far + next_guess
                if next_guess in to_guess:
                    if blanked(to_guess, guesses_so_far) == to_guess:
                        feedback = "Congratulations"
                        game_over = True
                    else:
                        feedback = "Yes, " + next_guess + " is in the word"
                else: # next_guess is not in the word to_guess
                    feedback = "Sorry, " + next_guess + " is not in the word."
                    health = health - 1
                    if health <= 0:
                        feedback = " Waah, waah, waah. Game over."
                        game_over= True
    
        if manual:
            # this is outside the for loop; executes once game_over is True
            print(feedback)
            print("The word was..." + to_guess)
            show_results(to_guess, len(guesses_so_far))
        
        return len(guesses_so_far), len(set(list(to_guess)))
        
    import sys 
    sys.setExecutionLimit(60000)     # let the game take up to a minute, 60 * 1000 milliseconds
    
    ###### Don't change code above this line; just read and understand it #####
    
    # Run this. Then change this call so that a game is played with a maximum of 3 wrong guesses 
    # before the game ends.
    game()

2. (2 points) Compute the average performance over many plays of the game.

Instead of playing the game once, you can get a better sense of the guesser's 
average performance by having it play the game many times. Write code to
run the game many times. Add up the total number of guesses it makes, and the
minimum number of guesses it could have made. Print out the ratio. The closer to 1,
the better your guesser.

(Hint: you will go crazy clicking OK forever unless you set the manual parameter to False in your
calls to the function game.)
    
.. actex:: ps5_2

    #### Don't change any of this provided code ######
    
    def guess(blanked, guessed_already, manual = True):
        """Return a single letter (upper case)"""
        # Initial version picks a letter completely at random,
        # without taking advantage of information from
        # blanked or what was guessed already
        alphabet = "abcdefghijklmnopqrstuvwxyz".upper()
        idx = random.randrange(0, 26)
        if manual:
            print("guess is " + alphabet[idx])
        return alphabet[idx]
        
    all_words = []
    f = open('words.txt', 'r')
    for l in f:
        all_words.append(l.strip().upper())
    f.close()
    
    import random
    
    
    def blanked(to_guess, revealed_letters):
        """Teturns blanked version of to_guess, with only revealed_letters showing""" 
        s = ""
        for ch in to_guess:
            if ch in revealed_letters:
                s += ch
            else:
                s += "_"
        return s
    
    def health_prompt(c_h, m_h):
        """Text representation of current health"""
        pos, rem = "+"*c_h, m_h - c_h
        return pos + "-"*rem
    
    def show_results(word, guess_count):
        """Results to show at end of game"""
        print "You got it in " + str(guess_count) + " guesses."
        if guess_count == len(set(list(word))):
            print "Awesome job."
        else:
            print "You could have gotten it in " + str(len(set(list(word)))) + " guesses..."
    
    def game_state_prompt(txt, h, m_h, word, guesses):
        """Returns a string showing current status of the game"""
        res = txt + "\n"
        res = res + health_prompt(h, m_h) + "\n"
        if guesses != "":
            res = res + "Guesses so far: " + guesses.upper() + "\n"
        else:
            res = res + "No guesses so far" + "\n"
        res = res + "Word: " + blanked(word, guesses) + "\n"
        return(res)
    
    #### GAMEPLAY
    
          
    def game(manual=True, better=False, max_health = 26):
        """Plays one game"""
        health = max_health
        to_guess = random.choice(all_words)
        to_guess = to_guess.upper() # everything in all capitals to avoid confusion
        guesses_so_far = ""
        game_over = False
    
        feedback = "let's get started"
    
        while not game_over:
            if manual:
                # give user a chance to see what happened on previous guess
                prompt = game_state_prompt(feedback, health, max_health, to_guess, guesses_so_far)
                full_prompt = prompt + "Enter (OK) to make the program guess again; anything else to quit\n"
                command = raw_input(full_prompt)
                if command != "":
                    # user entered a character, so (s)he wants to stop the game
                    return
            # call your function guess to pick a next letter
            if better:
                # call better_guess, which you will have to implement
                next_guess = better_guess(blanked(to_guess, guesses_so_far), guesses_so_far, manual)
            else:
                # call guess, which is provided
                next_guess = guess(blanked(to_guess, guesses_so_far), guesses_so_far, manual)
            # proceed as with last week to process the next_guess
            feedback = ""
            if len(next_guess) != 1:
                feedback = "I only understand single letter guesses. Please try again."     
            elif next_guess in guesses_so_far:
                feedback = "You already guessed " + next_guess
            else:
                guesses_so_far = guesses_so_far + next_guess
                if next_guess in to_guess:
                    if blanked(to_guess, guesses_so_far) == to_guess:
                        feedback = "Congratulations"
                        game_over = True
                    else:
                        feedback = "Yes, " + next_guess + " is in the word"
                else: # next_guess is not in the word to_guess
                    feedback = "Sorry, " + next_guess + " is not in the word."
                    health = health - 1
                    if health <= 0:
                        feedback = " Waah, waah, waah. Game over."
                        game_over= True
    
        if manual:
            # this is outside the for loop; executes once game_over is True
            print(feedback)
            print("The word was..." + to_guess)
            show_results(to_guess, len(guesses_so_far))
        
        return len(guesses_so_far), len(set(list(to_guess)))
        
    import sys 
    sys.setExecutionLimit(60000)     # let the game take up to a minute, 60 * 1000 milliseconds
    
    ###### Don't change code above this line; just read and understand it #####
    
    # write code to call game 50 times and compute the average performance

3. (1 point) Compute letter frequencies.

Now let's start building a better guesser. The initiall guess function selects
a random letter, without looking at all at blanked or its previous guesses. One obvious 
thing to do is to guess letters that occur more frequently. 

For this exercise, you will take the first step toward that. Here your job is to define a function
letter_frequencies. It takes a list of strings (words) as an input. As an output
it produces a dictionary with a key for each letter that appears in any of the
words. The value associated with each letter is the count of how many times the
letter appears in any of the words.

We have included some hidden code that runs unit tests on your function. If your
function is not producing the right outputs, it will give you some diagnostic
messages.


.. actex:: ps5_3

    def letter_frequencies(...fill this in...
    
    
    #####some tests 
    import test    
    test_words = ["HELLO", "GOODBYE", "LOVE", "PEACE"]
    r = letter_frequencies(test_words)
    # letter_frequencies should return a dictionary
    test.testEqual(type(r), type({}))
    test.testEqual(r['C'], 1)
    test.testEqual(r['O'], 4)    
    

4. (2 points) Use letter_frequencies to make better guesses. Fill in details of the better_guess function as indicated in the comments.


.. actex:: ps5_4

        #### Don't change any of this provided code ######
    
    def guess(blanked, guessed_already, manual = True):
        """Return a single letter (upper case)"""
        # Initial version picks a letter completely at random,
        # without taking advantage of information from
        # blanked or what was guessed already
        alphabet = "abcdefghijklmnopqrstuvwxyz".upper()
        idx = random.randrange(0, 26)
        if manual:
            print("guess is " + alphabet[idx])
        return alphabet[idx]
        
    all_words = []
    f = open('words.txt', 'r')
    for l in f:
        all_words.append(l.strip().upper())
    f.close()
    
    import random
    
    
    def blanked(to_guess, revealed_letters):
        """Teturns blanked version of to_guess, with only revealed_letters showing""" 
        s = ""
        for ch in to_guess:
            if ch in revealed_letters:
                s += ch
            else:
                s += "_"
        return s
    
    def health_prompt(c_h, m_h):
        """Text representation of current health"""
        pos, rem = "+"*c_h, m_h - c_h
        return pos + "-"*rem
    
    def show_results(word, guess_count):
        """Results to show at end of game"""
        print "You got it in " + str(guess_count) + " guesses."
        if guess_count == len(set(list(word))):
            print "Awesome job."
        else:
            print "You could have gotten it in " + str(len(set(list(word)))) + " guesses..."
    
    def game_state_prompt(txt, h, m_h, word, guesses):
        """Returns a string showing current status of the game"""
        res = txt + "\n"
        res = res + health_prompt(h, m_h) + "\n"
        if guesses != "":
            res = res + "Guesses so far: " + guesses.upper() + "\n"
        else:
            res = res + "No guesses so far" + "\n"
        res = res + "Word: " + blanked(word, guesses) + "\n"
        return(res)
    
    #### GAMEPLAY
    
          
    def game(manual=True, better=False, max_health = 26):
        """Plays one game"""
        health = max_health
        to_guess = random.choice(all_words)
        to_guess = to_guess.upper() # everything in all capitals to avoid confusion
        guesses_so_far = ""
        game_over = False
    
        feedback = "let's get started"
    
        while not game_over:
            if manual:
                # give user a chance to see what happened on previous guess
                prompt = game_state_prompt(feedback, health, max_health, to_guess, guesses_so_far)
                full_prompt = prompt + "Enter (OK) to make the program guess again; anything else to quit\n"
                command = raw_input(full_prompt)
                if command != "":
                    # user entered a character, so (s)he wants to stop the game
                    return
            # call your function guess to pick a next letter
            if better:
                # call better_guess, which you will have to implement
                next_guess = better_guess(blanked(to_guess, guesses_so_far), guesses_so_far, manual)
            else:
                # call guess, which is provided
                next_guess = guess(blanked(to_guess, guesses_so_far), guesses_so_far, manual)
            # proceed as with last week to process the next_guess
            feedback = ""
            if len(next_guess) != 1:
                feedback = "I only understand single letter guesses. Please try again."     
            elif next_guess in guesses_so_far:
                feedback = "You already guessed " + next_guess
            else:
                guesses_so_far = guesses_so_far + next_guess
                if next_guess in to_guess:
                    if blanked(to_guess, guesses_so_far) == to_guess:
                        feedback = "Congratulations"
                        game_over = True
                    else:
                        feedback = "Yes, " + next_guess + " is in the word"
                else: # next_guess is not in the word to_guess
                    feedback = "Sorry, " + next_guess + " is not in the word."
                    health = health - 1
                    if health <= 0:
                        feedback = " Waah, waah, waah. Game over."
                        game_over= True
    
        if manual:
            # this is outside the for loop; executes once game_over is True
            print(feedback)
            print("The word was..." + to_guess)
            show_results(to_guess, len(guesses_so_far))
        
        return len(guesses_so_far), len(set(list(to_guess)))
        
    import sys 
    sys.setExecutionLimit(60000)     # let the game take up to a minute, 60 * 1000 milliseconds
    
    ###### Don't change code above this line; just read and understand it #####
        
    # copy your letter_frequencies function here

    def possible_words(blanked_word, guessed_already, possible_ws = all_words):
        return possible_ws

    def better_guess(blanked, guessed_already, manual = False):
        freqs = letter_frequencies(possible_words(blanked, guessed_already))
        counts = freqs.items()
        # sort the pairs in counts so that the letter with the highest 
        # count appears first
        
        # return the letter that has the highest count that is not in guessed_already
        # (and print it out if manual is True)       

   
    ###some test cases###
    import test
    res = better_guess("H___O", "HOWQA")
    # should return a string
    test.testEqual(type(res), type(""))
    test.testEqual(len(res), 1)
    res = better_guess("HE__O", "HOWQAEN")
    test.testEqual(res, "S")

5. (3 points) Make a better version of possible words

Once you have made some guesses, not all of the words are still possible. For starters,
words that are longer or shorter than the blanked word are not possible.
Second, if you have guessed a letter that it's in the word, then only 
words containing that letter are still possible (actually, only words that have
that letter in the right place). Finally, if you have guessed a letter that's not
in the word, then only words that don't contain that letter are still possible.
Revise the possible_words function so that it returns a shorter list of possible
words (without removing any that are still possible.)

There are some hidden test cases that will give you feedback on how well you're doing.
If you don't manage to get exactly the number we got, you can still go on and 
let the graders figure it out, but most likely you've got an error.

.. actex:: ps5_5 

        #### Don't change any of this provided code ######
    
    def guess(blanked, guessed_already, manual = True):
        """Return a single letter (upper case)"""
        # Initial version picks a letter completely at random,
        # without taking advantage of information from
        # blanked or what was guessed already
        alphabet = "abcdefghijklmnopqrstuvwxyz".upper()
        idx = random.randrange(0, 26)
        if manual:
            print("guess is " + alphabet[idx])
        return alphabet[idx]
        
    all_words = []
    f = open('words.txt', 'r')
    for l in f:
        all_words.append(l.strip().upper())
    f.close()
    
    import random
    
    
    def blanked(to_guess, revealed_letters):
        """Teturns blanked version of to_guess, with only revealed_letters showing""" 
        s = ""
        for ch in to_guess:
            if ch in revealed_letters:
                s += ch
            else:
                s += "_"
        return s
    
    def health_prompt(c_h, m_h):
        """Text representation of current health"""
        pos, rem = "+"*c_h, m_h - c_h
        return pos + "-"*rem
    
    def show_results(word, guess_count):
        """Results to show at end of game"""
        print "You got it in " + str(guess_count) + " guesses."
        if guess_count == len(set(list(word))):
            print "Awesome job."
        else:
            print "You could have gotten it in " + str(len(set(list(word)))) + " guesses..."
    
    def game_state_prompt(txt, h, m_h, word, guesses):
        """Returns a string showing current status of the game"""
        res = txt + "\n"
        res = res + health_prompt(h, m_h) + "\n"
        if guesses != "":
            res = res + "Guesses so far: " + guesses.upper() + "\n"
        else:
            res = res + "No guesses so far" + "\n"
        res = res + "Word: " + blanked(word, guesses) + "\n"
        return(res)
    
    #### GAMEPLAY
    
          
    def game(manual=True, better=False, max_health = 26):
        """Plays one game"""
        health = max_health
        to_guess = random.choice(all_words)
        to_guess = to_guess.upper() # everything in all capitals to avoid confusion
        guesses_so_far = ""
        game_over = False
    
        feedback = "let's get started"
    
        while not game_over:
            if manual:
                # give user a chance to see what happened on previous guess
                prompt = game_state_prompt(feedback, health, max_health, to_guess, guesses_so_far)
                full_prompt = prompt + "Enter (OK) to make the program guess again; anything else to quit\n"
                command = raw_input(full_prompt)
                if command != "":
                    # user entered a character, so (s)he wants to stop the game
                    return
            # call your function guess to pick a next letter
            if better:
                # call better_guess, which you will have to implement
                next_guess = better_guess(blanked(to_guess, guesses_so_far), guesses_so_far, manual)
            else:
                # call guess, which is provided
                next_guess = guess(blanked(to_guess, guesses_so_far), guesses_so_far, manual)
            # proceed as with last week to process the next_guess
            feedback = ""
            if len(next_guess) != 1:
                feedback = "I only understand single letter guesses. Please try again."     
            elif next_guess in guesses_so_far:
                feedback = "You already guessed " + next_guess
            else:
                guesses_so_far = guesses_so_far + next_guess
                if next_guess in to_guess:
                    if blanked(to_guess, guesses_so_far) == to_guess:
                        feedback = "Congratulations"
                        game_over = True
                    else:
                        feedback = "Yes, " + next_guess + " is in the word"
                else: # next_guess is not in the word to_guess
                    feedback = "Sorry, " + next_guess + " is not in the word."
                    health = health - 1
                    if health <= 0:
                        feedback = " Waah, waah, waah. Game over."
                        game_over= True
    
        if manual:
            # this is outside the for loop; executes once game_over is True
            print(feedback)
            print("The word was..." + to_guess)
            show_results(to_guess, len(guesses_so_far))
        
        return len(guesses_so_far), len(set(list(to_guess)))
        
    import sys 
    sys.setExecutionLimit(60000)     # let the game take up to a minute, 60 * 1000 milliseconds
    
    ###### Don't change code above this line; just read and understand it #####
    
    def possible_words(blanked_word, guessed_already, possible_ws = all_words):
        return possible_ws # replace this with something better



    #### Some comments #####
    import test
    
    res = possible_words("H___O", "HOWQA")
    #should return a list of strings
    test.testEqual(type(res), type([]))
    test.testEqual(type(res[0]), type(""))
    test.testEqual(len(res), 54)
    
    


6. (1 point) Put it all together

.. actex:: ps5_6

        #### Don't change any of this provided code ######
    
    def guess(blanked, guessed_already, manual = True):
        """Return a single letter (upper case)"""
        # Initial version picks a letter completely at random,
        # without taking advantage of information from
        # blanked or what was guessed already
        alphabet = "abcdefghijklmnopqrstuvwxyz".upper()
        idx = random.randrange(0, 26)
        if manual:
            print("guess is " + alphabet[idx])
        return alphabet[idx]
        
    all_words = []
    f = open('words.txt', 'r')
    for l in f:
        all_words.append(l.strip().upper())
    f.close()
    
    import random
    
    
    def blanked(to_guess, revealed_letters):
        """Teturns blanked version of to_guess, with only revealed_letters showing""" 
        s = ""
        for ch in to_guess:
            if ch in revealed_letters:
                s += ch
            else:
                s += "_"
        return s
    
    def health_prompt(c_h, m_h):
        """Text representation of current health"""
        pos, rem = "+"*c_h, m_h - c_h
        return pos + "-"*rem
    
    def show_results(word, guess_count):
        """Results to show at end of game"""
        print "You got it in " + str(guess_count) + " guesses."
        if guess_count == len(set(list(word))):
            print "Awesome job."
        else:
            print "You could have gotten it in " + str(len(set(list(word)))) + " guesses..."
    
    def game_state_prompt(txt, h, m_h, word, guesses):
        """Returns a string showing current status of the game"""
        res = txt + "\n"
        res = res + health_prompt(h, m_h) + "\n"
        if guesses != "":
            res = res + "Guesses so far: " + guesses.upper() + "\n"
        else:
            res = res + "No guesses so far" + "\n"
        res = res + "Word: " + blanked(word, guesses) + "\n"
        return(res)
    
    #### GAMEPLAY
    
          
    def game(manual=True, better=False, max_health = 26):
        """Plays one game"""
        health = max_health
        to_guess = random.choice(all_words)
        to_guess = to_guess.upper() # everything in all capitals to avoid confusion
        guesses_so_far = ""
        game_over = False
    
        feedback = "let's get started"
    
        while not game_over:
            if manual:
                # give user a chance to see what happened on previous guess
                prompt = game_state_prompt(feedback, health, max_health, to_guess, guesses_so_far)
                full_prompt = prompt + "Enter (OK) to make the program guess again; anything else to quit\n"
                command = raw_input(full_prompt)
                if command != "":
                    # user entered a character, so (s)he wants to stop the game
                    return
            # call your function guess to pick a next letter
            if better:
                # call better_guess, which you will have to implement
                next_guess = better_guess(blanked(to_guess, guesses_so_far), guesses_so_far, manual)
            else:
                # call guess, which is provided
                next_guess = guess(blanked(to_guess, guesses_so_far), guesses_so_far, manual)
            # proceed as with last week to process the next_guess
            feedback = ""
            if len(next_guess) != 1:
                feedback = "I only understand single letter guesses. Please try again."     
            elif next_guess in guesses_so_far:
                feedback = "You already guessed " + next_guess
            else:
                guesses_so_far = guesses_so_far + next_guess
                if next_guess in to_guess:
                    if blanked(to_guess, guesses_so_far) == to_guess:
                        feedback = "Congratulations"
                        game_over = True
                    else:
                        feedback = "Yes, " + next_guess + " is in the word"
                else: # next_guess is not in the word to_guess
                    feedback = "Sorry, " + next_guess + " is not in the word."
                    health = health - 1
                    if health <= 0:
                        feedback = " Waah, waah, waah. Game over."
                        game_over= True
    
        if manual:
            # this is outside the for loop; executes once game_over is True
            print(feedback)
            print("The word was..." + to_guess)
            show_results(to_guess, len(guesses_so_far))
        
        return len(guesses_so_far), len(set(list(to_guess)))
        
    import sys 
    sys.setExecutionLimit(60000)     # let the game take up to a minute, 60 * 1000 milliseconds
    
    ###### Don't change code above this line; just read and understand it #####
    
        
    # paste your letter_frequencies, better_guess, and possible_words functions here
    
    # paste two copies of your code for computing, over 50 games, the ratio of 
    # guesses to min_guesses. 
    # Modify one copy to invoke game() in a way that better_guess will be used
    # instead of guess. 
    #
    # Note: a game using better_guess might take a while to
    # run. To improve performance, we've given you a smaller dictionary of words
    # for this exercise. You might want to try running it on just 1 or 5 of 10
    # games before you run it on all 50, to make sure it's working.  
    
    # How much better did you do using better_guess?
        
.. datafile::  words.txt
   :hide:

    AARGH
    ABACI
    ABAKAS
    ABASE
    ABASH
    ABASING
    ABATES
    ABATTIS
    ABBACY
    ABBEYS
    ABDUCE
    ABEAM
    ABELIAS
    ABETTOR
    ABHORS
    ABIDES
    ABIOSIS
    ABJURER
    ABLATOR
    ABLEISM
    ABLINGS
    ABLUTED
    ABODED
    ABOIL
    ABOMAS
    ABORT
    ABOUGHT
    ABOUT
    ABRADER
    ABRIS
    ABSCESS
    ABSENCE
    ABSORB
    ABUBBLE
    ABUSED
    ABUSIVE
    ABUZZ
    ABYES
    ABYSS
    ACADEME
    ACANTHA
    ACARIDS
    ACCEDE
    ACCENTS
    ACCIDIE
    ACCOSTS
    ACCRUED
    ACCUSED
    ACEQUIA
    ACEROLA
    ACETALS
    ACETINS
    ACETYL
    ACHES
    ACHIOTE
    ACIDIC
    ACIDY
    ACINIC
    ACKEES
    ACNED
    ACOLD
    ACORNS
    ACRASIA
    ACRID
    ACROMIA
    ACRYLIC
    ACTING
    ACTINS
    ACTOR
    ACTUARY
    ACULEUS
    ACUTER
    ACYLOIN
    ADAGIO
    ADAPTER
    ADDAX
    ADDENDA
    ADDICT
    ADDLES
    ADDUCED
    ADEEM
    ADENOMA
    ADEPTLY
    ADHERES
    ADIOS
    ADJOIN
    ADJUNCT
    ADJUROR
    ADMEN
    ADMIRES
    ADMIXES
    ADNOUN
    ADOBOS
    ADOPTER
    ADORERS
    ADORNER
    ADRIFT
    ADULT
    ADVANCE
    ADVERB
    ADVICE
    ADVISER
    ADYTA
    ADZUKI
    AECIUM
    AEGIS
    AEONIAN
    AERATES
    AERIED
    AERILY
    AEROBIC
    AERUGOS
    AFEARED
    AFFAIRS
    AFFINAL
    AFFIRMS
    AFFIXES
    AFFRAY
    AFGHANS
    AFOOT
    AFREETS
    AFTERS
    AGAINST
    AGAMID
    AGAPE
    AGAROSE
    AGATOID
    AGEING
    AGEISTS
    AGENDA
    AGENIZE
    AGERS
    AGGADOT
    AGGRADE
    AGHAST
    AGINGS
    AGIST
    AGITATE
    AGLET
    AGMAS
    AGNATIC
    AGNOSIA
    AGONIES
    AGONY
    AGOROTH
    AGRAFES
    AGREED
    AGUES
    AHIMSAS
    AHULL
    AIDES
    AIDMEN
    AIKIDO
    AILMENT
    AIMING
    AIRBAG
    AIRDATE
    AIREST
    AIRHEAD
    AIRING
    AIRLINE
    AIRPARK
    AIRSHIP
    AIRTH
    AIRTS
    AIRWISE
    AITCHES
    AJOWAN
    AKELA
    AKVAVIT
    ALAMOS
    ALANIN
    ALANTS
    ALARMS
    ALASKAS
    ALATION
    ALBEDOS
    ALBINOS
    ALBUM
    ALCADES
    ALCAYDE
    ALCIDS
    ALDER
    ALDOSES
    ALEGAR
    ALEPHS
    ALERTS
    ALEXIA
    ALFAKI
    ALFORJA
    ALGEBRA
    ALGOR
    ALIASES
    ALIBLE
    ALIENED
    ALIENS
    ALIGN
    ALIMENT
    ALINERS
    ALIQUOT
    ALIYAH
    ALKALI
    ALKANES
    ALKIES
    ALKYDS
    ALKYNES
    ALLEE
    ALLEGES
    ALLERGY
    ALLIED
    ALLOD
    ALLOT
    ALLOWS
    ALLSEED
    ALLURED
    ALLYL
    ALMANAC
    ALMES
    ALMONDY
    ALMSMEN
    ALMUDES
    ALNICOS
    ALOETIC
    ALOINS
    ALOUD
    ALPHORN
    ALREADY
    ALTARS
    ALTHAEA
    ALTOIST
    ALULAE
    ALUMINS
    ALUMS
    ALWAYS
    AMAIN
    AMASS
    AMATIVE
    AMAZED
    AMBAGE
    AMBEER
    AMBIENT
    AMBLER
    AMBONES
    AMBRY
    AMEBAN
    AMEER
    AMENDS
    AMENTS
    AMESACE
    AMICES
    AMIDES
    AMIDO
    AMIDST
    AMIGOS
    AMINO
    AMITIES
    AMMINO
    AMMOS
    AMNIC
    AMNIOTE
    AMOEBIC
    AMONGST
    AMOROSO
    AMOUNT
    AMPERE
    AMPLER
    AMPUL
    AMPUTEE
    AMTRACK
    AMULETS
    AMUSES
    AMYLASE
    AMYLS
    ANADEMS
    ANAGRAM
    ANALOGS
    ANALYZE
    ANARCH
    ANATTO
    ANCHOS
    ANCON
    ANDANTE
    ANEAR
    ANELES
    ANEMONE
    ANERGY
    ANGAKOK
    ANGELED
    ANGERED
    ANGINAS
    ANGLERS
    ANGLOS
    ANGRY
    ANGULAR
    ANILINS
    ANIMAL
    ANIME
    ANIMIST
    ANISE
    ANKHS
    ANKLETS
    ANLACE
    ANLAS
    ANNATES
    ANNEX
    ANNONAS
    ANNUAL
    ANNULET
    ANODAL
    ANODYNE
    ANOLYTE
    ANOMY
    ANOPSIA
    ANOSMIC
    ANSAE
    ANTACID
    ANTEED
    ANTHEM
    ANTHOID
    ANTIBUG
    ANTICLY
    ANTIFUR
    ANTILOG
    ANTIQUE
    ANTITAX
    ANTLION
    ANTRES
    ANURAL
    ANURIC
    ANVILS
    ANYMORE
    ANYWAY
    AORTA
    AOUDAD
    APAGOGE
    APATITE
    APERCUS
    APEXES
    APHESES
    APHIDS
    APHTHA
    APICAL
    APING
    APLITE
    APNEA
    APNOEAL
    APODAL
    APOGEAN
    APOLLOS
    APOMICT
    APOSTLE
    APPALS
    APPEAR
    APPEND
    APPLET
    APPLY
    APPOSES
    APRAXIA
    APRONED
    APSIDAL
    APTERIA
    APYRASE
    AQUAVIT
    ARABIC
    ARAKS
    ARANEID
    ARBORES
    ARBUTES
    ARCADIA
    ARCHAEA
    ARCHERS
    ARCHILS
    ARCHON
    ARCKING
    ARCUS
    ARDENT
    ARDUOUS
    AREAWAY
    ARENAS
    ARENOUS
    AREOLE
    ARETES
    ARGALIS
    ARGILS
    ARGOL
    ARGOT
    ARGUER
    ARGUS
    ARGYLLS
    ARIDER
    ARIELS
    ARILS
    ARISE
    ARISTAE
    ARKOSES
    ARMBAND
    ARMETS
    ARMIGER
    ARMLET
    ARMOIRE
    ARMORY
    ARMPITS
    ARNATTO
    AROIDS
    AROSE
    AROUSER
    ARPENS
    ARRAIGN
    ARRASES
    ARRAYS
    ARRIBA
    ARRIVED
    ARROW
    ARROYOS
    ARSHIN
    ARSIS
    ARTELS
    ARTIEST
    ARTISTS
    ARUGOLA
    ARVOS
    ASARUMS
    ASCENDS
    ASCETIC
    ASCOTS
    ASEPSES
    ASHCAKE
    ASHES
    ASHLAR
    ASHMAN
    ASHTRAY
    ASKANT
    ASKESIS
    ASKOS
    ASOCIAL
    ASPER
    ASPIC
    ASPIRES
    ASQUINT
    ASSAIL
    ASSAYED
    ASSENTS
    ASSET
    ASSIST
    ASSOIL
    ASSUME
    ASSURED
    ASTASIA
    ASTERS
    ASTIR
    ASTRAY
    ASUNDER
    ASYLUM
    ATAGHAN
    ATARAXY
    ATAXIAS
    ATELIC
    ATHIRST
    ATINGLE
    ATMAN
    ATOMIC
    ATOMIST
    ATONE
    ATONIA
    ATONING
    ATRESIA
    ATRIP
    ATTABOY
    ATTAIN
    ATTEMPT
    ATTESTS
    ATTIRES
    ATTRITE
    ATWAIN
    AUBERGE
    AUCUBAS
    AUDIBLY
    AUDINGS
    AUDITEE
    AUGER
    AUGITES
    AUGURED
    AUKLET
    AUNTIE
    AURAE
    AURATE
    AUREOLE
    AURIS
    AURORAE
    AURUMS
    AUSTRAL
    AUTEUR
    AUTISMS
    AUTOING
    AUTOPEN
    AUXESES
    AUXINS
    AVARICE
    AVELLAN
    AVENS
    AVERRED
    AVERTER
    AVIANS
    AVIATIC
    AVIDLY
    AVISOS
    AVOID
    AVOSETS
    AVOWER
    AVULSED
    AWAITS
    AWAKES
    AWARDER
    AWEIGH
    AWFULLY
    AWLESS
    AWNINGS
    AXELS
    AXIALLY
    AXILLAS
    AXION
    AXITES
    AXMEN
    AXONES
    AYAHS
    AZIDE
    AZINES
    AZOLES
    AZOTED
    AZOTISE
    AZURE
    BAAED
    BAASES
    BABBLE
    BABELS
    BABIER
    BABOO
    BABOOS
    BABYISH
    BACCAE
    BACHED
    BACKED
    BACKING
    BACKSAW
    BACONS
    BADDEST
    BADGED
    BADLAND
    BAFFED
    BAFFLER
    BAGASSE
    BAGGAGE
    BAGGIER
    BAGLIKE
    BAGPIPE
    BAGWIGS
    BAILEE
    BAILEYS
    BAILOR
    BAIRNLY
    BAITH
    BAIZE
    BAKERY
    BAKLAWA
    BALATAS
    BALDER
    BALDLY
    BALEEN
    BALES
    BALKIER
    BALLAD
    BALLER
    BALLING
    BALLOTS
    BALMIER
    BALONEY
    BAMBINI
    BAMMING
    BANCO
    BANDANA
    BANDER
    BANDIT
    BANDORA
    BANED
    BANGERS
    BANGS
    BANJAX
    BANKER
    BANKS
    BANNET
    BANQUET
    BANTENG
    BANYAN
    BAOBABS
    BARBAL
    BARBELL
    BARBET
    BARBS
    BARCAS
    BARDIC
    BAREGE
    BAREST
    BARGAIN
    BARGES
    BARILLA
    BARIUM
    BARKERS
    BARLESS
    BARMAID
    BARMS
    BARNIER
    BARONET
    BARONY
    BARRAGE
    BARREN
    BARRIER
    BARROW
    BARWARE
    BARYTA
    BARYTON
    BASCULE
    BASENJI
    BASHAWS
    BASHFUL
    BASIDIA
    BASILS
    BASING
    BASKED
    BASMATI
    BASSETS
    BASSO
    BASTE
    BASTILE
    BATBOYS
    BATEAU
    BATFOWL
    BATHERS
    BATHS
    BATIKS
    BATMEN
    BATTEAU
    BATTERS
    BATTING
    BATTS
    BATWING
    BAUDS
    BAUSOND
    BAWDIER
    BAWDS
    BAWLING
    BAWTY
    BAYED
    BAYOU
    BAZAR
    BAZOOS
    BEACON
    BEADIER
    BEADMAN
    BEAGLES
    BEAKS
    BEAMING
    BEANED
    BEANO
    BEARDED
    BEARING
    BEASTLY
    BEATIFY
    BEAUS
    BEAVER
    BEBOPS
    BECAPS
    BECKET
    BECKS
    BECLOUD
    BECRIME
    BEDAMN
    BEDBUGS
    BEDECK
    BEDELS
    BEDEWED
    BEDIM
    BEDLAMP
    BEDOUIN
    BEDRAPE
    BEDRUG
    BEDSORE
    BEDUMB
    BEEBEE
    BEECHY
    BEEFIER
    BEEHIVE
    BEEPERS
    BEERY
    BEETLES
    BEEZERS
    BEFITS
    BEFLECK
    BEFORE
    BEGALL
    BEGAZED
    BEGGARS
    BEGINS
    BEGLADS
    BEGORRA
    BEGROAN
    BEGUM
    BEHAVED
    BEHELD
    BEHOLD
    BEHOVED
    BEIGES
    BEING
    BEKNOT
    BELATED
    BELAYER
    BELCHES
    BELEAPS
    BELIE
    BELIERS
    BELLBOY
    BELLHOP
    BELLMEN
    BELON
    BELOW
    BELTING
    BELYING
    BEMEANS
    BEMISTS
    BEMOAN
    BEMUSED
    BENCH
    BENDAYS
    BENDERS
    BENDYS
    BENES
    BENNET
    BENNY
    BENTHOS
    BENUMBS
    BENZINS
    BENZOLS
    BEQUEST
    BERATED
    BERETS
    BERIME
    BERLINE
    BERMING
    BERRY
    BERTHAS
    BESCOUR
    BESET
    BESIDE
    BESMILE
    BESNOWS
    BESPAKE
    BESTIAL
    BESTOWS
    BESTUD
    BETAKEN
    BETELS
    BETHORN
    BETIDES
    BETOKEN
    BETRAY
    BETTED
    BETTORS
    BEVELER
    BEVORS
    BEWARES
    BEWIG
    BEWORRY
    BEWRAYS
    BEYOND
    BEZEL
    BEZOAR
    BHAKTI
    BHARAL
    BHOOTS
    BIALY
    BIASSED
    BIBBED
    BIBBS
    BIBLESS
    BICEP
    BICOLOR
    BICRONS
    BIDDERS
    BIDER
    BIDING
    BIENNIA
    BIFFIES
    BIFFY
    BIFOCAL
    BIGEYES
    BIGGETY
    BIGGINS
    BIGHORN
    BIGNESS
    BIGOTRY
    BIJOU
    BIKERS
    BIKING
    BILBO
    BILBY
    BILGES
    BILIOUS
    BILKS
    BILLET
    BILLION
    BILLOWY
    BILTONG
    BIMBOES
    BINAL
    BINDERY
    BINDLES
    BINGE
    BINGING
    BINITS
    BINTS
    BIOGAS
    BIOHERM
    BIONIC
    BIONTS
    BIOPTIC
    BIOTICS
    BIOTRON
    BIPED
    BIPODS
    BIRCHES
    BIRDIE
    BIRDMEN
    BIRIANI
    BIRLED
    BIRLS
    BIRSE
    BIRYANI
    BISHOP
    BISON
    BISTER
    BISTRES
    BITCHED
    BITERS
    BITSIER
    BITTERN
    BITTS
    BIVOUAC
    BIZONAL
    BLABBER
    BLACKEN
    BLADE
    BLADING
    BLAINS
    BLAMES
    BLANDER
    BLANKET
    BLARES
    BLASTED
    BLATANT
    BLATTER
    BLAWS
    BLAZES
    BLEAK
    BLEARED
    BLEATER
    BLEEDER
    BLEEPS
    BLENDE
    BLENNY
    BLESSER
    BLIGHT
    BLIMPS
    BLINDLY
    BLINKED
    BLIPPED
    BLISTER
    BLITZ
    BLOATED
    BLOCK
    BLOCS
    BLOND
    BLOOD
    BLOOIE
    BLOOMY
    BLOSSOM
    BLOTTER
    BLOUSES
    BLOWED
    BLOWIER
    BLOWOUT
    BLOWUPS
    BLUBBER
    BLUDGER
    BLUEGUM
    BLUER
    BLUETS
    BLUFFER
    BLUISH
    BLUNDER
    BLUNT
    BLURB
    BLURS
    BLUSH
    BLYPE
    BOARDS
    BOAST
    BOATEL
    BOATING
    BOBBER
    BOBBING
    BOBBY
    BOBSTAY
    BOCCIA
    BOCHE
    BODEGAS
    BODIED
    BODKIN
    BOFFING
    BOFFS
    BOGBEAN
    BOGGIER
    BOGGLER
    BOGLE
    BOGYISM
    BOHEMIA
    BOILED
    BOILS
    BOINKS
    BOLASES
    BOLERO
    BOLETI
    BOLIVIA
    BOLLOX
    BOLSHIE
    BOLTED
    BOLUS
    BOMBE
    BOMBING
    BONACIS
    BONDED
    BONDMEN
    BONER
    BONEYER
    BONGOES
    BONIEST
    BONITOS
    BONNE
    BONNIER
    BONOBOS
    BONZER
    BOOBING
    BOOBS
    BOODLE
    BOOED
    BOOGIE
    BOOHOOS
    BOOKEND
    BOOKIES
    BOOKMEN
    BOOMED
    BOOMKIN
    BOONS
    BOOSTER
    BOOTERY
    BOOTING
    BOOZED
    BOOZILY
    BOPPED
    BORACIC
    BORANE
    BORATES
    BORDER
    BORED
    BORERS
    BORING
    BORNE
    BORONS
    BORSCHT
    BORTY
    BOSCAGE
    BOSKET
    BOSOM
    BOSONIC
    BOSSDOM
    BOSSILY
    BOSTONS
    BOTAS
    BOTCHY
    BOTHERS
    BOTTLE
    BOTTOMS
    BOUCHEE
    BOUDOIR
    BOUGHS
    BOULE
    BOUNCED
    BOUNDED
    BOUQUET
    BOURN
    BOURSE
    BOUSES
    BOUTS
    BOVINES
    BOWER
    BOWFINS
    BOWLDER
    BOWLERS
    BOWLING
    BOWPOTS
    BOWSING
    BOXBALL
    BOXERS
    BOXHAUL
    BOXINGS
    BOYARDS
    BOYISH
    BRABBLE
    BRACERS
    BRACHIA
    BRACT
    BRADOON
    BRAGGY
    BRAIDED
    BRAILLE
    BRAINY
    BRAIZES
    BRAKING
    BRANCH
    BRANDS
    BRANNER
    BRASH
    BRASIER
    BRASSES
    BRATTY
    BRAVED
    BRAVES
    BRAVOED
    BRAWER
    BRAWLIE
    BRAWNY
    BRAYER
    BRAZAS
    BRAZER
    BRAZILS
    BREADS
    BREAKS
    BREAST
    BREATHY
    BREDES
    BREEKS
    BREEZY
    BREVE
    BREVITY
    BREWERY
    BREWSKI
    BRIARY
    BRIBER
    BRICK
    BRICOLE
    BRIDGE
    BRIDLER
    BRIEFER
    BRIERY
    BRIGHTS
    BRILLS
    BRINDED
    BRINERS
    BRINIER
    BRINKS
    BRIOS
    BRISKED
    BRISS
    BRITH
    BRITTLE
    BROAD
    BROADS
    BROCKS
    BROGUES
    BROILS
    BROKERS
    BROMATE
    BROMIDE
    BROMISM
    BRONCHI
    BRONZE
    BROOCH
    BROODY
    BROOM
    BROSE
    BROTHER
    BROWN
    BROWNY
    BROWSES
    BRUGHS
    BRUISER
    BRUITS
    BRUMAL
    BRUNCH
    BRUNTS
    BRUSHUP
    BRUTAL
    BRUTIFY
    BRUXED
    BUBAL
    BUBBA
    BUBBLER
    BUBKES
    BUCCAL
    BUCKET
    BUCKLE
    BUCKOES
    BUCKS
    BUDDERS
    BUDDING
    BUDGED
    BUDGETS
    BUDLIKE
    BUFFERS
    BUFFIER
    BUFFS
    BUGEYE
    BUGGERY
    BUGLE
    BUGLING
    BUGSHA
    BUILDED
    BUIRDLY
    BULBIL
    BULBUL
    BULGERS
    BULGUR
    BULKAGE
    BULKS
    BULLATE
    BULLETS
    BULLION
    BULLS
    BUMBLED
    BUMFS
    BUMMER
    BUMPER
    BUMPILY
    BUNAS
    BUNCO
    BUNDLED
    BUNDTS
    BUNGLE
    BUNION
    BUNKING
    BUNKUM
    BUNRAKU
    BUNTS
    BUOYED
    BUPPIE
    BURAN
    BURBLER
    BURBS
    BURDOCK
    BURET
    BURGEES
    BURGH
    BURGLE
    BURGOUT
    BURIER
    BURKA
    BURKERS
    BURLAPS
    BURLEY
    BURLS
    BURNET
    BURNISH
    BURPED
    BURRED
    BURRITO
    BURRS
    BURSAR
    BURSE
    BURSTED
    BURTONS
    BUSBIES
    BUSES
    BUSHER
    BUSHILY
    BUSHTIT
    BUSIED
    BUSING
    BUSKIN
    BUSMAN
    BUSTARD
    BUSTICS
    BUSTLER
    BUTANE
    BUTCHES
    BUTES
    BUTLERY
    BUTTED
    BUTTIES
    BUTTONY
    BUTYL
    BUTYRYL
    BUYBACK
    BUYOFFS
    BUZUKIS
    BUZZERS
    BWANAS
    BYGONES
    BYLINER
    BYPAST
    BYRES
    BYRNIES
    BYSSUS
    BYWAYS
    BYZANT
    CABALS
    CABBAGY
    CABBING
    CABILDO
    CABLE
    CABLET
    CABOB
    CACAOS
    CACHET
    CACHOUS
    CACKLES
    CACTUS
    CADDIES
    CADENCE
    CADET
    CADGERS
    CADMIC
    CAECA
    CAESAR
    CAFES
    CAGED
    CAGEY
    CAHIER
    CAHOWS
    CAIQUE
    CAIRNED
    CAJAPUT
    CAJOLES
    CAKES
    CALAMAR
    CALATHI
    CALCIFY
    CALDERA
    CALESAS
    CALICHE
    CALIFS
    CALIX
    CALKING
    CALLANS
    CALLEE
    CALLETS
    CALLS
    CALMING
    CALORIE
    CALPAC
    CALQUED
    CALUMNY
    CALVING
    CALYX
    CAMAS
    CAMBIA
    CAMBRIC
    CAMEO
    CAMERAL
    CAMISA
    CAMLET
    CAMOS
    CAMPHOR
    CAMPION
    CAMPS
    CANALED
    CANARDS
    CANCEL
    CANCHAS
    CANDIDS
    CANDLER
    CANDY
    CANES
    CANID
    CANING
    CANNED
    CANNERY
    CANNOLI
    CANNY
    CANOES
    CANONRY
    CANSO
    CANTALS
    CANTER
    CANTIC
    CANTO
    CANTOS
    CANTY
    CANVAS
    CANZONE
    CAPELAN
    CAPERER
    CAPHS
    CAPIZ
    CAPLIN
    CAPOS
    CAPPER
    CAPRINE
    CAPSIZE
    CAPTANS
    CAPTURE
    CARABIN
    CARACUL
    CARAPAX
    CARAVAN
    CARBINE
    CARBOS
    CARCASS
    CARDERS
    CARDING
    CARDS
    CAREERS
    CARESS
    CARFUL
    CARHOP
    CARICES
    CARINAL
    CARIOUS
    CARKS
    CARLINE
    CARLS
    CARNAL
    CARNIE
    CAROACH
    CAROL
    CAROLUS
    CAROTIN
    CARPED
    CARPET
    CARPORT
    CARRELL
    CARRION
    CARROTS
    CARSE
    CARTED
    CARTES
    CARTOP
    CARVELS
    CARVING
    CASAVA
    CASCARA
    CASEIC
    CASERN
    CASHAW
    CASHEW
    CASHOOS
    CASINOS
    CASKETS
    CASQUED
    CASSENA
    CASSINE
    CASTER
    CASTLED
    CASTS
    CATALO
    CATAWBA
    CATCHER
    CATECHU
    CATERAN
    CATFACE
    CATHEAD
    CATJANG
    CATLING
    CATNIP
    CATSUPS
    CATTIE
    CATTISH
    CAUDAD
    CAUDLES
    CAULINE
    CAULKS
    CAUSED
    CAUSEYS
    CAVALLA
    CAVED
    CAVERNS
    CAVIAR
    CAVIL
    CAVINGS
    CAWING
    CAYUSES
    CEASING
    CECAL
    CEDARN
    CEDERS
    CEDULA
    CEILER
    CEILIS
    CELERY
    CELLA
    CELLI
    CELLS
    CELOTEX
    CEMENTA
    CENSE
    CENSING
    CENSUS
    CENTAS
    CENTILE
    CENTOS
    CENTRES
    CENTUM
    CEPES
    CERATED
    CERCIS
    CERED
    CERIC
    CERISES
    CERMET
    CERTAIN
    CERUSES
    CESIUM
    CESSION
    CESTODE
    CESURA
    CETES
    CHABUKS
    CHADARS
    CHAEBOL
    CHAFED
    CHAFFED
    CHAGRIN
    CHAINS
    CHAISE
    CHALAHS
    CHALET
    CHALKS
    CHALLIE
    CHALOT
    CHAMBER
    CHAMMY
    CHAMPAK
    CHAMS
    CHANCES
    CHANGED
    CHANOYU
    CHANTEY
    CHAOS
    CHAPEAU
    CHAPMAN
    CHAPT
    CHARDS
    CHARGED
    CHARING
    CHARKA
    CHARLEY
    CHARMS
    CHARR
    CHARRY
    CHARTS
    CHASERS
    CHASMED
    CHASSED
    CHASTER
    CHATTER
    CHAWED
    CHAYOTE
    CHAZZEN
    CHEAPLY
    CHEATED
    CHECK
    CHEDDAR
    CHEEKED
    CHEEPER
    CHEERIO
    CHEERY
    CHEETAH
    CHEFS
    CHELAS
    CHEMISE
    CHEQUE
    CHERRY
    CHERUBS
    CHESTED
    CHETH
    CHEVIOT
    CHEVY
    CHEWING
    CHIAO
    CHIASMS
    CHICANO
    CHICHIS
    CHICLE
    CHICOS
    CHIDER
    CHIEFER
    CHIELDS
    CHIGOE
    CHILDLY
    CHILIES
    CHILLI
    CHIMAR
    CHIME
    CHIMERS
    CHIMLEY
    CHINAS
    CHINES
    CHINKY
    CHINOS
    CHINWAG
    CHIPS
    CHIRKS
    CHIROS
    CHIRPY
    CHIRRES
    CHISEL
    CHITLIN
    CHITTY
    CHIVIES
    CHLORIC
    CHOCK
    CHOICES
    CHOKED
    CHOKIER
    CHOLATE
    CHOLINE
    CHOMP
    CHOOKS
    CHOOSY
    CHOPPER
    CHORALE
    CHORDS
    CHORED
    CHORIC
    CHOROID
    CHOSEN
    CHOUGHS
    CHOUSH
    CHOWSE
    CHRISMS
    CHROME
    CHROMOS
    CHUBBY
    CHUCKS
    CHUFA
    CHUFFS
    CHUKAR
    CHUKKER
    CHUMPS
    CHUNKY
    CHUPPAS
    CHURN
    CHURRED
    CHUTED
    CHUTNEY
    CHYME
    CHYMOUS
    CIBOULE
    CICALAS
    CICHLID
    CIGARET
    CILICE
    CINCH
    CINDERY
    CINEOLE
    CINQUE
    CIPHONY
    CIRCLER
    CIRCUSY
    CIRRI
    CISCO
    CISSY
    CISTUS
    CITER
    CITHERN
    CITIFY
    CITOLE
    CITRIC
    CITRONS
    CIVET
    CIVIES
    CIVVIES
    CLACHS
    CLADDED
    CLADODE
    CLAIMED
    CLAMMED
    CLAMOUR
    CLAMS
    CLANGS
    CLANS
    CLAQUE
    CLARIES
    CLARO
    CLASHED
    CLASPER
    CLASSER
    CLASSY
    CLAUCHT
    CLAVATE
    CLAVI
    CLAWERS
    CLAYED
    CLAYPAN
    CLEANLY
    CLEARED
    CLEATED
    CLEAVES
    CLEFT
    CLEOME
    CLEPING
    CLERID
    CLERKLY
    CLEWING
    CLICK
    CLIENTS
    CLIFTS
    CLIMBER
    CLINCH
    CLINGER
    CLINK
    CLIPPER
    CLIQUES
    CLIVERS
    CLOACAL
    CLOBBER
    CLOCKER
    CLOGGER
    CLOMPED
    CLONER
    CLONISM
    CLONUS
    CLOQUE
    CLOSER
    CLOSETS
    CLOTHE
    CLOTTED
    CLOUDS
    CLOURED
    CLOUTS
    CLOVERY
    CLOWNS
    CLOZES
    CLUBMEN
    CLUED
    CLUMP
    CLUNG
    CLUNKY
    CLUTTER
    CNIDA
    COACHES
    COADMIT
    COALAS
    COALERS
    COALS
    COAPTED
    COAST
    COATED
    COATI
    COAXED
    COAXING
    COBBIER
    COBBS
    COBLES
    COBWEB
    COCAS
    COCCIDS
    COCHAIR
    COCKED
    COCKILY
    COCKLES
    COCKUP
    COCOMAT
    COCOTTE
    CODDER
    CODDLER
    CODEIA
    CODEINS
    CODES
    CODICES
    CODLING
    CODROVE
    COELOM
    COENACT
    COERCED
    COEVAL
    COFFEES
    COFFINS
    COFFS
    COGGING
    COGNATE
    COGWAY
    COHEIR
    COHERES
    COHOS
    COHUNES
    COIFING
    COIGNES
    COILING
    COINERS
    COIRS
    COJOINS
    COLAS
    COLDISH
    COLED
    COLICKY
    COLITIC
    COLLARS
    COLLET
    COLLIER
    COLLOPS
    COLOG
    COLONEL
    COLONUS
    COLORS
    COLTERS
    COLUMEL
    COLZA
    COMAKER
    COMATES
    COMBE
    COMBINE
    COMBUST
    COMELY
    COMETH
    COMFITS
    COMICAL
    COMITY
    COMMATA
    COMMIT
    COMMON
    COMMY
    COMPARE
    COMPEER
    COMPETE
    COMPLOT
    COMPORT
    COMPS
    COMRADE
    CONCAVE
    CONCEPT
    CONCHAE
    CONCHO
    CONCOCT
    CONDEMN
    CONDOM
    CONDOS
    CONED
    CONFABS
    CONFIDE
    CONFLUX
    CONGAED
    CONGEED
    CONGEST
    CONGOS
    CONICS
    CONIN
    CONIUM
    CONKER
    CONNATE
    CONNING
    CONOIDS
    CONSOL
    CONSULS
    CONTE
    CONTEST
    CONTOUR
    CONUS
    CONVEX
    CONVOY
    COOED
    COOERS
    COOING
    COOKEY
    COOKOFF
    COOLANT
    COOLIE
    COOLS
    COOMBE
    COONTIE
    COOPING
    COOTER
    COPAIBA
    COPAY
    COPEN
    COPES
    COPIHUE
    COPLOT
    COPPER
    COPPRA
    COPRAS
    COPULA
    COPYCAT
    COQUINA
    CORANTO
    CORBELS
    CORDAGE
    CORDIAL
    CORDONS
    CORER
    CORIA
    CORKER
    CORKY
    CORMS
    CORNED
    CORNET
    CORNIFY
    CORNU
    CORNUTO
    CORONAE
    CORONET
    CORPUS
    CORRIDA
    CORRUPT
    CORSE
    CORTEGE
    CORULER
    CORVETS
    CORYMB
    COSEC
    COSEY
    COSHES
    COSIES
    COSINE
    COSMISM
    COSSETS
    COSTARD
    COSTERS
    COSTS
    COTEAU
    COTHURN
    COTTAE
    COTTER
    COTTONY
    COUCHER
    COUGH
    COULDST
    COULOMB
    COUNTED
    COUPE
    COUPLED
    COUPONS
    COURLAN
    COURT
    COUSIN
    COUTH
    COUVADE
    COVER
    COVERTS
    COVETER
    COVING
    COWARD
    COWBIRD
    COWER
    COWFLOP
    COWHERD
    COWLED
    COWMEN
    COWPIE
    COWRIE
    COWSHED
    COXALGY
    COXITIS
    COYER
    COYNESS
    COYPU
    COZENS
    COZIED
    COZYING
    CRABBED
    CRACKED
    CRACKUP
    CRADLES
    CRAFTY
    CRAKES
    CRAMMED
    CRAMPON
    CRANE
    CRANING
    CRANKLE
    CRANNY
    CRAPOLA
    CRAPS
    CRASHES
    CRATCH
    CRATES
    CRAVAT
    CRAVENS
    CRAWDAD
    CRAWLY
    CRAZED
    CRAZING
    CREAKY
    CREAMY
    CREASY
    CREATOR
    CREDIT
    CREED
    CREEL
    CREEPER
    CREESES
    CREMINI
    CREOLES
    CREPEY
    CREPT
    CRESSES
    CRESTED
    CRETICS
    CREWED
    CREWMEN
    CRICK
    CRICOID
    CRIKEY
    CRIMINY
    CRIMPLE
    CRINGED
    CRINKLE
    CRIOLLO
    CRISIC
    CRISPER
    CRISSAL
    CRITICS
    CROAKED
    CROCHET
    CROCKET
    CROFTER
    CRONES
    CROOKED
    CROONER
    CROPS
    CROSIER
    CROSSES
    CROUCH
    CROUPY
    CROWBAR
    CROWDS
    CROWING
    CROWNS
    CROZES
    CRUCIFY
    CRUDE
    CRUDITY
    CRUELTY
    CRUISER
    CRUMBER
    CRUMBY
    CRUMPET
    CRUNCHY
    CRURA
    CRUSES
    CRUSHER
    CRUSTED
    CRUZADO
    CRYOGEN
    CRYPTO
    CUATRO
    CUBBISH
    CUBER
    CUBICLE
    CUBISMS
    CUBITI
    CUCKOLD
    CUDDIES
    CUDDLY
    CUEING
    CUFFS
    CUISHES
    CUKES
    CULEX
    CULLAYS
    CULLETS
    CULLIS
    CULMS
    CULTCH
    CULTIST
    CULVERS
    CUMBIA
    CUMMERS
    CUMULI
    CUNEATE
    CUPCAKE
    CUPFUL
    CUPOLA
    CUPPER
    CUPRIC
    CUPSFUL
    CUPULES
    CURACY
    CURARE
    CURATED
    CURBERS
    CURCUMA
    CURDLED
    CURED
    CURETS
    CURIA
    CURING
    CURITE
    CURLER
    CURLILY
    CURRACH
    CURRED
    CURRIES
    CURSE
    CURSING
    CURST
    CURTATE
    CURTSEY
    CURVES
    CURVING
    CUSHAT
    CUSHILY
    CUSPATE
    CUSPS
    CUSSING
    CUSTOM
    CUTBANK
    CUTER
    CUTEY
    CUTIN
    CUTLASS
    CUTLETS
    CUTOUTS
    CUTTIES
    CUTTY
    CUVEE
    CYANID
    CYANINS
    CYBORG
    CYCASES
    CYCLER
    CYCLIN
    CYCLO
    CYDER
    CYGNETS
    CYMARS
    CYMENE
    CYMLINS
    CYMOUS
    CYPHERS
    CYPSELA
    CYSTS
    CZARDOM
    DABBED
    DABBLED
    DACHA
    DACKERS
    DACRONS
    DADAIST
    DADDLES
    DADOING
    DAFFED
    DAFFY
    DAGGAS
    DAGGLES
    DAGOS
    DAHOON
    DAIKONS
    DAIMIOS
    DAINTY
    DAISIES
    DALAPON
    DALES
    DALLIER
    DAMAGE
    DAMANS
    DAMES
    DAMMER
    DAMNER
    DAMOSEL
    DAMPER
    DAMPLY
    DAMSONS
    DANCERS
    DANDIER
    DANDLED
    DANGER
    DANGLER
    DANIOS
    DANSEUR
    DAPPER
    DAPSONE
    DARED
    DARESAY
    DARIOLE
    DARKEST
    DARKING
    DARKLY
    DARNEL
    DARNS
    DARTING
    DASHED
    DASHI
    DASHPOT
    DASYURE
    DATED
    DATING
    DATTO
    DATURAS
    DAUBERS
    DAUBRY
    DAUNTED
    DAUTIE
    DAVENED
    DAWDLE
    DAWEN
    DAWNS
    DAWTS
    DAYFLY
    DAYMARE
    DAYSTAR
    DAZES
    DAZZLES
    DEADER
    DEADMEN
    DEAFER
    DEAIRED
    DEALING
    DEANING
    DEARIES
    DEARY
    DEATH
    DEAVED
    DEBAGS
    DEBASE
    DEBATED
    DEBEAKS
    DEBONE
    DEBRIDE
    DEBTS
    DEBUT
    DECADAL
    DECAGON
    DECAMPS
    DECANTS
    DECAYED
    DECEITS
    DECERNS
    DECIDER
    DECIMAL
    DECKERS
    DECLAIM
    DECLINE
    DECODER
    DECORUM
    DECOYS
    DECRIAL
    DECRY
    DECURY
    DEDUCES
    DEEDING
    DEEMED
    DEEPER
    DEERS
    DEFACED
    DEFAMER
    DEFATS
    DEFECTS
    DEFER
    DEFICIT
    DEFILE
    DEFINED
    DEFLEA
    DEFOCUS
    DEFORMS
    DEFRAYS
    DEFTLY
    DEFUNDS
    DEFUZE
    DEGAME
    DEGASES
    DEGRADE
    DEGUMS
    DEHORNS
    DEICER
    DEICTIC
    DEIFORM
    DEILS
    DEISTS
    DEJECTA
    DEKEING
    DELAINE
    DELAY
    DELEADS
    DELETE
    DELFTS
    DELIMED
    DELISH
    DELLS
    DELTAIC
    DELUDE
    DELUGED
    DELVER
    DEMAND
    DEMASTS
    DEMERGE
    DEMIC
    DEMISED
    DEMOBS
    DEMON
    DEMOTE
    DEMUR
    DENARI
    DENES
    DENIED
    DENIMED
    DENOTE
    DENSER
    DENTALS
    DENTIN
    DENTOID
    DENUDER
    DEODARA
    DEPAINT
    DEPERM
    DEPLETE
    DEPONE
    DEPOSAL
    DEPOSIT
    DEPRIVE
    DEPUTED
    DERAILS
    DERATES
    DERBY
    DERIVE
    DERMAL
    DERMS
    DERRY
    DESANDS
    DESERT
    DESEXES
    DESIRER
    DESKMEN
    DESMID
    DESOXY
    DESPOND
    DESTINE
    DETAIL
    DETECTS
    DETERGE
    DETICKS
    DETOXED
    DEUCE
    DEVALUE
    DEVELED
    DEVIANT
    DEVILED
    DEVISE
    DEVISOR
    DEVOLVE
    DEVOTEE
    DEWAN
    DEWAX
    DEWED
    DEWING
    DEWOOLS
    DEXIES
    DEXTRO
    DHARMA
    DHOBI
    DHOORA
    DHOTI
    DHURNAS
    DIABOLO
    DIAGRAM
    DIALING
    DIALOG
    DIAMIDE
    DIAPER
    DIARCHY
    DIASTER
    DIAZINE
    DIBBED
    DIBBLED
    DICAMBA
    DICERS
    DICING
    DICKEY
    DICKING
    DICOTS
    DICTION
    DIDACT
    DIDDLES
    DIDOES
    DIEING
    DIESEL
    DIETARY
    DIETING
    DIFFUSE
    DIGGED
    DIGHTED
    DIGLOT
    DIGRAPH
    DIKER
    DIKTAT
    DILATES
    DILDOS
    DILLY
    DILUTES
    DIMERS
    DIMMED
    DIMNESS
    DIMPLED
    DINAR
    DINED
    DINERS
    DINGED
    DINGEYS
    DINGING
    DINGS
    DINKED
    DINKING
    DINKY
    DINOS
    DIOBOLS
    DIOLS
    DIOXAN
    DIOXIDS
    DIPLOE
    DIPLONT
    DIPODY
    DIPPER
    DIPSAS
    DIPTYCA
    DIRAMS
    DIREFUL
    DIRGES
    DIRKS
    DIRNDLS
    DIRTILY
    DISARMS
    DISBUD
    DISCED
    DISCO
    DISCS
    DISEUR
    DISHELM
    DISHPAN
    DISKED
    DISMAL
    DISME
    DISOWN
    DISPEND
    DISRATE
    DISSEAT
    DISSES
    DISTANT
    DISTILL
    DISUSE
    DITCH
    DITHER
    DITSY
    DITTOS
    DIURNAL
    DIVAS
    DIVERSE
    DIVESTS
    DIVINE
    DIVISOR
    DIVULSE
    DIWANS
    DIZENS
    DIZZY
    DJINNS
    DOATING
    DOBBIN
    DOBLA
    DOBRAS
    DOCENT
    DOCKED
    DOCKING
    DODDERS
    DODGEMS
    DODGIER
    DODOS
    DOFFED
    DOGBANE
    DOGEARS
    DOGFACE
    DOGGERY
    DOGGISH
    DOGIE
    DOGMA
    DOGSLED
    DOILIES
    DOITS
    DOLEFUL
    DOLLED
    DOLLOP
    DOLMAN
    DOLOR
    DOLTISH
    DOMAL
    DOMICIL
    DOMINO
    DONATES
    DONGAS
    DONJON
    DONNAS
    DONNERD
    DONORS
    DONZEL
    DOODADS
    DOODLES
    DOOLEE
    DOOMED
    DOOMS
    DOORS
    DOOZERS
    DOPANTS
    DOPES
    DOPING
    DORBUGS
    DORKY
    DORMIE
    DORNECK
    DORPS
    DORSALS
    DORSUM
    DOSER
    DOSSALS
    DOSSERS
    DOSSING
    DOTARDS
    DOTIER
    DOTTELS
    DOTTING
    DOUBLE
    DOUBLY
    DOUCE
    DOUCHES
    DOUGHY
    DOUMS
    DOURER
    DOUSED
    DOVECOT
    DOVENS
    DOWDIER
    DOWEL
    DOWERS
    DOWNED
    DOWNS
    DOWSED
    DOXIE
    DOYLEY
    DOZEN
    DOZERS
    DOZING
    DRABLY
    DRACHMS
    DRAFTED
    DRAGEE
    DRAGGY
    DRAGS
    DRAINER
    DRAMADY
    DRANK
    DRAPERY
    DRATS
    DRAWEE
    DRAWL
    DRAWN
    DRAYMAN
    DREADS
    DREAMT
    DRECK
    DREDGER
    DREGGY
    DREIDLS
    DRESSED
    DRIBBED
    DRIED
    DRIEST
    DRIFTY
    DRILY
    DRIPPER
    DRIVEL
    DRIVES
    DROGUES
    DROLL
    DROMON
    DRONER
    DRONING
    DROOLY
    DROPLET
    DROPSY
    DROSS
    DROUKED
    DROVE
    DROVING
    DROWNER
    DROWSY
    DRUDGED
    DRUGGIE
    DRUIDS
    DRUMMER
    DRUNKS
    DRYABLE
    DRYER
    DRYLAND
    DRYWALL
    DUALITY
    DUBBER
    DUBIETY
    DUCAT
    DUCHY
    DUCKIER
    DUCKY
    DUCTS
    DUDEEN
    DUDISH
    DUELIST
    DUELLOS
    DUENNA
    DUETTED
    DUFFLE
    DUGONG
    DUIKERS
    DUKING
    DULIAS
    DULLING
    DULSE
    DUMBEST
    DUMBS
    DUMMIED
    DUMPERS
    DUMPS
    DUNCES
    DUNGED
    DUNGY
    DUNKER
    DUNLINS
    DUNNEST
    DUNTS
    DUOMO
    DUPED
    DUPING
    DURABLE
    DURAS
    DURESS
    DURIONS
    DUROC
    DURRIE
    DURUMS
    DUSKISH
    DUSTER
    DUSTMAN
    DUSTS
    DUTEOUS
    DUVETS
    DWARFS
    DWELL
    DWINDLE
    DYABLE
    DYBBUK
    DYERS
    DYKED
    DYNAMO
    DYNEIN
    DYNODE
    DYVOUR
    EAGERS
    EAGLETS
    EARACHE
    EARED
    EARINGS
    EARLIER
    EARMARK
    EARNEST
    EARSHOT
    EARTHS
    EARWORM
    EASELS
    EASILY
    EASTING
    EATERS
    EAVES
    EBONICS
    EBONS
    ECARTES
    ECDYSON
    ECHED
    ECHING
    ECHOERS
    ECHOISM
    ECLATS
    ECONOMY
    ECRUS
    ECTHYMA
    ECTYPE
    EDAPHIC
    EDEMA
    EDGER
    EDGILY
    EDICT
    EDIFIER
    EDITED
    EDITRIX
    EDUCES
    EELIER
    EERIE
    EFFACE
    EFFECTS
    EFFORT
    EFFUSES
    EGEST
    EGGARS
    EGGERS
    EGGNOGS
    EGOISTS
    EGRET
    EIDOLA
    EIGHTH
    EIKON
    EISWEIN
    EJECTOR
    EKUELE
    ELANS
    ELAPSED
    ELATED
    ELATION
    ELDER
    ELDRICH
    ELECTRO
    ELEGISE
    ELEGY
    ELEVATE
    ELFIN
    ELICIT
    ELIDING
    ELITES
    ELLIPSE
    ELOIGN
    ELOINS
    ELOPES
    ELUATES
    ELUDES
    ELUSIVE
    ELUTING
    ELVER
    ELYTRA
    EMAILS
    EMBANK
    EMBARKS
    EMBAYS
    EMBLAZE
    EMBOLIC
    EMBOSOM
    EMBOWER
    EMBRUE
    EMBRYON
    EMDASH
    EMENDER
    EMERGES
    EMERODS
    EMESIS
    EMETINS
    EMIGRES
    EMITTED
    EMMETS
    EMOTED
    EMOTION
    EMPALES
    EMPIRE
    EMPLOY
    EMPRESS
    EMPTIES
    EMULATE
    ENABLE
    ENACTED
    ENAMINE
    ENATES
    ENCAGES
    ENCASES
    ENCINA
    ENCLOSE
    ENCOMIA
    ENCRYPT
    ENDEAR
    ENDERS
    ENDITED
    ENDLESS
    ENDOPOD
    ENDOWS
    ENDUED
    ENDURER
    ENDWISE
    ENEMY
    ENFACES
    ENFOLDS
    ENGAGER
    ENGINED
    ENGLISH
    ENGRAIL
    ENGROSS
    ENHANCE
    ENISLES
    ENJOYER
    ENLARGE
    ENMITY
    ENNUIS
    ENOLASE
    ENOSIS
    ENPLANE
    ENRAGES
    ENROBER
    ENROLS
    ENSIGN
    ENSKIED
    ENSNARE
    ENSUED
    ENSURER
    ENTASIA
    ENTERAL
    ENTERS
    ENTICED
    ENTITLE
    ENTOMBS
    ENTRAP
    ENTRIES
    ENTWIST
    ENVELOP
    ENVIES
    ENVOI
    ENWHEEL
    ENWOUND
    ENZYMES
    EOLIAN
    EONISMS
    EOSINS
    EPARCHY
    EPEIRIC
    EPHEBE
    EPHEBOS
    EPHOR
    EPICAL
    EPIDERM
    EPIGENE
    EPIGRAM
    EPIMER
    EPISCIA
    EPITAXY
    EPIZOIC
    EPODE
    EPOPEE
    EPOXIES
    EQUABLY
    EQUATE
    EQUID
    EQUIP
    ERASED
    ERASION
    ERECTED
    ERELONG
    ERETHIC
    ERGOTIC
    ERINGO
    ERMINED
    ERODENT
    EROSES
    EROTICS
    ERRAND
    ERRATAS
    ERRING
    ERUCT
    ERUGOS
    ERVILS
    ESCAPED
    ESCARP
    ESCHEAT
    ESCORTS
    ESCROWS
    ESKAR
    ESPANOL
    ESPIES
    ESQUIRE
    ESSENCE
    ESTATED
    ESTERS
    ESTRAL
    ESTRINS
    ESTRUM
    ETALON
    ETAPE
    ETCHED
    ETERNAL
    ETHANOL
    ETHERS
    ETHION
    ETHNOS
    ETHYL
    ETHYNYL
    ETUDES
    ETYMON
    EUCHRES
    EUGENIC
    EUNUCH
    EUPLOID
    EUREKA
    EURYOKY
    EVACUEE
    EVADES
    EVASIVE
    EVENING
    EVERT
    EVICT
    EVIDENT
    EVILS
    EVITED
    EVOKER
    EVOLVE
    EVULSED
    EXABYTE
    EXACTER
    EXALTED
    EXAMINE
    EXARCHS
    EXCELS
    EXCIDE
    EXCISE
    EXCITER
    EXCLAVE
    EXCUSED
    EXEDRA
    EXEMPTS
    EXERTS
    EXHAUST
    EXHUME
    EXILE
    EXILIAN
    EXING
    EXITING
    EXODOS
    EXONIC
    EXOSMIC
    EXPAND
    EXPECT
    EXPENDS
    EXPIRE
    EXPLAIN
    EXPORT
    EXPOSED
    EXPRESS
    EXSECTS
    EXTENDS
    EXTERNS
    EXTOLS
    EXTRAS
    EXUDE
    EXULTED
    EXURBS
    EYASES
    EYEBAR
    EYECUP
    EYEHOLE
    EYELET
    EYELIKE
    EYESPOT
    EYRAS
    FABBER
    FABLERS
    FABRICS
    FACER
    FACETED
    FACIAL
    FACILE
    FACTOID
    FACTUAL
    FACULTY
    FADDIST
    FADEINS
    FADGE
    FADINGS
    FAENA
    FAGGED
    FAGGOTY
    FAGOTED
    FAILING
    FAINER
    FAINTLY
    FAIRIES
    FAIRWAY
    FAITOUR
    FAKEERS
    FAKEY
    FALBALA
    FALLACY
    FALLERS
    FALLOWS
    FALSEST
    FALTER
    FAMINE
    FAMULI
    FANCIES
    FANDOMS
    FANFIC
    FANGED
    FANJETS
    FANNIES
    FANOS
    FANTOD
    FANUMS
    FAQIRS
    FARADIC
    FARCER
    FARCIE
    FARDEL
    FARED
    FARFALS
    FARING
    FARMED
    FARNESS
    FARROWS
    FARTLEK
    FASCIAL
    FASHED
    FASTEN
    FASTS
    FATED
    FATHERS
    FATING
    FATNESS
    FATTEN
    FATTIES
    FATUITY
    FAUCAL
    FAUCIAL
    FAULTED
    FAUNAL
    FAUVISM
    FAVELLA
    FAVORED
    FAVUS
    FAWNIER
    FAXES
    FAZENDA
    FEARER
    FEASE
    FEASTED
    FEATHER
    FEAZED
    FECES
    FECULA
    FEDEX
    FEEBLE
    FEEDBOX
    FEEDS
    FEELING
    FEEZING
    FEIJOA
    FEIRIE
    FELID
    FELLAH
    FELLER
    FELLOE
    FELLY
    FELSIC
    FELTS
    FEMES
    FEMORAL
    FENCED
    FENDED
    FENLAND
    FENNIER
    FEOFF
    FEOFFS
    FERES
    FERINE
    FERMATA
    FERMIS
    FERNY
    FERRETS
    FERRITE
    FERRY
    FERULE
    FERVOR
    FESSE
    FESTER
    FETAL
    FETCHES
    FETICH
    FETLOCK
    FETTERS
    FETUS
    FEUDARY
    FEUED
    FEWER
    FEYLY
    FEZZY
    FIANCES
    FIATS
    FIBER
    FIBRIL
    FIBROIN
    FIBULAE
    FICHES
    FICKLE
    FICTION
    FIDDLED
    FIDEIST
    FIDGETS
    FIEFS
    FIEND
    FIERILY
    FIFER
    FIFTH
    FIGGED
    FIGMENT
    FIGURES
    FILBERT
    FILED
    FILET
    FILIBEG
    FILLER
    FILLIES
    FILLOS
    FILMER
    FILMILY
    FILMY
    FILTH
    FIMBLES
    FINALE
    FINANCE
    FINCHES
    FINED
    FINESSE
    FINGERS
    FINIKIN
    FINISH
    FINKING
    FINNED
    FIORD
    FIQUES
    FIREDOG
    FIREPAN
    FIRING
    FIRMANS
    FIRMING
    FIRRY
    FIRTHS
    FISHER
    FISHGIG
    FISHWAY
    FISSURE
    FISTS
    FITCHET
    FITMENT
    FITTEST
    FIXABLE
    FIXED
    FIXING
    FIXURE
    FIZZER
    FIZZLE
    FJELDS
    FLABS
    FLACON
    FLAGMAN
    FLAIL
    FLAKE
    FLAKEY
    FLAMBE
    FLAMEN
    FLAMIER
    FLANES
    FLANGES
    FLANKS
    FLAPPY
    FLAREUP
    FLASHES
    FLATBED
    FLATS
    FLATUS
    FLAUTAS
    FLAVOR
    FLAWIER
    FLAXES
    FLAYERS
    FLEAMS
    FLECK
    FLEDGED
    FLEECER
    FLEER
    FLEETED
    FLEMISH
    FLENSES
    FLESHLY
    FLEWS
    FLEXION
    FLEYING
    FLICKS
    FLIES
    FLIMSY
    FLINGS
    FLIPPED
    FLIRT
    FLITCH
    FLITS
    FLOATED
    FLOCCED
    FLOCKS
    FLOGGER
    FLOOD
    FLOOIE
    FLOOSIE
    FLOPPER
    FLORAL
    FLORID
    FLOSS
    FLOSSY
    FLOUNCE
    FLOURY
    FLOWAGE
    FLOWING
    FLUBDUB
    FLUERIC
    FLUFFS
    FLUIDLY
    FLUKES
    FLUKY
    FLUMMOX
    FLUNK
    FLUNKS
    FLUORIN
    FLUSHER
    FLUTER
    FLUTING
    FLUXED
    FLUYTS
    FLYBLOW
    FLYBYS
    FLYLEAF
    FLYOFFS
    FLYTED
    FLYWAY
    FOAMED
    FOAMING
    FOCAL
    FOCUSES
    FOEHNS
    FOETOR
    FOGDOG
    FOGGED
    FOGGING
    FOGLESS
    FOIBLES
    FOINING
    FOISTED
    FOLDED
    FOLDS
    FOLIA
    FOLIO
    FOLIUM
    FOLKISH
    FOLKY
    FOLLOWS
    FOMITES
    FONDING
    FONDLY
    FONDUES
    FOODIE
    FOOLING
    FOOTBOY
    FOOTIER
    FOOTLER
    FOOTS
    FOOZLE
    FOPPERY
    FORAGER
    FORAY
    FORBADE
    FORBODE
    FORCE
    FORCES
    FORDO
    FOREBAY
    FOREGO
    FOREMEN
    FORESAW
    FOREVER
    FORGE
    FORGES
    FORGO
    FORINT
    FORKFUL
    FORLORN
    FORMATE
    FORMER
    FORMICA
    FORMULA
    FORRIT
    FORTH
    FORTUNE
    FORWENT
    FOSSAS
    FOSSIL
    FOUGHT
    FOULING
    FOUNDER
    FOURGON
    FOVEAE
    FOVEOLE
    FOWLPOX
    FOXFISH
    FOXILY
    FOXTAIL
    FOZIEST
    FRACTUR
    FRAGILE
    FRAILS
    FRAME
    FRAMING
    FRANKER
    FRAPPED
    FRATER
    FRAUGHT
    FRAZILS
    FREAKY
    FREED
    FREEMEN
    FREEST
    FREIGHT
    FRENUM
    FRESCO
    FRESHER
    FRETFUL
    FRETTY
    FRIARY
    FRIEND
    FRIEZE
    FRIGHT
    FRIJOLE
    FRILLY
    FRISBEE
    FRISEUR
    FRISKS
    FRITHS
    FRITTS
    FRIZED
    FRIZZ
    FRIZZLY
    FROES
    FROGMAN
    FROMAGE
    FRONT
    FRONTON
    FROSTED
    FROTHER
    FROWARD
    FROWS
    FROWZY
    FRUGS
    FRUITY
    FRUSTUM
    FRYPAN
    FUBSIER
    FUCKER
    FUCKUP
    FUCOSES
    FUDDLE
    FUDGED
    FUELER
    FUELS
    FUGGED
    FUGIO
    FUGLING
    FUGUIST
    FULCRA
    FULGENT
    FULLAMS
    FULLEST
    FULMARS
    FUMARIC
    FUMED
    FUMETS
    FUMULI
    FUNDERS
    FUNDUS
    FUNGAL
    FUNGOES
    FUNKED
    FUNKIER
    FUNNED
    FUNNIER
    FUNPLEX
    FURBISH
    FURIOSO
    FURLESS
    FURMITY
    FURORES
    FURRING
    FURTHER
    FURZY
    FUSED
    FUSES
    FUSILLI
    FUSSED
    FUSSILY
    FUSTIC
    FUSUMA
    FUTILE
    FUTURE
    FUZED
    FUZILS
    FUZZILY
    FYLFOT
    GABBARD
    GABBIER
    GABBLES
    GABFEST
    GABLED
    GADDED
    GADDIS
    GADID
    GADOID
    GAFFE
    GAFFING
    GAGER
    GAGGERS
    GAGING
    GAIETY
    GAINERS
    GAINSAY
    GAITING
    GALAH
    GALAX
    GALEAS
    GALERE
    GALIOT
    GALLED
    GALLETA
    GALLIC
    GALLIOT
    GALLOON
    GALLOWS
    GALOOTS
    GALORES
    GALYACS
    GAMAYS
    GAMBE
    GAMBIR
    GAMBLED
    GAMBOLS
    GAMELY
    GAMETAL
    GAMIC
    GAMINE
    GAMMA
    GAMMIER
    GAMPS
    GANDERS
    GANGED
    GANGLY
    GANGUES
    GANJAS
    GANOID
    GAOLER
    GAPER
    GAPOSIS
    GARAGE
    GARBED
    GARBLES
    GARDA
    GARFISH
    GARGLED
    GARLAND
    GARNERS
    GAROTE
    GARRED
    GARRONS
    GARTHS
    GASCON
    GASHED
    GASIFY
    GASKINS
    GASOHOL
    GASPS
    GASSIER
    GASTER
    GASTRIC
    GATEAUX
    GATERS
    GATING
    GAUCHER
    GAUDIES
    GAUGE
    GAUGING
    GAUMS
    GAURS
    GAUZIER
    GAVEL
    GAVOT
    GAWKERS
    GAWKISH
    GAWPERS
    GAYAL
    GAYEST
    GAZABOS
    GAZEBOS
    GAZES
    GAZUMP
    GEARS
    GECKOS
    GEEKDOM
    GEESE
    GEISHA
    GELANT
    GELATI
    GELCAP
    GELDING
    GELIDLY
    GEMINAL
    GEMMED
    GEMMY
    GEMSBOK
    GENERIC
    GENETIC
    GENIAL
    GENIP
    GENIUS
    GENOME
    GENRES
    GENTES
    GENTLED
    GENTOOS
    GENUS
    GEODIC
    GEOLOGY
    GERBIL
    GERMAN
    GERMIER
    GERUNDS
    GESTAPO
    GESTS
    GETTER
    GEUMS
    GHARIAL
    GHASTLY
    GHAZIES
    GHETTO
    GHOST
    GHOUL
    GIANT
    GIBBED
    GIBBING
    GIBED
    GIBLET
    GIDDIED
    GIDDYAP
    GIFTEES
    GIGATON
    GIGGLER
    GIGLETS
    GIGOT
    GILDED
    GILLED
    GILLIES
    GILTS
    GIMLET
    GIMMES
    GIMPIER
    GINGALL
    GINGERS
    GINGKO
    GINNED
    GINNY
    GIPONS
    GIPSIED
    GIRDED
    GIRDLED
    GIRLIER
    GIRNED
    GIRONS
    GIRTED
    GIRTS
    GITANO
    GITTIN
    GIVERS
    GIZZARD
    GLACIAL
    GLADDER
    GLADS
    GLAIRE
    GLAIVE
    GLAMOUR
    GLANCES
    GLARE
    GLARY
    GLASSY
    GLAZES
    GLEAM
    GLEAN
    GLEBAE
    GLEDS
    GLEEKED
    GLEET
    GLENOID
    GLIADIN
    GLIDE
    GLIDING
    GLIMES
    GLINT
    GLIOMAS
    GLITTER
    GLOAM
    GLOATS
    GLOBED
    GLOBOID
    GLOCHID
    GLOMS
    GLOOMS
    GLORIA
    GLORY
    GLOSSAS
    GLOST
    GLOUT
    GLOVER
    GLOWER
    GLOZE
    GLUCANS
    GLUER
    GLUGS
    GLUME
    GLUMS
    GLUTEAL
    GLUTEUS
    GLYCANS
    GLYCOLS
    GLYPHS
    GNARLY
    GNASH
    GNATS
    GNAWING
    GNOME
    GNOMON
    GOADED
    GOALIES
    GOATEE
    GOBAN
    GOBBET
    GOBBLER
    GOBLETS
    GOBONY
    GODDED
    GODETS
    GODLIKE
    GODOWNS
    GODSONS
    GOFERS
    GOGGLER
    GOGOS
    GOITRE
    GOLDER
    GOLEM
    GOLFING
    GOLOSH
    GOMER
    GOMUTI
    GONADS
    GONERS
    GONIDIA
    GONIFS
    GONOPH
    GOODBY
    GOODISH
    GOODY
    GOOFING
    GOOGOLS
    GOOMBAH
    GOONIER
    GOOPS
    GOOSED
    GOOSY
    GORALS
    GORGE
    GORGET
    GORHEN
    GORILY
    GORMS
    GORSY
    GOSPORT
    GOSSIPY
    GOTHICS
    GOUGE
    GOUGING
    GOURDES
    GOUTS
    GOWANED
    GOWNED
    GOYISH
    GRABBLE
    GRACE
    GRACKLE
    GRADERS
    GRADINS
    GRAFTED
    GRAIL
    GRAINS
    GRAMMA
    GRAMP
    GRAMS
    GRANDAM
    GRANDPA
    GRANITA
    GRANS
    GRANTOR
    GRAPERY
    GRAPHIC
    GRAPPA
    GRASPED
    GRASSES
    GRATERS
    GRATING
    GRAVED
    GRAVER
    GRAVIDA
    GRAVURE
    GRAYING
    GRAYS
    GRAZES
    GREASER
    GREATER
    GREAVES
    GREEDS
    GREENED
    GREENTH
    GREETER
    GREIGES
    GREMMY
    GREYHEN
    GREYS
    GRIDE
    GRIEF
    GRIEVES
    GRIFFON
    GRIFTS
    GRILLE
    GRILSE
    GRIMES
    GRIMMER
    GRINDER
    GRINGOS
    GRIOTS
    GRIPES
    GRIPMEN
    GRIPPLE
    GRISKIN
    GRISTER
    GRITHS
    GRIVET
    GROANED
    GROCER
    GROGGY
    GROINS
    GROOMED
    GROOVER
    GROPER
    GROSSED
    GROSZE
    GROTTY
    GROUP
    GROUSE
    GROUTED
    GROVED
    GROWERS
    GROWLS
    GROWTH
    GRUBBED
    GRUDGED
    GRUELER
    GRUFFER
    GRUGRUS
    GRUMMER
    GRUMPED
    GRUNGER
    GRUNTED
    GRUTCH
    GUACOS
    GUANAY
    GUANO
    GUARD
    GUAVA
    GUDGEON
    GUESSED
    GUESTS
    GUGGLED
    GUIDED
    GUIDON
    GUILDS
    GUILT
    GUINEA
    GUISARD
    GUITAR
    GULCH
    GULFED
    GULLED
    GULLIED
    GULPED
    GULPS
    GUMBOOT
    GUMLINE
    GUMMER
    GUMMOSE
    GUMWEED
    GUNFIRE
    GUNKY
    GUNNED
    GUNNERS
    GUNPLAY
    GUNSHOT
    GURGED
    GURGLES
    GURNEY
    GURSHES
    GUSHES
    GUSSET
    GUSSY
    GUSTO
    GUTLIKE
    GUTTAE
    GUTTERY
    GUTTLER
    GUYLINE
    GUZZLER
    GWINE
    GYNECIA
    GYPPED
    GYPSIES
    GYRAL
    GYRATED
    GYRENES
    GYROS
    GYVED
    HABILE
    HABITS
    HABUS
    HACKED
    HACKIE
    HACKLER
    HACKNEY
    HADDEST
    HADITH
    HADJI
    HAEING
    HAEMOID
    HAFFETS
    HAFNIUM
    HAFTING
    HAGBUT
    HAGGADA
    HAGGISH
    HAGRIDE
    HAIKS
    HAILERS
    HAINTS
    HAIRED
    HAIRY
    HAJJIS
    HAKIMS
    HALAKIC
    HALALS
    HALED
    HALEST
    HALIDES
    HALITES
    HALLEL
    HALLOED
    HALLOT
    HALLUX
    HALOED
    HALOING
    HALTER
    HALUTZ
    HALVE
    HALYARD
    HAMATE
    HAMBURG
    HAMMAL
    HAMMER
    HAMMOCK
    HAMULAR
    HAMZAHS
    HANDAX
    HANDERS
    HANDING
    HANDOFF
    HANDSET
    HANGED
    HANGMEN
    HANGUP
    HANKERS
    HANKY
    HANSELS
    HANTING
    HAOLE
    HAPLESS
    HAPPED
    HAPPING
    HAPTIC
    HARDASS
    HARDHAT
    HARDPAN
    HARED
    HAREMS
    HARING
    HARKING
    HARMED
    HARMINE
    HARNESS
    HARPIN
    HARPS
    HARROW
    HARSHER
    HARTS
    HASHING
    HASPING
    HASSLE
    HASTE
    HASTIER
    HATBAND
    HATCHER
    HATER
    HATING
    HATRACK
    HATTER
    HAUGHS
    HAULERS
    HAULMY
    HAUNTER
    HAUTE
    HAVENS
    HAVES
    HAVOC
    HAWING
    HAWKEYS
    HAWKS
    HAYCOCK
    HAYFORK
    HAYMOW
    HAYSEED
    HAZANS
    HAZELLY
    HAZIER
    HAZMAT
    HEADEND
    HEADILY
    HEADS
    HEALER
    HEALTHS
    HEAPING
    HEARERS
    HEARSE
    HEARTEN
    HEATED
    HEATHER
    HEAUME
    HEAVENS
    HEAVIES
    HEBETIC
    HECKS
    HEDDLE
    HEDGED
    HEDGING
    HEEDERS
    HEEHAWS
    HEELS
    HEEZING
    HEFTILY
    HEGARIS
    HEIFER
    HEIGHTS
    HEINIE
    HEIRESS
    HEISTED
    HEKTARE
    HELICON
    HELIUMS
    HELLED
    HELLING
    HELLOES
    HELMET
    HELOT
    HELPERS
    HELVED
    HEMATAL
    HEMIN
    HEMMED
    HEMPEN
    HENBANE
    HENGE
    HENNA
    HENPECK
    HENTING
    HEPCATS
    HEPTANE
    HERBAL
    HERBY
    HERDICS
    HEREAT
    HEREON
    HERIOT
    HERMAE
    HERNIA
    HEROES
    HEROINS
    HERONS
    HERRING
    HESSIAN
    HETERO
    HEUCH
    HEWED
    HEXADE
    HEXANE
    HEXER
    HEXONE
    HEXYL
    HEYDEY
    HICCUP
    HICKIES
    HIDALGO
    HIDER
    HIEING
    HIGGLES
    HIGHS
    HIGHTOP
    HIJACK
    HIJRAHS
    HIKES
    HILLER
    HILLOA
    HILLOS
    HILTING
    HIMSELF
    HINGE
    HINGING
    HINNY
    HINTS
    HIPLY
    HIPPIE
    HIPPO
    HIRABLE
    HIRER
    HIRPLED
    HIRSLED
    HISSED
    HISSIER
    HISTING
    HITCH
    HITLESS
    HITTING
    HOAGIES
    HOARDS
    HOARSEN
    HOAXER
    HOBBER
    HOBBITS
    HOBBY
    HOBOED
    HOCKED
    HOCKING
    HODAD
    HODDIN
    HOELIKE
    HOGFISH
    HOGGETS
    HOGMANE
    HOGTIED
    HOICKED
    HOISED
    HOISTER
    HOKIER
    HOKUM
    HOLDEN
    HOLDS
    HOLEY
    HOLIEST
    HOLIST
    HOLLA
    HOLLERS
    HOLLOED
    HOLLOW
    HOLMS
    HOMAGE
    HOMBRES
    HOMER
    HOMEY
    HOMIEST
    HOMINY
    HOMOS
    HONCHOS
    HONDLES
    HONEST
    HONGI
    HONING
    HONKEYS
    HONKY
    HONORS
    HOOCHIE
    HOODING
    HOODY
    HOOFERS
    HOOKAHS
    HOOKEY
    HOOKLET
    HOOLIE
    HOOPING
    HOOPOO
    HOORAY
    HOOTER
    HOOTY
    HOPED
    HOPHEAD
    HOPPERS
    HOPPLES
    HORAHS
    HORDED
    HORMONE
    HORNILY
    HORNY
    HORRORS
    HORSIER
    HORSTES
    HOSEL
    HOSES
    HOSIERS
    HOSTAGE
    HOSTESS
    HOSTS
    HOTCH
    HOTEL
    HOTLINK
    HOTSHOT
    HOTTEST
    HOUDAH
    HOUNDS
    HOUSE
    HOUSERS
    HOVELS
    HOWBEIT
    HOWDIES
    HOWFFS
    HOWLED
    HOWLING
    HOYLE
    HUBBIES
    HUBCAP
    HUCKS
    HUELESS
    HUFFISH
    HUGER
    HUGGING
    HULKIER
    HULLER
    HULLOAS
    HULLOS
    HUMANLY
    HUMBLED
    HUMBUGS
    HUMIC
    HUMMED
    HUMMUS
    HUMOUR
    HUMPH
    HUMPS
    HUMVEES
    HUNGER
    HUNKEY
    HUNKS
    HUNTERS
    HURDIES
    HURDS
    HURLEYS
    HURRAH
    HURRIER
    HURTER
    HURTLED
    HUSHED
    HUSKER
    HUSKING
    HUSSIES
    HUSTLES
    HUTLIKE
    HUTZPAH
    HUZZAHS
    HYALIN
    HYBRID
    HYDRAE
    HYDRIA
    HYDRIDS
    HYDROUS
    HYENINE
    HYING
    HYMENS
    HYMNING
    HYOIDAL
    HYPERS
    HYPHEN
    HYPOED
    HYPOS
    HYRAXES
    IAMBI
    IATRIC
    ICEBERG
    ICEFALL
    ICHNITE
    ICICLES
    ICING
    ICKIEST
    ICTERIC
    IDEAL
    IDEATED
    IDIOMS
    IDLER
    IDLING
    IDYLIST
    IFFIER
    IGLOOS
    IGNITE
    IGNOBLE
    IGNORES
    IHRAMS
    ILEAL
    ILEXES
    ILIUM
    ILLITE
    ILLUDE
    ILLUMES
    IMAGERS
    IMAGISM
    IMAMATE
    IMAUMS
    IMBED
    IMBIBES
    IMBROWN
    IMBUE
    IMIDES
    IMINES
    IMMERGE
    IMMIXED
    IMMURE
    IMPAINT
    IMPALE
    IMPARK
    IMPASTE
    IMPEACH
    IMPEDER
    IMPENDS
    IMPHEES
    IMPIOUS
    IMPLED
    IMPLY
    IMPORTS
    IMPOST
    IMPRESA
    IMPROV
    IMPULSE
    IMPUTER
    INANES
    INARCH
    INBOARD
    INBREED
    INCAGED
    INCASED
    INCEPT
    INCHER
    INCISAL
    INCITE
    INCLASP
    INCLUDE
    INCOMES
    INCUBI
    INCUR
    INCUSED
    INDEED
    INDEX
    INDICES
    INDIES
    INDITE
    INDIUMS
    INDOOR
    INDOWS
    INDRIS
    INDUCT
    INDUING
    INDUSIA
    INEPT
    INERTS
    INFANCY
    INFARCT
    INFECTS
    INFEST
    INFILL
    INFIXES
    INFLOW
    INFORM
    INFUSE
    INGATES
    INGLE
    INGOTS
    INGROUP
    INHALE
    INHAULS
    INHIBIN
    INHUMER
    INJECT
    INJURES
    INKERS
    INKJET
    INKLING
    INLACE
    INLANDS
    INLETS
    INMATES
    INNARDS
    INNERS
    INOCULA
    INPOURS
    INQUIRE
    INRUNS
    INSCULP
    INSERT
    INSIDE
    INSIPID
    INSOLE
    INSPANS
    INSTALS
    INSTEAD
    INSTILS
    INSURE
    INTACT
    INTEND
    INTER
    INTERS
    INTIMAS
    INTITLE
    INTONER
    INTRANT
    INTRON
    INTUIT
    INTWIST
    INURED
    INURNS
    INVADES
    INVENT
    INVEST
    INVITEE
    INVOKED
    INWALLS
    INWINDS
    INWRAPS
    IODID
    IODINE
    IODISES
    IODIZER
    IONIC
    IONIUM
    IONIZES
    IOTAS
    IRADE
    IRATEST
    IRIDES
    IRISED
    IRKED
    IRONE
    IRONIC
    IRONMAN
    IRRUPT
    ISATINS
    ISLAND
    ISLETED
    ISOBARS
    ISOGAMY
    ISOGONY
    ISOHYET
    ISOLOGS
    ISOPOD
    ISOTOPE
    ISSEIS
    ISSUERS
    ISTHMUS
    ITCHED
    ITCHY
    ITEMS
    ITSELF
    IVYLIKE
    IXORAS
    IZZARDS
    JABIRU
    JACALES
    JACINTH
    JACKED
    JACKIES
    JACKY
    JADED
    JADISH
    JAGERS
    JAGGERY
    JAGGY
    JAGUARS
    JAILOR
    JALAPIC
    JALOPS
    JAMBES
    JAMMER
    JAMMY
    JANGLES
    JAPANS
    JAPES
    JARGONS
    JARINAS
    JARRED
    JASMIN
    JASPERY
    JAUKING
    JAUNT
    JAUPING
    JAWANS
    JAWLIKE
    JAYVEE
    JAZZED
    JAZZILY
    JEALOUS
    JEEING
    JEEPS
    JEERS
    JEJUNA
    JELLED
    JELLO
    JEMIDAR
    JENNETS
    JERBOAS
    JERKED
    JERKILY
    JERKY
    JERRY
    JESSED
    JESTERS
    JESUITS
    JETLAGS
    JETSAM
    JETTIED
    JETTONS
    JEWEL
    JEWFISH
    JIBBED
    JIBBS
    JIBING
    JIFFY
    JIGGIER
    JIGGLES
    JIGSAWN
    JILLS
    JILTS
    JIMMIES
    JIMPLY
    JINGKO
    JINGLY
    JINKERS
    JINNIS
    JISMS
    JITTERY
    JIVES
    JNANA
    JOBBERS
    JOCKEY
    JOCOSE
    JOGGED
    JOGGLED
    JOHNS
    JOINERS
    JOINTED
    JOISTED
    JOKER
    JOKIEST
    JOLLIER
    JOLLY
    JOLTILY
    JONES
    JORAMS
    JOSEPH
    JOSHES
    JOSTLER
    JOTTERS
    JOUKED
    JOUNCE
    JOURNEY
    JOUSTER
    JOWED
    JOWLY
    JOYLESS
    JOYRODE
    JUBHAH
    JUCOS
    JUDGE
    JUDGING
    JUGAL
    JUGGING
    JUGHEAD
    JUGUM
    JUICERS
    JUICY
    JUJUIST
    JUKES
    JUMBAL
    JUMBLES
    JUMPER
    JUMPOFF
    JUNCOS
    JUNIOR
    JUNKERS
    JUNKIES
    JUNKY
    JUPES
    JURANT
    JURELS
    JURISTS
    JURYMEN
    JUSTEST
    JUSTLED
    JUTTED
    JUVENAL
    KABALA
    KABAYAS
    KABOBS
    KADIS
    KAFTAN
    KAIAK
    KAINITE
    KAJEPUT
    KALAM
    KALIANS
    KALIPHS
    KALONG
    KALPAK
    KAMES
    KAMSIN
    KANBAN
    KANTAR
    KAOLIN
    KAPAS
    KAPPAS
    KARAT
    KARMAS
    KAROSS
    KARSTS
    KASHA
    KASHRUT
    KATIONS
    KAURIS
    KAYAKED
    KAYOES
    KBARS
    KEBBIE
    KEBLAHS
    KECKLE
    KEDDAHS
    KEEFS
    KEELED
    KEENER
    KEENS
    KEESTER
    KEFIRS
    KEGGING
    KEISTER
    KELIMS
    KELPED
    KELPY
    KELTS
    KENAF
    KENDOS
    KENOS
    KEPIS
    KERATIN
    KERFED
    KERMIS
    KERNES
    KERRIA
    KERSEYS
    KETCHUP
    KETONE
    KETOSIS
    KEVELS
    KEXES
    KEYLESS
    KEYPALS
    KEYWAYS
    KHAFS
    KHALIFS
    KHAPHS
    KHEDAH
    KHETHS
    KIANG
    KIBBEH
    KIBBITZ
    KIBEI
    KIBLAH
    KICKED
    KICKOFF
    KIDDED
    KIDDING
    KIDDUSH
    KIDNEY
    KIEFS
    KILIMS
    KILLICK
    KILLOCK
    KILOBAR
    KILTED
    KILTING
    KIMCHIS
    KINAS
    KINDLE
    KINDRED
    KINESES
    KINFOLK
    KINGLET
    KININS
    KINKS
    KINSMAN
    KIPPEN
    KIRKMAN
    KIRNING
    KIRTLES
    KISMAT
    KISSER
    KISTFUL
    KITED
    KITHE
    KITING
    KITTEL
    KITTLE
    KIVAS
    KLAXON
    KLEPHTS
    KLICKS
    KLOOF
    KLUDGEY
    KLUGING
    KNACKED
    KNAPS
    KNAURS
    KNAWE
    KNEADED
    KNEEING
    KNEEPAD
    KNELLS
    KNIFER
    KNIGHTS
    KNITTER
    KNOBS
    KNOLL
    KNOPPED
    KNOTTED
    KNOUTS
    KNOWNS
    KNURL
    KOALA
    KOBOS
    KOJIS
    KOLHOZ
    KOLKOZY
    KONKED
    KOOKIE
    KOPECKS
    KOPJE
    KOPPIES
    KORMA
    KORUNY
    KOTOWED
    KOUMYS
    KOUSSO
    KRAALED
    KRAITS
    KRAUT
    KREUZER
    KRIMMER
    KRONER
    KROONS
    KRULLER
    KUDUS
    KUGELS
    KULAKS
    KUMMELS
    KURBASH
    KURUS
    KVASS
    KVETCH
    KWANZAS
    KYANITE
    KYLIKES
    KYTHE
    LAAGERS
    LABELED
    LABIAL
    LABOR
    LABOURS
    LABRUM
    LACES
    LACILY
    LACKERS
    LACONIC
    LACTARY
    LACTIC
    LACUNAL
    LADANUM
    LADDISH
    LADER
    LADING
    LADLED
    LADRON
    LADYKIN
    LAGENDS
    LAGGED
    LAGOONS
    LAHAR
    LAICISE
    LAIGHS
    LAIRING
    LAITY
    LAKES
    LAKINGS
    LALLED
    LAMBAST
    LAMBER
    LAMBIES
    LAMED
    LAMELY
    LAMEST
    LAMINAE
    LAMININ
    LAMPAS
    LAMPOON
    LANAIS
    LANCER
    LANCING
    LANDERS
    LANDS
    LANGREL
    LANGUOR
    LANITAL
    LANKLY
    LANOSE
    LANYARD
    LAPEL
    LAPIDES
    LAPISES
    LAPPETS
    LAPSERS
    LAPTOPS
    LARCHES
    LARDING
    LARDY
    LARGELY
    LARGISH
    LARINE
    LARKIER
    LARRUP
    LARVAE
    LASAGNE
    LASERS
    LASHES
    LASSES
    LASSO
    LASTED
    LASTS
    LATCHET
    LATEN
    LATENTS
    LATESTS
    LATHER
    LATHIER
    LATICES
    LATINAS
    LATKES
    LATTE
    LATTICE
    LAUDED
    LAUGH
    LAUNCES
    LAURAE
    LAVABO
    LAVASH
    LAVERS
    LAWBOOK
    LAWING
    LAWMEN
    LAWYERS
    LAXLY
    LAYERED
    LAYINS
    LAYOUT
    LAZAR
    LAZIED
    LAZING
    LEACH
    LEADED
    LEADIER
    LEADS
    LEAFING
    LEAGUED
    LEAKER
    LEAKS
    LEANER
    LEANS
    LEAPING
    LEARNED
    LEARY
    LEASES
    LEAST
    LEAVEN
    LEAVIER
    LECHED
    LECHING
    LECTINS
    LECYTHI
    LEDGIER
    LEEKS
    LEERS
    LEEWAYS
    LEFTISM
    LEGAL
    LEGATEE
    LEGEND
    LEGGED
    LEGGY
    LEGIONS
    LEGLESS
    LEGONGS
    LEGWORK
    LEISTER
    LEKVARS
    LEMMAS
    LEMONY
    LENDER
    LENGTH
    LENITE
    LENSE
    LENSMEN
    LENTILS
    LEONE
    LEPER
    LEPROUS
    LEPTONS
    LESION
    LESSENS
    LESSORS
    LETHAL
    LETTED
    LETUP
    LEUCITE
    LEUKON
    LEVEE
    LEVELER
    LEVERET
    LEVIES
    LEVULIN
    LEWIS
    LEXES
    LEZZES
    LIAISE
    LIANAS
    LIANOID
    LIBBERS
    LIBELS
    LIBIDO
    LIBRAE
    LICENCE
    LICHEN
    LICHT
    LICITLY
    LICKS
    LIDDED
    LIEFER
    LIENAL
    LIEUS
    LIFER
    LIFTERS
    LIFTS
    LIGASE
    LIGER
    LIGHTER
    LIGNIFY
    LIGULA
    LIGULES
    LIKELY
    LIKERS
    LIKUTA
    LILOS
    LIMAN
    LIMBATE
    LIMBI
    LIMBOS
    LIMED
    LIMEYS
    LIMING
    LIMITS
    LIMNERS
    LIMPA
    LIMPEST
    LIMPKIN
    LIMULI
    LINAGE
    LINDENS
    LINEAR
    LINEMEN
    LINERS
    LINGA
    LINGER
    LINGS
    LINGY
    LININGS
    LINKER
    LINKS
    LINNETS
    LINSEED
    LINTELS
    LINTOL
    LINUMS
    LIONS
    LIPIDES
    LIPLESS
    LIPOMAS
    LIPPERS
    LIQUATE
    LIQUIFY
    LIROT
    LISPED
    LISSOM
    LISTEL
    LISTERS
    LITAS
    LITERS
    LITHIA
    LITHO
    LITMUS
    LITRES
    LITTLE
    LIVED
    LIVENS
    LIVES
    LIVIERS
    LIVYER
    LLAMA
    LOACHES
    LOADS
    LOAFS
    LOAMY
    LOANS
    LOATHES
    LOBATED
    LOBBIES
    LOBEFIN
    LOBULAR
    LOCALE
    LOCATED
    LOCHANS
    LOCKBOX
    LOCKETS
    LOCKRAM
    LOCOED
    LOCULAR
    LOCULUS
    LOCUSTA
    LODGE
    LODGING
    LOFTER
    LOFTS
    LOGBOOK
    LOGGERS
    LOGGIER
    LOGIC
    LOGILY
    LOGJAM
    LOGOS
    LOIDED
    LOITERS
    LOLLING
    LOLLY
    LOMENTS
    LONGANS
    LONGERS
    LONGISH
    LOOED
    LOOFAHS
    LOOING
    LOOKISM
    LOOKUPS
    LOONEYS
    LOONS
    LOOPIER
    LOOSE
    LOOSER
    LOOTER
    LOPER
    LOPPER
    LOQUAT
    LORDED
    LOREAL
    LORIES
    LORRIES
    LOSER
    LOSSES
    LOTIC
    LOTTE
    LOTTES
    LOTUSES
    LOUDEST
    LOUIE
    LOUNGE
    LOUPE
    LOUPS
    LOUSE
    LOUSING
    LOUTS
    LOUVRES
    LOVAT
    LOVER
    LOWBALL
    LOWBROW
    LOWERS
    LOWINGS
    LOWLILY
    LOXES
    LOYALTY
    LUBED
    LUCENCE
    LUCERNS
    LUCITE
    LUCKIES
    LUCRE
    LUETICS
    LUFFS
    LUGES
    LUGGIE
    LUGWORM
    LULLING
    LUMBAR
    LUMENAL
    LUMPED
    LUMPIER
    LUMPY
    LUNATE
    LUNCHER
    LUNETTE
    LUNGEE
    LUNGFUL
    LUNGYI
    LUNKER
    LUNTS
    LUNULES
    LUPINS
    LURCH
    LURDANE
    LURES
    LURING
    LURKS
    LUSHING
    LUSTFUL
    LUSTRAL
    LUSTS
    LUTEAL
    LUTES
    LUTING
    LUXATE
    LWEIS
    LYCEA
    LYCHEE
    LYCRA
    LYINGS
    LYNCHED
    LYRATED
    LYRICS
    LYSATE
    LYSINE
    LYSOGEN
    LYTTAE
    MACABRE
    MACAW
    MACER
    MACHETE
    MACHS
    MACKLES
    MACON
    MACRONS
    MACULAS
    MADAM
    MADCAPS
    MADDERS
    MADLY
    MADRAS
    MADRONE
    MADUROS
    MAESTRI
    MAFIA
    MAFTIR
    MAGGOT
    MAGIC
    MAGLEV
    MAGNATE
    MAGNUM
    MAGPIES
    MAHJONG
    MAHOUTS
    MAIDENS
    MAIHEMS
    MAILER
    MAILLOT
    MAIMED
    MAINLY
    MAISTS
    MAJOR
    MAKAR
    MAKEUP
    MAKUTA
    MALAR
    MALATES
    MALGRE
    MALIGNS
    MALKINS
    MALLEI
    MALLOW
    MALMSEY
    MALTED
    MALTING
    MALTY
    MAMBOED
    MAMEYS
    MAMMA
    MAMMAS
    MAMMER
    MAMMEYS
    MAMMONS
    MANACLE
    MANAKIN
    MANATEE
    MANDALA
    MANED
    MANGA
    MANGELS
    MANGIER
    MANGLES
    MANGY
    MANIAC
    MANIHOT
    MANILLE
    MANITO
    MANKIND
    MANLY
    MANNAS
    MANNISH
    MANOS
    MANSE
    MANTEAU
    MANTID
    MANTLES
    MANTRAS
    MANUALS
    MANURER
    MAPLE
    MAPPERS
    MARABOU
    MARASCA
    MARBLER
    MARCELS
    MARCHES
    MARES
    MARGES
    MARINA
    MARISH
    MARKER
    MARKING
    MARKUP
    MARLINE
    MARLY
    MAROONS
    MARQUIS
    MARRER
    MARRING
    MARROWY
    MARSH
    MARTEN
    MARTING
    MARTYR
    MARVY
    MASCON
    MASERS
    MASHIE
    MASJIDS
    MASKERS
    MASONIC
    MASQUES
    MASSED
    MASSIFS
    MASTED
    MASTICS
    MASTS
    MATCHES
    MATERS
    MATIER
    MATINEE
    MATRASS
    MATSAH
    MATTERS
    MATTINS
    MATURED
    MATZAHS
    MATZOON
    MAUDS
    MAULERS
    MAUND
    MAUVE
    MAVIES
    MAWED
    MAXILLA
    MAXIMS
    MAXIXES
    MAYBES
    MAYED
    MAYHEMS
    MAYORS
    MAYST
    MAZARDS
    MAZES
    MAZUMA
    MBIRAS
    MEAGER
    MEALS
    MEANEST
    MEANS
    MEASLES
    MEATIER
    MEATUS
    MEDAKAS
    MEDDLED
    MEDIA
    MEDIALS
    MEDIATE
    MEDICO
    MEDINA
    MEDIVAC
    MEDULLA
    MEDUSAS
    MEERKAT
    MEETS
    MEGARA
    MEGILLA
    MEGOHMS
    MEIKLE
    MEIOSIS
    MELANIC
    MELDING
    MELENAS
    MELLING
    MELODIC
    MELONS
    MELTING
    MEMBER
    MEMOIRS
    MENACER
    MENAGES
    MENDIGO
    MENHIRS
    MENORAH
    MENSCH
    MENSH
    MENTAL
    MENTOR
    MENUS
    MEOWING
    MERCES
    MERCURY
    MERER
    MERGEE
    MERGING
    MERIT
    MERLES
    MERLOT
    MERMEN
    MERRY
    MESCALS
    MESHIER
    MESIAN
    MESONIC
    MESSANS
    MESSILY
    MESTEE
    MESTIZO
    METALS
    METAZOA
    METEPAS
    METHANE
    METHYL
    METING
    METONYM
    METOPON
    METRICS
    METROS
    METUMPS
    MEWLERS
    MEZES
    MEZUZOT
    MIAOUS
    MIASMA
    MIAUL
    MICELLA
    MICHES
    MICKLER
    MICRO
    MICROS
    MIDDAY
    MIDDLE
    MIDGE
    MIDGUTS
    MIDLEGS
    MIDNOON
    MIDSHIP
    MIDTERM
    MIDWIFE
    MIFFING
    MIGGS
    MIGNONS
    MIKADO
    MIKRA
    MIKVEH
    MILADI
    MILCH
    MILDER
    MILDING
    MILERS
    MILIEU
    MILKED
    MILKING
    MILKY
    MILLER
    MILLIER
    MILLRUN
    MILORDS
    MILTED
    MILTS
    MIMEO
    MIMES
    MIMICAL
    MIMOSAS
    MINCE
    MINCIER
    MINDERS
    MINED
    MINGIER
    MINGY
    MINICAR
    MINIMA
    MINING
    MINISH
    MINIVER
    MINNOW
    MINORED
    MINTER
    MINTY
    MINUSES
    MINUTIA
    MIOCENE
    MIRACLE
    MIRES
    MIRIN
    MIRKIER
    MIRRORS
    MISACT
    MISAIMS
    MISBILL
    MISCODE
    MISCUED
    MISDEAL
    MISDO
    MISDREW
    MISER
    MISFED
    MISFITS
    MISGROW
    MISHITS
    MISKEPT
    MISLAIN
    MISLIE
    MISMADE
    MISMET
    MISPART
    MISPLED
    MISSAID
    MISSEAT
    MISSENT
    MISSIES
    MISSIVE
    MISSUIT
    MISTED
    MISTEUK
    MISTOOK
    MISTYPE
    MISWORD
    MITERER
    MITIER
    MITOSES
    MITRED
    MITTENS
    MIXEDLY
    MIXING
    MIZENS
    MIZZLE
    MOANER
    MOATED
    MOBBERS
    MOBCAPS
    MOCHA
    MOCKERS
    MOCKUPS
    MODELED
    MODEMS
    MODEST
    MODIOLI
    MODULES
    MOFETTE
    MOGGY
    MOGULS
    MOHAWKS
    MOHURS
    MOILERS
    MOIRE
    MOISTLY
    MOLAL
    MOLDER
    MOLDY
    MOLINE
    MOLLIFY
    MOLOCH
    MOLTERS
    MOMENTA
    MOMISMS
    MOMSER
    MOMZERS
    MONADIC
    MONAXON
    MONERAN
    MONGER
    MONGOL
    MONIE
    MONISM
    MONKERY
    MONOCLE
    MONOFIL
    MONSOON
    MONTERO
    MONURON
    MOODIER
    MOOING
    MOOLEY
    MOONER
    MOONING
    MOONSET
    MOORIER
    MOOSE
    MOOTS
    MOPERY
    MOPING
    MOPPER
    MORAE
    MORALLY
    MORAY
    MORDENT
    MORELLO
    MORGEN
    MORIONS
    MORONIC
    MORPHIA
    MORPHS
    MORROW
    MORTAL
    MORTICE
    MORULAE
    MOSEY
    MOSHER
    MOSQUE
    MOSSES
    MOSTE
    MOTELS
    MOTHER
    MOTHY
    MOTILES
    MOTIVES
    MOTMOT
    MOTORS
    MOTTLER
    MOTTS
    MOUFLON
    MOULD
    MOULIN
    MOULTS
    MOUNTED
    MOURNER
    MOUSER
    MOUSILY
    MOUSY
    MOUTHY
    MOVED
    MOVIES
    MOWERS
    MOXIES
    MUCHLY
    MUCKED
    MUCKING
    MUCLUC
    MUCORS
    MUCOSE
    MUDBUG
    MUDCATS
    MUDDIER
    MUDDLED
    MUDFISH
    MUDHENS
    MUDRAS
    MUESLI
    MUFFING
    MUFFLES
    MUGFULS
    MUGGEES
    MUGGING
    MUGGY
    MUHLIES
    MUKLUKS
    MULCHED
    MULED
    MULEYS
    MULLAHS
    MULLENS
    MULLEY
    MULLOCK
    MUMBLER
    MUMMERS
    MUMMING
    MUMPERS
    MUNCHED
    MUNGOES
    MUNTIN
    MUONIC
    MURALS
    MUREIN
    MURIATE
    MURINES
    MURKILY
    MURMURS
    MURRE
    MURRHAS
    MURTHER
    MUSCID
    MUSCLY
    MUSES
    MUSHER
    MUSHING
    MUSICKS
    MUSJIDS
    MUSKIE
    MUSKITS
    MUSLIN
    MUSSELS
    MUSSY
    MUSTEES
    MUSTIER
    MUTABLE
    MUTASE
    MUTCH
    MUTER
    MUTINES
    MUTON
    MUTTONS
    MUTUEL
    MUUMUU
    MUZJIKS
    MUZZLER
    MYASES
    MYCOSES
    MYELINS
    MYLAR
    MYNHEER
    MYOMATA
    MYOPIC
    MYOSINS
    MYOTOME
    MYRRH
    MYSELF
    MYSTERY
    MYTHIER
    MYXOID
    NABBER
    NABOB
    NACHO
    NADAS
    NAEVOID
    NAGANA
    NAGGIER
    NAIADS
    NAILING
    NAIRU
    NAIVES
    NAKEDER
    NALED
    NAMER
    NANAS
    NANDIN
    NANKEEN
    NANNY
    NAPES
    NAPLESS
    NAPPER
    NAPPIES
    NARCIST
    NARCS
    NARIAL
    NARKING
    NARROWS
    NASAL
    NASION
    NASTILY
    NATES
    NATRIUM
    NATTIER
    NATURED
    NAUPLII
    NAVAID
    NAVARS
    NAVIES
    NAYSAID
    NEAPS
    NEARING
    NEATER
    NEATS
    NEBULAS
    NECKERS
    NECTAR
    NEEDED
    NEEDILY
    NEEDLES
    NEGATE
    NEGATOR
    NEGUS
    NEIGHS
    NELLIE
    NELUMBO
    NENES
    NEOLOGY
    NEOTYPE
    NEPHRIC
    NERDS
    NERITIC
    NERTS
    NERVES
    NERVOUS
    NESTED
    NESTLED
    NESTS
    NETOP
    NETTERS
    NETTLER
    NETWORK
    NEUMS
    NEURON
    NEUSTON
    NEVER
    NEWBIES
    NEWEST
    NEWMOWN
    NEWSIES
    NEWTONS
    NIACIN
    NIBBLED
    NICAD
    NICETY
    NICKED
    NICKING
    NICOISE
    NIDAL
    NIDES
    NIDUS
    NIELLO
    NIFFERS
    NIGELLA
    NIGGLED
    NIGHER
    NIGHTIE
    NIHIL
    NILGAUS
    NILLS
    NIMBUS
    NIMROD
    NINJA
    NINONS
    NIOBIC
    NIPPED
    NIPPING
    NIRVANA
    NITER
    NITID
    NITRATE
    NITRIDE
    NITRILS
    NITROUS
    NIVAL
    NIXIES
    NOBBILY
    NOBBY
    NOBLY
    NOCKS
    NODAL
    NODDIES
    NODDY
    NODULAR
    NOESIS
    NOGGINS
    NOIRISH
    NOISIER
    NOLOS
    NOMAS
    NOMINA
    NOMOI
    NONAGON
    NONBODY
    NONCOLA
    NONDRUG
    NONETS
    NONFAT
    NONGAYS
    NONJURY
    NONNEWS
    NONPAST
    NONPROS
    NONSTOP
    NONUSE
    NONWARS
    NONYLS
    NOODLE
    NOOKIE
    NOONING
    NOOSERS
    NOPALS
    NORIS
    NORMAL
    NORTHER
    NOSES
    NOSHES
    NOSING
    NOSTRUM
    NOTATE
    NOTCHER
    NOTER
    NOTICE
    NOTING
    NOUGATS
    NOUNS
    NOVAS
    NOVELS
    NOVICE
    NOWISE
    NOYADES
    NUANCES
    NUBBLES
    NUBILE
    NUCHAE
    NUCLEI
    NUDELY
    NUDGED
    NUDIE
    NUDISTS
    NUDZH
    NUGGETY
    NULLAHS
    NULLS
    NUMBERS
    NUMBS
    NUMMARY
    NUNCLES
    NURDS
    NURSED
    NURSING
    NUTATES
    NUTLIKE
    NUTRIA
    NUTTER
    NUTTY
    NUZZLES
    NYLON
    NYMPHAL
    OAFISH
    OAKMOSS
    OARING
    OARSMEN
    OATEN
    OATMEAL
    OBELI
    OBELISM
    OBESE
    OBEYERS
    OBIISMS
    OBJETS
    OBLATES
    OBLIGES
    OBLOQUY
    OBOLES
    OBOVOID
    OBSESS
    OBTESTS
    OBTUSER
    OBVIOUS
    OCCULTS
    OCEANIC
    OCELOID
    OCHERS
    OCHREAE
    OCHROUS
    OCKERS
    OCTADIC
    OCTANE
    OCTANTS
    OCTAVOS
    OCTOPOD
    OCTUPLY
    OCULI
    ODDBALL
    ODDLY
    ODEUM
    ODIUM
    ODORFUL
    ODOURS
    OEDEMA
    OESTRIN
    OFAYS
    OFFCUT
    OFFENDS
    OFFEROR
    OFFICES
    OFFLINE
    OFFSIDE
    OGAMS
    OGHAMIC
    OGLED
    OGREISH
    OGRISM
    OHMAGES
    OILBIRD
    OILCUPS
    OILIER
    OILMEN
    OINKED
    OKAPIS
    OKRAS
    OLDIES
    OLEATE
    OLEIC
    OLEOS
    OLINGO
    OLIVES
    OLOGY
    OMBERS
    OMELET
    OMENTA
    OMIKRON
    OMNIBUS
    ONAGRI
    ONEFOLD
    ONERY
    ONIONS
    ONLINE
    ONSETS
    ONUSES
    OOCYSTS
    OOGAMY
    OOLITE
    OOLOGIC
    OOMIACK
    OOMPAHS
    OORALIS
    OOTID
    OOZIEST
    OPAHS
    OPAQUER
    OPENEST
    OPERAND
    OPERONS
    OPIATE
    OPINES
    OPIOIDS
    OPPOSE
    OPPUGN
    OPSONIN
    OPTIMA
    OPTING
    OPUSES
    ORACLE
    ORALLY
    ORANGEY
    ORATES
    ORATORY
    ORBING
    ORBITS
    ORCHARD
    ORCHIS
    ORDAINS
    ORDERER
    ORDOS
    ORECTIC
    ORFRAYS
    ORGANON
    ORGASMS
    ORGIC
    ORIBIS
    ORIFICE
    ORIGINS
    ORISON
    ORLOP
    ORMOLUS
    OROIDE
    ORPHANS
    ORPINE
    ORRICES
    ORYXES
    OSCULAR
    OSETRAS
    OSMIC
    OSMOL
    OSMOLS
    OSMOTIC
    OSPREY
    OSSETRA
    OSSUARY
    OSTIARY
    OSTMARK
    OSTRAKA
    OTHER
    OTOCYST
    OTTAVA
    OTTOS
    OUGHT
    OUNCES
    OURANGS
    OURIE
    OUSTER
    OUTACTS
    OUTASK
    OUTBARK
    OUTBID
    OUTBULK
    OUTBYE
    OUTCOME
    OUTDARE
    OUTDOES
    OUTDREW
    OUTEATS
    OUTFACE
    OUTFELT
    OUTFITS
    OUTFOOT
    OUTGAZE
    OUTGOES
    OUTGUN
    OUTHIT
    OUTINGS
    OUTKEEP
    OUTLAID
    OUTLAWS
    OUTLED
    OUTLIES
    OUTMAN
    OUTPACE
    OUTPLOD
    OUTPOUR
    OUTPUTS
    OUTRANK
    OUTRIDE
    OUTROCK
    OUTROWS
    OUTSAID
    OUTSAY
    OUTSELL
    OUTSIDE
    OUTSITS
    OUTSPAN
    OUTSWAM
    OUTTASK
    OUTVIE
    OUTWALK
    OUTWEAR
    OUTWILL
    OUTWITS
    OUTYELL
    OVALITY
    OVARIES
    OVENS
    OVERARM
    OVERBID
    OVERDID
    OVERDUE
    OVERFAT
    OVERING
    OVERLET
    OVERMEN
    OVERRAN
    OVERSEA
    OVERT
    OVERUSE
    OVIFORM
    OVISACS
    OVOLO
    OVULARY
    OWLET
    OWNED
    OXALATE
    OXBOW
    OXEYES
    OXIDASE
    OXIDISE
    OXIMS
    OXTAILS
    OXYGENS
    OXYTONE
    OYSTERS
    OZONES
    OZONOUS
    PACAS
    PACEY
    PACIER
    PACKAGE
    PACKETS
    PACKS
    PADAUKS
    PADDING
    PADDOCK
    PADLOCK
    PADRE
    PADSHAH
    PAEON
    PAESANS
    PAGED
    PAGINAL
    PAGODAS
    PAIKING
    PAINED
    PAINTED
    PAIRING
    PAISANO
    PAJAMA
    PAKORAS
    PALADIN
    PALATE
    PALEA
    PALELY
    PALETOT
    PALIEST
    PALLED
    PALLID
    PALLORS
    PALMATE
    PALMIER
    PALMY
    PALPED
    PALSHIP
    PALTERS
    PAMPEAN
    PANACHE
    PANCAKE
    PANDECT
    PANDIT
    PANDOUR
    PANELED
    PANFUL
    PANGEN
    PANGS
    PANICUM
    PANNE
    PANNIER
    PANPIPE
    PANTIE
    PANTOS
    PANZER
    PAPADUM
    PAPAS
    PAPAYAS
    PAPERY
    PAPIST
    PAPPIES
    PAPRICA
    PAPULE
    PARABLE
    PARADOR
    PARAMO
    PARAPH
    PARBOIL
    PARCHES
    PARDIE
    PARDS
    PARENTS
    PARERS
    PAREU
    PARGED
    PARGO
    PARIANS
    PARISES
    PARKAS
    PARKS
    PARLED
    PARLOR
    PARODOI
    PAROLED
    PAROTIC
    PARRALS
    PARRIER
    PARROTY
    PARSECS
    PARSING
    PARTAKE
    PARTIED
    PARTITE
    PARTONS
    PARTYER
    PARVE
    PARVOS
    PASEOS
    PASHES
    PASSAGE
    PASSEL
    PASSIM
    PASSUS
    PASTEL
    PASTES
    PASTIL
    PASTIS
    PASTURE
    PATAMAR
    PATCHY
    PATENS
    PATES
    PATIN
    PATINED
    PATLY
    PATROLS
    PATSY
    PATTER
    PATTING
    PAUGHTY
    PAUPER
    PAUSER
    PAVANE
    PAVER
    PAVING
    PAVIOUR
    PAVISSE
    PAWING
    PAWNAGE
    PAWNERS
    PAWPAW
    PAYABLY
    PAYEE
    PAYLOAD
    PAYOFFS
    PAYOUT
    PEACED
    PEACHES
    PEAFOWL
    PEAHENS
    PEAKS
    PEALS
    PEARLED
    PEART
    PEASE
    PEATY
    PEBBLE
    PECANS
    PECHANS
    PECKER
    PECKS
    PECTENS
    PECULIA
    PEDALO
    PEDATE
    PEDES
    PEDLARS
    PEDOCAL
    PEEKED
    PEELERS
    PEENS
    PEEPS
    PEERESS
    PEERY
    PEEVISH
    PEGBOX
    PEINED
    PEISES
    PEKES
    PELAGE
    PELICAN
    PELLET
    PELORIA
    PELOTON
    PELTERS
    PELVIC
    PEMPHIX
    PENANG
    PENCELS
    PENDENT
    PENGOS
    PENIS
    PENNA
    PENNE
    PENNIA
    PENNON
    PENSEES
    PENSIVE
    PENTENE
    PENUCHE
    PEONAGE
    PEONY
    PEPINO
    PEPLUMS
    PEPPERS
    PEPPY
    PEPTIC
    PEPTIZE
    PERCEPT
    PERCOID
    PERDUES
    PEREIA
    PERFECT
    PERFUSE
    PERIDOT
    PERILLA
    PERIQUE
    PERIWIG
    PERKILY
    PERLITE
    PERMITS
    PERNODS
    PERPENT
    PERRONS
    PERSIST
    PERTAIN
    PERUKE
    PERUSED
    PERVS
    PESEWA
    PESOS
    PESTLE
    PESTS
    PETARD
    PETER
    PETITE
    PETREL
    PETROUS
    PETTERS
    PETTISH
    PETTY
    PEWITS
    PEYOTL
    PHAETON
    PHALLIC
    PHARYNX
    PHASIC
    PHATTER
    PHENOLS
    PHENYLS
    PHILTRE
    PHLOEM
    PHOBIAS
    PHOEBES
    PHONE
    PHONEYS
    PHONIES
    PHONONS
    PHORATE
    PHOTOED
    PHOTOS
    PHRASED
    PHRENIC
    PHYLAR
    PHYLON
    PHYSIC
    PHYTINS
    PHYTONS
    PIANIC
    PIANS
    PIAZZA
    PIBROCH
    PICARA
    PICCATA
    PICKED
    PICKETS
    PICKLES
    PICKY
    PICOTED
    PICRIC
    PIDDLE
    PIDDOCK
    PIECED
    PIEFORT
    PIERCER
    PIETA
    PIETY
    PIGEON
    PIGGIE
    PIGGINS
    PIGLIKE
    PIGNORA
    PIGOUTS
    PIGSTY
    PIKAKES
    PIKER
    PILAF
    PILAU
    PILEATE
    PILEUM
    PILFERS
    PILLAGE
    PILLING
    PILLOWY
    PILOTS
    PILULES
    PIMPING
    PIMPS
    PINATAS
    PINCH
    PINDERS
    PINENES
    PINETUM
    PINGER
    PINGOS
    PINIER
    PINITE
    PINKENS
    PINKEYE
    PINKISH
    PINKS
    PINNAL
    PINNERS
    PINNY
    PINONES
    PINTADA
    PINTLE
    PINTS
    PINWORK
    PIOLET
    PIOSITY
    PIPAL
    PIPER
    PIPETTE
    PIPIT
    PIPPIN
    PIQUED
    PIRACY
    PIRATE
    PIRAYAS
    PIROGI
    PISCINA
    PISHER
    PISMIRE
    PISSERS
    PISTES
    PISTOLS
    PITAPAT
    PITCHED
    PITFALL
    PITHING
    PITIERS
    PITMEN
    PITTA
    PIVOT
    PIXELS
    PIZAZZ
    PIZZAZZ
    PLACE
    PLACES
    PLACK
    PLAGAL
    PLAGUER
    PLAICES
    PLAINED
    PLAINTS
    PLANAR
    PLANED
    PLANETS
    PLANKS
    PLANTAR
    PLAQUE
    PLASHES
    PLASMIC
    PLASTER
    PLATANS
    PLATENS
    PLATIES
    PLATTED
    PLAUDIT
    PLAYDAY
    PLAYING
    PLAZA
    PLEADER
    PLEASER
    PLEATS
    PLEDGE
    PLEDGET
    PLENARY
    PLENTY
    PLEONIC
    PLEURAE
    PLEXAL
    PLIABLE
    PLICAE
    PLIERS
    PLINK
    PLINTHS
    PLODDED
    PLONKED
    PLOSIVE
    PLOTZ
    PLOVER
    PLOWERS
    PLOYED
    PLUCKER
    PLUGOLA
    PLUMBED
    PLUME
    PLUMMER
    PLUMPED
    PLUMS
    PLUNGED
    PLUNKER
    PLUSES
    PLUSHY
    PLUTONS
    PLYING
    POACHED
    POBOY
    POCKETS
    POCKY
    PODDED
    PODGY
    PODIUM
    PODZOL
    POETESS
    POETRY
    POGONIA
    POILUS
    POINTE
    POINTY
    POISES
    POITREL
    POKES
    POKIEST
    POLARS
    POLECAT
    POLER
    POLICE
    POLIES
    POLISH
    POLKA
    POLLED
    POLLER
    POLLOCK
    POLYCOT
    POLYNYI
    POLYPED
    POLYS
    POMADES
    POMFRET
    POMMIES
    POMPOMS
    PONCE
    PONCING
    PONDS
    PONGEES
    PONIARD
    PONTIL
    PONTOON
    POODLE
    POOFTAH
    POOHS
    POOLING
    POOPS
    POORISH
    POPEDOM
    POPGUNS
    POPLINS
    POPPER
    POPPIES
    POPPY
    PORCH
    PORED
    PORISM
    PORKIER
    PORKY
    PORNY
    PORTAL
    PORTER
    PORTLY
    POSADAS
    POSEUR
    POSIES
    POSOLE
    POSSET
    POSTAL
    POSTDOC
    POSTERS
    POSTING
    POSTOPS
    POTABLE
    POTATO
    POTEENS
    POTFULS
    POTHERS
    POTION
    POTLUCK
    POTSHOT
    POTTED
    POTTIER
    POTTO
    POUCH
    POUFF
    POUFFY
    POULTRY
    POUNCES
    POUNDS
    POURS
    POUTFUL
    POUTY
    POWER
    POWWOW
    POXIEST
    POZOLES
    PRAHU
    PRAISER
    PRAMS
    PRANG
    PRANKS
    PRATED
    PRATS
    PRAWNER
    PRAYER
    PREACHY
    PREAMPS
    PREBADE
    PREBILL
    PREBUY
    PRECENT
    PRECISE
    PRECURE
    PREDIAL
    PREED
    PREEN
    PREFAB
    PREFER
    PREFORM
    PRELATE
    PRELIMS
    PREMEAL
    PREMIE
    PREMIUM
    PREMUNE
    PREORAL
    PREPAY
    PREPPIE
    PREPUPA
    PRESA
    PRESENT
    PRESIDE
    PRESORT
    PRESSOR
    PRESTS
    PRETELL
    PRETOLD
    PRETYPE
    PREVIEW
    PREWAR
    PREWORK
    PREXY
    PREYS
    PRICE
    PRICEY
    PRICKED
    PRICKS
    PRIDES
    PRIES
    PRILL
    PRIMAGE
    PRIME
    PRIMERS
    PRIMLY
    PRIMP
    PRIMULA
    PRINK
    PRINTED
    PRIOR
    PRISED
    PRISMS
    PRISSES
    PRIVET
    PRIVITY
    PRIZERS
    PROBANG
    PROBERS
    PROBITY
    PROCTOR
    PRODRUG
    PROEMS
    PROFILE
    PROGENY
    PROGUN
    PROLANS
    PROLES
    PROLONG
    PROMOS
    PRONATE
    PRONGS
    PROOFED
    PROPELS
    PROPHET
    PROPONE
    PROPYL
    PROSE
    PROSES
    PROSO
    PROSS
    PROSY
    PROTEGE
    PROTEST
    PROTONS
    PROUDER
    PROVER
    PROVING
    PROWER
    PROWLER
    PROXY
    PRUDISH
    PRUNES
    PRUTA
    PRYERS
    PSALMIC
    PSCHENT
    PSHAW
    PSOAS
    PSYCHE
    PSYCHOS
    PSYOPS
    PTERYLA
    PTOSES
    PUBERTY
    PUBLICS
    PUCKER
    PUDDING
    PUDDLY
    PUDGY
    PUFFED
    PUFFILY
    PUFFY
    PUGGISH
    PUGREE
    PUJAHS
    PUKKA
    PULIK
    PULLER
    PULLEYS
    PULLUP
    PULPERS
    PULPITS
    PULQUES
    PULSE
    PULSING
    PUMELOS
    PUMMEL
    PUMPERS
    PUNCH
    PUNDIT
    PUNGLES
    PUNISH
    PUNKAHS
    PUNKEY
    PUNKIN
    PUNNED
    PUNNIER
    PUNTER
    PUNTOS
    PUPARIA
    PUPFISH
    PUPPET
    PUPUS
    PURDAH
    PUREES
    PURFLED
    PURGER
    PURIN
    PURISM
    PURITY
    PURLING
    PURPLED
    PURPOSE
    PURRS
    PURSES
    PURSUED
    PURTIER
    PUSES
    PUSHFUL
    PUSHROD
    PUSLEYS
    PUSSLEY
    PUTDOWN
    PUTON
    PUTRID
    PUTTER
    PUTTIER
    PUTTY
    PUZZLED
    PYEMIA
    PYGMIES
    PYJAMAS
    PYLORI
    PYOSIS
    PYRENE
    PYREXES
    PYRITE
    PYROLAS
    PYROS
    PYRROLS
    PYXES
    PYXIS
    QAIDS
    QINTAR
    QUACK
    QUADRAT
    QUAFF
    QUAGGAS
    QUAHOGS
    QUAIL
    QUAKE
    QUAKIER
    QUALIA
    QUALMY
    QUANTA
    QUANTUM
    QUARRY
    QUARTES
    QUARTS
    QUASHED
    QUASSES
    QUATRES
    QUAYS
    QUEAN
    QUEENED
    QUEERER
    QUELL
    QUERIDA
    QUERN
    QUESTER
    QUEUED
    QUEYS
    QUICHES
    QUICKLY
    QUIETEN
    QUIFF
    QUILLET
    QUILTS
    QUINELA
    QUININS
    QUINOL
    QUINT
    QUINTAS
    QUINTIN
    QUIPPUS
    QUIRE
    QUIRKED
    QUIRTS
    QUITTER
    QUIXOTE
    QUOHOG
    QUOIT
    QUOLL
    QUORUMS
    QUOTER
    QUOTING
    QWERTYS
    RABBET
    RABBINS
    RABBLE
    RABIC
    RACED
    RACER
    RACHETS
    RACIEST
    RACISMS
    RACKERS
    RACKING
    RACOON
    RADDED
    RADIAL
    RADIANT
    RADICLE
    RADISH
    RADIXES
    RADULA
    RAFFIAS
    RAFFLES
    RAFTING
    RAGED
    RAGGEDY
    RAGGLE
    RAGIS
    RAGOUT
    RAGTOP
    RAIDED
    RAILBUS
    RAILING
    RAINED
    RAINS
    RAISERS
    RAISINY
    RAJAS
    RAKEOFF
    RAKIS
    RALLIER
    RALLYES
    RAMADAS
    RAMBLE
    RAMEES
    RAMETS
    RAMJET
    RAMMIER
    RAMONAS
    RAMPART
    RAMPOLE
    RAMSONS
    RANCES
    RANCHO
    RANCOUR
    RANDOM
    RANEES
    RANGES
    RANIDS
    RANKEST
    RANKLES
    RANSOM
    RANTING
    RAPED
    RAPHE
    RAPHIS
    RAPIER
    RAPINI
    RAPPEES
    RAPPERS
    RAPTOR
    RAREFY
    RARIFY
    RASCALS
    RASHER
    RASING
    RASPING
    RASSLED
    RASURES
    RATAL
    RATATAT
    RATCHET
    RATERS
    RATHER
    RATING
    RATIOS
    RATLINE
    RATTAIL
    RATTEN
    RATTING
    RATTLES
    RATTRAP
    RAUNCHY
    RAVED
    RAVELLY
    RAVENS
    RAVINE
    RAVINS
    RAWHIDE
    RAWNESS
    RAYAHS
    RAYLIKE
    RAZEED
    RAZING
    RAZZES
    REACHES
    READAPT
    READERS
    READING
    READS
    REAGINS
    REALIA
    REALITY
    REALMS
    REAMED
    REANNEX
    REAPPLY
    REARGUE
    REARS
    REAVAIL
    REAVES
    REAWOKE
    REBATE
    REBATOS
    REBECKS
    REBEL
    REBILLS
    REBLENT
    REBOIL
    REBOOTS
    REBORES
    REBRED
    REBUILT
    REBURY
    REBUY
    RECANED
    RECAPS
    RECCES
    RECEIVE
    RECESS
    RECHEWS
    RECITAL
    RECITS
    RECKS
    RECLASP
    RECOALS
    RECODE
    RECOIN
    RECON
    RECORD
    RECOUP
    RECROSS
    RECTI
    RECTORY
    RECTUS
    RECUSE
    RECYCLE
    REDATE
    REDBAYS
    REDBUG
    REDDED
    REDDEST
    REDDLES
    REDEEM
    REDEYE
    REDHEAD
    REDIAS
    REDIPT
    REDNECK
    REDOING
    REDOUBT
    REDOWAS
    REDRAW
    REDREW
    REDROOT
    REDTOP
    REDUCED
    REDWING
    REEARN
    REEDIER
    REEDITS
    REEFED
    REEFS
    REEKERS
    REELECT
    REELS
    REENJOY
    REEST
    REEVES
    REFACED
    REFECTS
    REFEELS
    REFENCE
    REFFING
    REFILL
    REFINDS
    REFIRE
    REFIX
    REFLATE
    REFLEX
    REFLOWN
    REFOLD
    REFOUND
    REFRIED
    REFUEL
    REFUGES
    REFUSE
    REFUTE
    REGAINS
    REGALES
    REGATTA
    REGENCY
    REGGAES
    REGIMEN
    REGINAS
    REGIVEN
    REGLOSS
    REGLUES
    REGNANT
    REGRAFT
    REGRESS
    REGROOM
    REGULAR
    REHANG
    REHEARS
    REHEM
    REHIRES
    REIFIES
    REIGNS
    REINING
    REINTER
    REIVER
    REJECTS
    REJOINS
    REKNIT
    RELACE
    RELANDS
    RELATES
    RELAXES
    RELEARN
    RELENTS
    RELIANT
    RELIED
    RELIES
    RELINED
    RELISH
    RELIVED
    RELOAN
    RELOOKS
    RELUMES
    REMAIN
    REMAN
    REMAPS
    REMATE
    REMEETS
    REMERGE
    REMINDS
    REMISES
    REMIXED
    REMOLD
    REMORSE
    REMOVAL
    REMUDA
    RENAME
    RENDERS
    RENEGER
    RENEWAL
    RENIGS
    RENNETS
    RENTAL
    RENTERS
    RENVOI
    REOILED
    REPACK
    REPAIRS
    REPARKS
    REPAVE
    REPEAL
    REPEGS
    REPERK
    REPINER
    REPLANS
    REPLEAD
    REPLIED
    REPLOW
    REPOLLS
    REPOSE
    REPOT
    REPPED
    REPRINT
    REPROS
    REPUGNS
    REPUTED
    REQUINS
    RERAISE
    RERENT
    RERISEN
    REROOFS
    RESAID
    RESAT
    RESAY
    RESCUE
    RESEALS
    RESEAUX
    RESEE
    RESEEN
    RESEND
    RESET
    RESEWS
    RESHIP
    RESHOES
    RESHOWN
    RESIDER
    RESIFT
    RESILE
    RESINED
    RESIT
    RESIZE
    RESOAK
    RESOLD
    RESORB
    RESOW
    RESPADE
    RESPIRE
    RESPOOL
    RESTAFF
    RESTED
    RESTIVE
    RESTUDY
    RESUME
    RETABLE
    RETAIL
    RETAKEN
    RETAPED
    RETAX
    RETCHES
    RETEARS
    RETENE
    RETIA
    RETIED
    RETIME
    RETINAL
    RETINT
    RETIREE
    RETOOK
    RETORT
    RETRACK
    RETREAT
    RETRIMS
    RETTED
    RETURN
    RETYPE
    REUNITE
    REUTTER
    REVEALS
    REVELS
    REVERE
    REVERS
    REVERY
    REVIEW
    REVILES
    REVISES
    REVIVED
    REVOKED
    REVOLVE
    REVUES
    REWAKED
    REWARDS
    REWAXED
    REWED
    REWET
    REWINDS
    REWOKE
    REWORE
    REWOVE
    REWRITE
    REYNARD
    REZONES
    RHAPHE
    RHEBOKS
    RHETOR
    RHEUMY
    RHIZOMA
    RHODORA
    RHOMBUS
    RHUMBA
    RHYMED
    RHYTA
    RIALS
    RIATA
    RIBANDS
    RIBBIER
    RIBBY
    RIBLET
    RIBWORT
    RICHEN
    RICHLY
    RICKED
    RICKING
    RICRACS
    RIDDEN
    RIDDLED
    RIDERS
    RIDGELS
    RIDGING
    RIDLEYS
    RIFELY
    RIFFLE
    RIFLE
    RIFLES
    RIFTING
    RIGGING
    RIGHTO
    RIGOR
    RIKSHAW
    RILIEVO
    RILLET
    RIMER
    RIMIEST
    RIMMER
    RIMPLE
    RINDED
    RINGER
    RINGS
    RINSED
    RIOJA
    RIOTING
    RIPELY
    RIPER
    RIPING
    RIPOSTS
    RIPPLE
    RIPPLY
    RIPSAWS
    RISERS
    RISIBLY
    RISKERS
    RISKY
    RISTRAS
    RITES
    RITZES
    RIVAGES
    RIVED
    RIVET
    RIVIERE
    ROACH
    ROADEOS
    ROAMED
    ROANS
    ROARS
    ROBALO
    ROBBER
    ROBBINS
    ROBINS
    ROBOTRY
    ROCHETS
    ROCKERY
    ROCKOON
    RODDED
    RODEOED
    RODMAN
    ROGER
    ROGUERY
    ROILIER
    ROLES
    ROLFS
    ROLLING
    ROLLWAY
    ROMANCE
    ROMEO
    ROMPING
    RONDELS
    RONIONS
    RONYONS
    ROOFIE
    ROOKED
    ROOKING
    ROOMERS
    ROOMILY
    ROOSED
    ROOST
    ROOTCAP
    ROOTING
    ROOTS
    ROPERS
    ROPIER
    ROQUES
    ROSARIA
    ROSEBAY
    ROSEOLA
    ROSETTE
    ROSILY
    ROSINS
    ROSTRA
    ROTATE
    ROTCHE
    ROTIFER
    ROTOS
    ROTTERS
    ROUBLE
    ROUENS
    ROUGH
    ROUGHS
    ROULEAU
    ROUNDLY
    ROUPIER
    ROUSE
    ROUSING
    ROUTE
    ROUTH
    ROVED
    ROVING
    ROWBOAT
    ROWED
    ROWENS
    ROWLOCK
    ROYALS
    RUANA
    RUBASSE
    RUBBER
    RUBBISH
    RUBBY
    RUBEOLA
    RUBIES
    RUBLE
    RUBOUTS
    RUCHE
    RUCKING
    RUCKUS
    RUDDILY
    RUDDS
    RUDERY
    RUFFE
    RUFFLE
    RUFFS
    RUGATE
    RUGGERS
    RUGOSA
    RUINED
    RUINOUS
    RULERS
    RULINGS
    RUMBAS
    RUMBLY
    RUMMAGE
    RUMMIES
    RUMOUR
    RUMPLY
    RUNDLE
    RUNGS
    RUNLESS
    RUNNER
    RUNOFF
    RUNTIER
    RUNWAYS
    RUPTURE
    RUSHED
    RUSHES
    RUSKS
    RUSTED
    RUSTING
    RUSTS
    RUTILES
    RUTTILY
    RYKES
    RYOTS
    SABBAT
    SABED
    SABES
    SABIR
    SABOTS
    SABRES
    SACCADE
    SACHEMS
    SACKER
    SACLIKE
    SACRALS
    SACRUMS
    SADDHU
    SADDLES
    SADHUS
    SADIST
    SAFARIS
    SAFETY
    SAGAMAN
    SAGELY
    SAGGARD
    SAGGIER
    SAGOS
    SAHIWAL
    SAIGA
    SAILING
    SAIMINS
    SAINTED
    SAIYID
    SAKERS
    SALABLE
    SALALS
    SALEP
    SALIENT
    SALINES
    SALLIED
    SALLOWY
    SALMONS
    SALOON
    SALPAE
    SALPINX
    SALTANT
    SALTERS
    SALTILY
    SALTPAN
    SALUTE
    SALVE
    SALVIA
    SALVOES
    SAMARA
    SAMBALS
    SAMBHUR
    SAMBUR
    SAMEKH
    SAMISEN
    SAMOSA
    SAMPANS
    SAMPS
    SANCTA
    SANDBAR
    SANDER
    SANDHOG
    SANDMEN
    SANELY
    SANGAR
    SANGH
    SANING
    SANNOP
    SANSARS
    SANTIMI
    SANTO
    SANTOUR
    SAPHENA
    SAPLING
    SAPOTAS
    SAPPED
    SAPPILY
    SAPWOOD
    SARCASM
    SARDANA
    SARDS
    SARGO
    SARKIER
    SARODE
    SAROS
    SARSENS
    SASHAYS
    SASIN
    SASSIER
    SATANG
    SATAY
    SATEENS
    SATIN
    SATIRE
    SATORI
    SATSUMA
    SAUCE
    SAUCH
    SAUCY
    SAUGHY
    SAUNAED
    SAURIAN
    SAUTED
    SAVAGE
    SAVANT
    SAVED
    SAVIN
    SAVINS
    SAVORED
    SAVOURS
    SAVVIER
    SAWBUCK
    SAWFISH
    SAWLOGS
    SAWYERS
    SAYABLE
    SAYEST
    SAYST
    SCABBY
    SCALADE
    SCALARS
    SCALE
    SCALERS
    SCALL
    SCALPEL
    SCAMMER
    SCAMPS
    SCANNED
    SCANTER
    SCAPED
    SCARAB
    SCARED
    SCARF
    SCARIFY
    SCARPED
    SCARRED
    SCARTS
    SCATHES
    SCATTS
    SCAUR
    SCENDED
    SCENIC
    SCEPTER
    SCHAVS
    SCHEMER
    SCHISMS
    SCHIZY
    SCHLOCK
    SCHMEAR
    SCHMOOS
    SCHNOZ
    SCHOOLS
    SCHROD
    SCHUIT
    SCHUSS
    SCILLA
    SCISSOR
    SCLERAE
    SCOFFER
    SCOLDS
    SCONCES
    SCOOPED
    SCOOTED
    SCOPES
    SCORE
    SCORIA
    SCORNED
    SCOTERS
    SCOTTIE
    SCOURS
    SCOUTER
    SCOWED
    SCOWLS
    SCRAICH
    SCRAPE
    SCRAPPY
    SCRAWLY
    SCREAM
    SCREEDS
    SCREWED
    SCRIBAL
    SCRIED
    SCRIMPS
    SCRIPT
    SCROD
    SCROOCH
    SCROTAL
    SCRUBS
    SCRUMS
    SCUBAED
    SCUDS
    SCUFFS
    SCULKS
    SCULP
    SCULPTS
    SCUMMER
    SCUPS
    SCURRY
    SCUTCH
    SCUTTLE
    SCYPHI
    SEABAG
    SEABOOT
    SEAFOWL
    SEALER
    SEALS
    SEAMER
    SEAMY
    SEARED
    SEASICK
    SEATER
    SEAWAN
    SEAWAY
    SEBUM
    SECCOS
    SECERN
    SECONDE
    SECPARS
    SECTARY
    SECTS
    SECURER
    SEDATE
    SEDERS
    SEDILE
    SEDUCES
    SEEDED
    SEEDING
    SEEDY
    SEEKING
    SEELY
    SEEMLY
    SEEPING
    SEESAW
    SEGETAL
    SEGNO
    SEGUES
    SEIFS
    SEINES
    SEISERS
    SEISM
    SEISORS
    SEIZED
    SEIZING
    SEJANT
    SELECT
    SELFING
    SELLE
    SELLOFF
    SELTZER
    SEMATIC
    SEMENS
    SEMIMAT
    SEMIRAW
    SENARII
    SENDAL
    SENDING
    SENECA
    SENGI
    SENILES
    SENNAS
    SENOPIA
    SENORS
    SENSED
    SENSOR
    SENTE
    SEPALED
    SEPOY
    SEPTA
    SEPTETS
    SEPTUM
    SEQUENT
    SERACS
    SERAL
    SERDAB
    SERENE
    SEREST
    SERGE
    SERGING
    SERIEMA
    SERIN
    SERINS
    SEROSAE
    SEROW
    SERRATE
    SERUMAL
    SERVE
    SERVICE
    SESAME
    SESTETS
    SETBACK
    SETONS
    SETTEE
    SETTLE
    SETTS
    SEVENTH
    SEVERED
    SEWABLE
    SEWAR
    SEWERS
    SEXIER
    SEXISMS
    SEXPOTS
    SEXTET
    SEXTONS
    SFUMATO
    SHACKO
    SHADER
    SHADILY
    SHADOWY
    SHAFT
    SHAGS
    SHAIRN
    SHAKER
    SHAKILY
    SHAKY
    SHALIER
    SHALOM
    SHAMANS
    SHAMES
    SHAMMES
    SHAMOY
    SHANDY
    SHANTEY
    SHAPE
    SHAPERS
    SHARDS
    SHARES
    SHARIFS
    SHARKS
    SHARPED
    SHARPS
    SHAUGHS
    SHAVED
    SHAVIE
    SHAWL
    SHAWN
    SHEAFED
    SHEARED
    SHEATHE
    SHEBANG
    SHEDS
    SHEENS
    SHEERER
    SHEETED
    SHEGETZ
    SHEILA
    SHELF
    SHELLS
    SHELTIE
    SHELVES
    SHEOL
    SHERD
    SHERIFS
    SHERRY
    SHEWED
    SHEWS
    SHICKER
    SHIELDS
    SHIEST
    SHIFTY
    SHIKSA
    SHILL
    SHIMMED
    SHINDY
    SHINERS
    SHINILY
    SHINS
    SHIPPED
    SHIPWAY
    SHIRKER
    SHIRT
    SHITAKE
    SHITTY
    SHIVE
    SHIVITI
    SHLEPS
    SHLUBS
    SHMEAR
    SHMUCKS
    SHOAL
    SHOAT
    SHOCKS
    SHOEING
    SHOFAR
    SHOGS
    SHOLOM
    SHOOING
    SHOOLS
    SHOOTS
    SHOPPE
    SHORAN
    SHORING
    SHORTED
    SHORTLY
    SHOTGUN
    SHOTTS
    SHOUTS
    SHOVER
    SHOWED
    SHOWILY
    SHOWOFF
    SHRANK
    SHREWED
    SHRIEVE
    SHRILL
    SHRIMPY
    SHRINKS
    SHRIVEN
    SHROUD
    SHRUBS
    SHTETL
    SHTIK
    SHUCKS
    SHUNNED
    SHUNTER
    SHUSHES
    SHUTING
    SHUTTLE
    SHYING
    SIALIC
    SIAMANG
    SIBYLIC
    SICES
    SICKEES
    SICKIE
    SICKLED
    SICKOUT
    SIDEBAR
    SIDES
    SIDLE
    SIDLING
    SIEMENS
    SIERRAN
    SIEURS
    SIEVING
    SIFTERS
    SIGHER
    SIGHTED
    SIGILS
    SIGMA
    SIGNAGE
    SIGNEES
    SIGNIFY
    SIGNORE
    SIKAS
    SILANE
    SILENT
    SILEXES
    SILICON
    SILKIE
    SILKS
    SILLIES
    SILOING
    SILTS
    SILVAN
    SILVERS
    SIMARS
    SIMILE
    SIMLIN
    SIMNELS
    SIMOONS
    SIMPLES
    SINCE
    SINEWS
    SINGER
    SINGLED
    SINHS
    SINKS
    SINNING
    SINTERS
    SIPED
    SIPPED
    SIPPING
    SIREES
    SIRLOIN
    SIRRAS
    SIRUPS
    SISKIN
    SISSY
    SITAR
    SITES
    SITTERS
    SITUS
    SIXFOLD
    SIXTES
    SIXTY
    SIZED
    SIZIEST
    SIZZLER
    SKALDIC
    SKANKS
    SKATERS
    SKATOLS
    SKEANS
    SKEES
    SKEIGH
    SKELLS
    SKELPED
    SKENES
    SKETCH
    SKEWING
    SKIDDED
    SKIDOOS
    SKIERS
    SKIFFS
    SKILLED
    SKIMO
    SKIMPY
    SKINKER
    SKINS
    SKIPS
    SKIRRED
    SKIRTER
    SKITING
    SKIVED
    SKIVVY
    SKOALED
    SKOSH
    SKULK
    SKULLED
    SKUNKY
    SKYDOVE
    SKYJACK
    SKYMAN
    SKYSURF
    SLABBED
    SLACKEN
    SLAGGY
    SLAKED
    SLALOM
    SLANDER
    SLANK
    SLANTY
    SLASHED
    SLATED
    SLATHER
    SLATY
    SLAVERY
    SLAVISH
    SLAYING
    SLEAZE
    SLEDDER
    SLEEK
    SLEEKLY
    SLEEPS
    SLEETY
    SLEIGHS
    SLEUTHS
    SLICED
    SLICK
    SLICKS
    SLIDES
    SLIEVES
    SLIMED
    SLIMLY
    SLIMSY
    SLINK
    SLIPED
    SLIPPER
    SLIPUPS
    SLITTER
    SLOBBY
    SLOGGED
    SLOJD
    SLOPED
    SLOPPED
    SLOSHES
    SLOTTED
    SLOUGHS
    SLOWER
    SLOWS
    SLUBS
    SLUED
    SLUGGED
    SLUICES
    SLUMISM
    SLUMPED
    SLURB
    SLURPS
    SLUSHED
    SLYER
    SLYPES
    SMALL
    SMALTO
    SMARMS
    SMARTER
    SMASH
    SMATTER
    SMEARER
    SMEEK
    SMELL
    SMELT
    SMERKED
    SMIDGES
    SMILER
    SMILING
    SMIRKS
    SMITES
    SMITTEN
    SMOGS
    SMOKES
    SMOKY
    SMOOCHY
    SMOTE
    SMUDGY
    SMUSHED
    SMUTTED
    SNACKS
    SNAGGED
    SNAILS
    SNAKIER
    SNAPPER
    SNARER
    SNARFS
    SNARL
    SNASH
    SNATHE
    SNAWS
    SNEAKS
    SNECK
    SNEERED
    SNEEZE
    SNELL
    SNIBS
    SNIDE
    SNIFFED
    SNIFFY
    SNIPE
    SNIPING
    SNIPS
    SNOBBY
    SNOODED
    SNOOKS
    SNOOPED
    SNOOTED
    SNOOZER
    SNORED
    SNORKEL
    SNOTS
    SNOUTY
    SNOWILY
    SNOWY
    SNUCK
    SNUFFLY
    SNUGGLE
    SOAKED
    SOAPBOX
    SOAPILY
    SOARER
    SOAVES
    SOBBING
    SOBERLY
    SOCAGES
    SOCIAL
    SOCKETS
    SOCKO
    SOCMEN
    SODDIES
    SODIUMS
    SOFABED
    SOFFITS
    SOFTER
    SOFTLY
    SOGGILY
    SOILED
    SOIREES
    SOKES
    SOLACER
    SOLANIN
    SOLAR
    SOLATIA
    SOLDI
    SOLELY
    SOLFEGE
    SOLIDI
    SOLION
    SOLOIST
    SOLUBLY
    SOLUTE
    SOLVENT
    SOMAN
    SOMBER
    SOMEWAY
    SOMONI
    SONARS
    SONDERS
    SONHOOD
    SONLY
    SONOVOX
    SOOEY
    SOOTED
    SOOTHES
    SOOTING
    SOPHIST
    SOPITES
    SOPPING
    SORBATE
    SORBIC
    SORDID
    SORDORS
    SORELY
    SORGHOS
    SORINGS
    SORNERS
    SOROSES
    SORRILY
    SORTED
    SORTIES
    SOTOL
    SOUARIS
    SOUDANS
    SOUGHT
    SOULS
    SOUNDS
    SOUPS
    SOURED
    SOURLY
    SOUSES
    SOUTERS
    SOVIET
    SOWABLE
    SOWCARS
    SOWING
    SOYUZES
    SOZZLED
    SPACES
    SPACKLE
    SPADERS
    SPAED
    SPAHI
    SPAITS
    SPALLED
    SPAMMER
    SPANGLE
    SPANKER
    SPARE
    SPARES
    SPARGES
    SPARKED
    SPARKY
    SPARS
    SPASMED
    SPATHAL
    SPATIAL
    SPATZLE
    SPAVINS
    SPAYED
    SPEAK
    SPEANS
    SPECCED
    SPECK
    SPECTER
    SPEED
    SPEEDS
    SPEELS
    SPEILED
    SPEISE
    SPELLED
    SPELTS
    SPENCES
    SPENSE
    SPERMS
    SPEWS
    SPHERE
    SPHINX
    SPICATE
    SPICERY
    SPICING
    SPICULE
    SPIED
    SPIELS
    SPIFF
    SPIGOTS
    SPIKES
    SPIKS
    SPILING
    SPILT
    SPINAL
    SPINE
    SPINET
    SPINNY
    SPINOUS
    SPINULA
    SPIRALS
    SPIRED
    SPIRIER
    SPIRT
    SPITAL
    SPITING
    SPITZ
    SPLAKES
    SPLAY
    SPLEENY
    SPLENTS
    SPLIFF
    SPLINT
    SPLORE
    SPLURGY
    SPOILER
    SPOKEN
    SPONGED
    SPONSAL
    SPOOFER
    SPOOKS
    SPOOLS
    SPOONY
    SPORE
    SPORRAN
    SPORTS
    SPOTTED
    SPOUSED
    SPOUTS
    SPRANG
    SPRAWLS
    SPRAYS
    SPRENT
    SPRIGHT
    SPRINGY
    SPRITES
    SPRUCE
    SPRUE
    SPRYER
    SPUDS
    SPUMED
    SPUMONI
    SPUNKIE
    SPURN
    SPURRER
    SPURTED
    SPUTNIK
    SQUABBY
    SQUALL
    SQUAMAE
    SQUARK
    SQUATLY
    SQUAWKS
    SQUEAL
    SQUELCH
    SQUIFFY
    SQUINNY
    SQUIRED
    SQUIRT
    SQUUSH
    STABBER
    STABLES
    STACKER
    STADDLE
    STADIUM
    STAGE
    STAGEY
    STAGIER
    STAID
    STAIN
    STAIRS
    STAKING
    STALELY
    STALK
    STALL
    STAMINA
    STAMPER
    STAND
    STANDUP
    STANGED
    STANKS
    STANZA
    STAPLE
    STARCHY
    STARERS
    STARKER
    STARRY
    STARTLE
    STARVED
    STASHED
    STATANT
    STATERS
    STATIN
    STATIST
    STATUE
    STATUSY
    STAVES
    STAYING
    STEADY
    STEALS
    STEAMS
    STEEDS
    STEELED
    STEEPED
    STEEPS
    STEEVE
    STELA
    STELENE
    STELLAS
    STEMMY
    STENCIL
    STENT
    STEPPER
    STEREO
    STERLET
    STERNLY
    STEROLS
    STEWARD
    STEWS
    STIBINE
    STICK
    STICKS
    STIES
    STIFFIE
    STIFLER
    STILE
    STILLS
    STIME
    STIMY
    STINGS
    STINKS
    STINTS
    STIPEND
    STIRKS
    STIRRER
    STIVER
    STOAT
    STOCKED
    STODGED
    STOGIE
    STOICS
    STOKES
    STOLES
    STOMA
    STOMATE
    STONE
    STONEY
    STONY
    STOOK
    STOOLED
    STOOPER
    STOPERS
    STOPPED
    STORAGE
    STORERS
    STORIES
    STORMED
    STOTIN
    STOTTS
    STOUR
    STOURY
    STOUTS
    STOWAGE
    STOWS
    STRAIN
    STRAKED
    STRANGE
    STRATA
    STRATI
    STRAWS
    STRAYS
    STREAMS
    STREELS
    STRESS
    STRETTO
    STREWS
    STRICK
    STRIDES
    STRIKE
    STRINGY
    STRIPES
    STRIVED
    STROBES
    STROKED
    STROMA
    STROPHE
    STROVE
    STROY
    STRUDEL
    STRUMS
    STRUTS
    STUBS
    STUDDIE
    STUDIO
    STUFF
    STUIVER
    STUMP
    STUMS
    STUNS
    STUPAS
    STUPIDS
    STURTS
    STYING
    STYLER
    STYLI
    STYLITE
    STYMIED
    STYRAX
    SUASIVE
    SUAVEST
    SUBAHS
    SUBATOM
    SUBCELL
    SUBDEAN
    SUBDUCT
    SUBECHO
    SUBERS
    SUBGUM
    SUBITO
    SUBLETS
    SUBMENU
    SUBNETS
    SUBPAR
    SUBRENT
    SUBSECT
    SUBSIDY
    SUBTASK
    SUBTEXT
    SUBTONE
    SUBVENE
    SUBZONE
    SUCCOR
    SUCCUBA
    SUCKER
    SUCKLED
    SUCRASE
    SUDARIA
    SUDOR
    SUDSERS
    SUEDE
    SUETS
    SUFFICE
    SUGARER
    SUGHING
    SUINTS
    SUITES
    SUKKAH
    SULCATE
    SULFA
    SULFIDS
    SULFURS
    SULKIER
    SULKY
    SULLY
    SULTAN
    SUMAC
    SUMMA
    SUMMATE
    SUMMING
    SUMOIST
    SUNBATH
    SUNBOWS
    SUNDER
    SUNDOG
    SUNFISH
    SUNLAMP
    SUNNA
    SUNNIER
    SUNRAY
    SUNSET
    SUNTANS
    SUPER
    SUPINE
    SUPPING
    SUPPLY
    SUPREMO
    SURBASE
    SUREST
    SURFER
    SURFMEN
    SURGEON
    SURGING
    SURLILY
    SURPLUS
    SURREYS
    SURVEYS
    SUSLIKS
    SUSSES
    SUTRA
    SUTTEES
    SVARAJ
    SWABBIE
    SWAGE
    SWAGGED
    SWAGMEN
    SWAINS
    SWAMIES
    SWAMPS
    SWANKED
    SWANNY
    SWAPS
    SWARE
    SWARMER
    SWARTHY
    SWASHES
    SWATHER
    SWATTER
    SWAYING
    SWEAT
    SWEDE
    SWEEPER
    SWEETEN
    SWELL
    SWELTRY
    SWERVES
    SWIFTER
    SWIGS
    SWIMMER
    SWING
    SWINGES
    SWINK
    SWIPED
    SWIPPLE
    SWISH
    SWISS
    SWITHER
    SWIVELS
    SWIZZLE
    SWOON
    SWOOP
    SWOOSH
    SWORE
    SWOUN
    SWUNG
    SYCONIA
    SYLIS
    SYLPHS
    SYLVANS
    SYLVITE
    SYMPTOM
    SYNCED
    SYNCING
    SYNDET
    SYNESIS
    SYNODAL
    SYNTAGM
    SYNURA
    SYPHONS
    SYRINGA
    SYRUPED
    SYSTEM
    TABANID
    TABBIED
    TABER
    TABID
    TABLED
    TABLOID
    TABORED
    TABOULI
    TABULAR
    TABUS
    TACHISM
    TACITLY
    TACKETS
    TACKING
    TACKS
    TACTFUL
    TACTS
    TAENIAE
    TAFFIES
    TAGGED
    TAGLINE
    TAHINIS
    TAIGAS
    TAILFIN
    TAILORS
    TAINTS
    TAKAHE
    TAKEOUT
    TAKEUPS
    TALAR
    TALCING
    TALCS
    TALER
    TALIPED
    TALKERS
    TALKS
    TALLEST
    TALLISH
    TALLOLS
    TALLY
    TALOOKA
    TALUS
    TAMALES
    TAMARI
    TAMBACS
    TAMBUR
    TAMEINS
    TAMEST
    TAMMIES
    TAMPED
    TAMPON
    TANDEM
    TANGELO
    TANGLED
    TANGOED
    TANIST
    TANKAS
    TANKING
    TANNED
    TANNIC
    TANNOY
    TANSY
    TANTRAS
    TANYARD
    TAPER
    TAPETA
    TAPIOCA
    TAPPED
    TAPPING
    TARAMAS
    TARDIVE
    TARES
    TARIFF
    TARNAL
    TAROK
    TARPAN
    TARRE
    TARRIES
    TARSI
    TARTAN
    TARTARS
    TARTILY
    TARTS
    TARZANS
    TASSE
    TASSETS
    TASTER
    TASTING
    TATARS
    TATSOI
    TATTIE
    TATTLE
    TATTOOS
    TAUNTER
    TAUPES
    TAUTENS
    TAUTOG
    TAVERNS
    TAWIE
    TAWNIES
    TAWSE
    TAXABLY
    TAXER
    TAXIES
    TAXIS
    TAXLESS
    TAXON
    TAXYING
    TEABOX
    TEACHES
    TEALS
    TEAPOTS
    TEARERS
    TEARING
    TEASED
    TEASES
    TEATS
    TEAZLED
    TECHIES
    TECHS
    TECTRIX
    TEDDERS
    TEDIUM
    TEEMER
    TEENER
    TEENSY
    TEETER
    TEETHER
    TEGGS
    TEGULAR
    TEINDS
    TELAMON
    TELEDUS
    TELEMEN
    TELESIS
    TELFERS
    TELIUM
    TELLS
    TELOI
    TELPHER
    TEMPEH
    TEMPEST
    TEMPLED
    TEMPS
    TEMPURA
    TENAIL
    TENCH
    TENDING
    TENDU
    TENGE
    TENNERS
    TENONED
    TENOUR
    TENRECS
    TENSES
    TENSITY
    TENTED
    TENTHS
    TENTY
    TENURE
    TENUTOS
    TEPAS
    TEPHRAS
    TEQUILA
    TERBIA
    TERCEL
    TEREBIC
    TERGA
    TERMER
    TERMLY
    TERNATE
    TERPENE
    TERRANE
    TERRETS
    TERRIT
    TERSE
    TERTIAN
    TESTACY
    TESTEES
    TESTIFY
    TESTONS
    TETANAL
    TETCHY
    TETRA
    TETRIS
    TETTERS
    TEWING
    TEXTUAL
    THAIRM
    THALLI
    THANE
    THANKS
    THAWED
    THEATER
    THECAE
    THEFT
    THEIN
    THEIRS
    THEME
    THENAL
    THEOLOG
    THERE
    THEREON
    THERM
    THERMES
    THEROID
    THESPS
    THEWIER
    THIAZOL
    THICKLY
    THIEVES
    THILLS
    THINK
    THINNER
    THIONIC
    THIRD
    THIRLS
    THISTLE
    THOLES
    THONGED
    THORIC
    THORNS
    THORP
    THOUED
    THRALL
    THRAW
    THREADS
    THREATS
    THRESH
    THRIFTY
    THRIVE
    THROAT
    THROE
    THRONES
    THROW
    THRUMMY
    THRUSTS
    THUGS
    THULIUM
    THUMPED
    THUNKED
    THUYA
    THWARTS
    THYMIC
    THYMUS
    THYRSI
    TIARAS
    TICAL
    TICKER
    TICKLE
    TICTAC
    TIDALLY
    TIDED
    TIDIER
    TIDING
    TIELESS
    TIERCEL
    TIFFANY
    TIFFS
    TIGHTER
    TIGON
    TIKIS
    TILAPIA
    TILER
    TILLAGE
    TILLITE
    TILTH
    TIMBAL
    TIMBERY
    TIMED
    TIMERS
    TIMING
    TIMPANI
    TINCT
    TINDERY
    TINEID
    TINFULS
    TINGLE
    TINGS
    TINING
    TINKLER
    TINMEN
    TINNILY
    TINSELS
    TINTS
    TIPCAT
    TIPOFFS
    TIPPETS
    TIPPLER
    TIPSTER
    TIPTOP
    TIREDER
    TIRLING
    TISSUAL
    TITAN
    TITBITS
    TITHE
    TITHING
    TITLE
    TITMAN
    TITRE
    TITTIES
    TITTY
    TMESIS
    TOADY
    TOASTY
    TOCHER
    TODAYS
    TODDLES
    TOECAPS
    TOENAIL
    TOFFS
    TOGAE
    TOGGED
    TOGGLER
    TOILED
    TOILETS
    TOITING
    TOKED
    TOKERS
    TOLANE
    TOLAS
    TOLIDIN
    TOLLER
    TOLLS
    TOLUID
    TOLUOLS
    TOLYLS
    TOMBACK
    TOMBED
    TOMBOYS
    TOMCODS
    TOMMIES
    TOMTITS
    TONDOS
    TONEMIC
    TONETTE
    TONGER
    TONGS
    TONICS
    TONISH
    TONNEAU
    TONSIL
    TONUSES
    TOOLERS
    TOONS
    TOOTHED
    TOOTLED
    TOOTSIE
    TOPED
    TOPES
    TOPHI
    TOPICAL
    TOPKNOT
    TOPOI
    TOPPERS
    TOPSAIL
    TOQUE
    TORAHS
    TORCHON
    TORES
    TORMENT
    TOROSE
    TORPID
    TORQUED
    TORRID
    TORSES
    TORSO
    TORTEN
    TORTS
    TORUS
    TOSSES
    TOSTADA
    TOTALLY
    TOTEMS
    TOTING
    TOTTING
    TOUCHED
    TOUGH
    TOUGHLY
    TOURACO
    TOURISM
    TOUSED
    TOUSLES
    TOUTS
    TOWAGE
    TOWBOAT
    TOWER
    TOWHEE
    TOWLINE
    TOWNIE
    TOWNY
    TOXEMIC
    TOXINE
    TOYED
    TOYLESS
    TOYSHOP
    TRACERY
    TRACK
    TRACTOR
    TRADERS
    TRAGEDY
    TRAIK
    TRAILER
    TRAINER
    TRAITS
    TRAMELS
    TRAMPER
    TRAMWAY
    TRANGAM
    TRANQS
    TRAPANS
    TRAPS
    TRASHES
    TRAUMAS
    TRAVES
    TRAWLEY
    TREACLY
    TREADS
    TREATS
    TREBLY
    TREENS
    TREHALA
    TREMBLE
    TRENAIL
    TRENDY
    TRESS
    TRESTLE
    TREYS
    TRIAD
    TRIAGES
    TRIBAL
    TRIBUTE
    TRICES
    TRICKIE
    TRICKY
    TRIDENT
    TRIENS
    TRIFLE
    TRIFORM
    TRIGON
    TRIJET
    TRILITH
    TRILOGY
    TRIMMER
    TRINE
    TRINKET
    TRIOLS
    TRIPACK
    TRIPLED
    TRIPOD
    TRIPPED
    TRIPTAN
    TRISMIC
    TRITE
    TRITOMA
    TRIUNE
    TRIVIAL
    TROCAR
    TROCHEE
    TROCKS
    TROGONS
    TROIS
    TROLAND
    TROLLOP
    TROMPE
    TRONAS
    TROOPER
    TROPHIC
    TROPINE
    TROTHS
    TROTYLS
    TROUPE
    TROUT
    TROVERS
    TROWING
    TRUANCY
    TRUCES
    TRUCKLE
    TRUDGER
    TRUES
    TRUGS
    TRULLS
    TRUMPET
    TRUNKS
    TRUSSES
    TRUSTOR
    TRYING
    TRYPSIN
    TRYSTED
    TSADE
    TSARINA
    TSETSE
    TSKTSK
    TSOURIS
    TUATERA
    TUBATE
    TUBBING
    TUBES
    TUBINGS
    TUBULE
    TUCKED
    TUCKING
    TUFFS
    TUFTIER
    TUGBOAT
    TUGHRIK
    TUILLES
    TULIP
    TUMBLED
    TUMEFY
    TUMMLER
    TUMOUR
    TUMULAR
    TUNABLE
    TUNDRAS
    TUNES
    TUNICA
    TUNNAGE
    TUNNING
    TUPIKS
    TURACO
    TURBARY
    TURBITH
    TURBOTS
    TURFED
    TURFS
    TURGITE
    TURISTA
    TURMOIL
    TURNING
    TURNON
    TURNUPS
    TURTLE
    TUSCHE
    TUSHIE
    TUSKER
    TUSSAHS
    TUSSEHS
    TUSSIVE
    TUSSOR
    TUSSURS
    TUTORED
    TUTTI
    TUTUED
    TUYER
    TWAES
    TWANGER
    TWASOME
    TWEAKS
    TWEEDY
    TWEET
    TWEEZED
    TWELVES
    TWIBILL
    TWIER
    TWIGS
    TWINE
    TWINGE
    TWINJET
    TWINS
    TWIRLER
    TWIST
    TWITCH
    TWIXT
    TWOSOME
    TYEES
    TYLOSIN
    TYMPANI
    TYNES
    TYPED
    TYPHON
    TYPHUS
    TYPIFY
    TYPPS
    TYRES
    TYTHED
    TZARINA
    TZETZES
    TZURIS
    UDDER
    UGLIES
    UHLAN
    UKULELE
    ULCERED
    ULLAGE
    ULNAR
    ULSTERS
    ULTRAS
    UMAMIS
    UMBERED
    UMBONIC
    UMBRAL
    UMIACS
    UMLAUT
    UMPIRED
    UNADDED
    UNAGING
    UNAKIN
    UNARM
    UNAUS
    UNBAKED
    UNBANS
    UNBEAR
    UNBEND
    UNBINDS
    UNBONED
    UNBOX
    UNBRAKE
    UNBULKY
    UNCAGES
    UNCAP
    UNCAST
    UNCHIC
    UNCIALS
    UNCLAD
    UNCLEAR
    UNCLOAK
    UNCOCK
    UNCOMIC
    UNCOUTH
    UNCROSS
    UNCURB
    UNCUS
    UNDEE
    UNDIES
    UNDOER
    UNDRAPE
    UNDREST
    UNDULAR
    UNEARTH
    UNENDED
    UNFAITH
    UNFELT
    UNFITS
    UNFOLD
    UNFREED
    UNFURL
    UNGIRD
    UNGLUED
    UNGUARD
    UNGULAE
    UNHANDS
    UNHASTY
    UNHELMS
    UNHITCH
    UNHOOKS
    UNHUNG
    UNICORN
    UNIFIER
    UNIONS
    UNIQUES
    UNITAGE
    UNITER
    UNITIVE
    UNJAM
    UNKEND
    UNKINKS
    UNKNOWN
    UNLADED
    UNLATCH
    UNLEARN
    UNLEVEL
    UNLINKS
    UNLOAD
    UNLOOSE
    UNMAKE
    UNMANS
    UNMEET
    UNMEWED
    UNMIX
    UNMOLDS
    UNMOWN
    UNNOISY
    UNPACK
    UNPEG
    UNPICK
    UNPIN
    UNPOSED
    UNRATED
    UNREAL
    UNREST
    UNRIP
    UNROBE
    UNROOF
    UNROUGH
    UNRULY
    UNSAWED
    UNSEAL
    UNSEATS
    UNSET
    UNSEWS
    UNSHARP
    UNSHIPS
    UNSIGHT
    UNSMART
    UNSNARL
    UNSONSY
    UNSPENT
    UNSPUN
    UNSTEPS
    UNSTUCK
    UNSWEAR
    UNTACKS
    UNTEACH
    UNTIES
    UNTORN
    UNTRIMS
    UNTRUSS
    UNTUNED
    UNURGED
    UNVEXED
    UNWAXED
    UNWEPT
    UNWISE
    UNWON
    UNWOVEN
    UNYOKED
    UNZONED
    UPBEATS
    UPBORE
    UPBRAID
    UPCASTS
    UPCOILS
    UPDART
    UPDATES
    UPDOVE
    UPEND
    UPFLOW
    UPFRONT
    UPGIRDS
    UPGROW
    UPHEAVE
    UPHOLD
    UPKEEP
    UPLEAPS
    UPLINK
    UPMOST
    UPPILED
    UPPITY
    UPRATED
    UPRIGHT
    UPRIVER
    UPROSE
    UPSENDS
    UPSHOOT
    UPSILON
    UPSOAR
    UPSTARE
    UPSTIR
    UPSWELL
    UPTAKES
    UPTEMPO
    UPTIGHT
    UPTORE
    UPTREND
    UPWARD
    UPWINDS
    URAEMIC
    URANIC
    URANOUS
    URARI
    URATES
    URBIA
    UREAS
    UREDIUM
    UREIDES
    URETERS
    URGENCY
    URGING
    URINALS
    URINOSE
    UROLOGY
    URSAE
    URTEXTS
    USAGES
    USEABLY
    USHERED
    USQUE
    USURER
    USURPER
    UTERINE
    UTILIZE
    UTOPIAS
    UTTERED
    UVEAS
    UVULAE
    VACANCY
    VACCINA
    VACUOUS
    VAGALLY
    VAGINAL
    VAGUELY
    VAHINES
    VAINEST
    VAKIL
    VALERIC
    VALGOID
    VALINE
    VALKYRS
    VALOR
    VALSES
    VALUERS
    VALVAL
    VALVES
    VAMOSE
    VAMPERS
    VAMPS
    VANDALS
    VANGS
    VANMAN
    VANNING
    VAPIDLY
    VAPORY
    VARAS
    VARICES
    VARIETY
    VARLET
    VARNAS
    VARUS
    VARYING
    VASSALS
    VASTLY
    VATIC
    VAULT
    VAUNT
    VAUNTY
    VEALED
    VEALS
    VEDETTE
    VEEPEE
    VEERING
    VEGES
    VEGGIES
    VEILED
    VEINAL
    VEINING
    VELAMEN
    VELCRO
    VELIGER
    VELOUR
    VELURED
    VENAE
    VENDED
    VENDING
    VENDUES
    VENERY
    VENIAL
    VENIRE
    VENOMER
    VENTAIL
    VENTRAL
    VENUES
    VENUSES
    VERBID
    VERBS
    VERDURE
    VERGES
    VERIEST
    VERISMS
    VERITES
    VERMIN
    VERNIX
    VERSED
    VERSETS
    VERSO
    VERSTS
    VERTU
    VERVET
    VESICLE
    VESPINE
    VESTALS
    VESTIGE
    VESTURE
    VETOED
    VETTED
    VEXEDLY
    VEXILLA
    VIADUCT
    VIAND
    VIATORS
    VIBRATE
    VICAR
    VICES
    VICIOUS
    VICTORS
    VICUNAS
    VIDUITY
    VIEWIER
    VIGIA
    VIGORS
    VILAYET
    VILLA
    VILLEIN
    VILLUS
    VINALS
    VINCULA
    VINES
    VINING
    VINYL
    VIOLATE
    VIOLINS
    VIPERS
    VIRELAI
    VIREOS
    VIRGIN
    VIRION
    VIROSES
    VIRTUES
    VISAGE
    VISARDS
    VISCOSE
    VISEING
    VISION
    VISITOR
    VISORS
    VISUALS
    VITAMER
    VITRIC
    VITTA
    VITTLES
    VIVAS
    VIVIFIC
    VIZARD
    VIZIRS
    VIZSLAS
    VOCAL
    VOCODER
    VODOUNS
    VOGUE
    VOGUING
    VOICERS
    VOIDERS
    VOILES
    VOLED
    VOLLEYS
    VOLTAIC
    VOLUBLE
    VOLUTE
    VOLVAS
    VOMERS
    VOMITER
    VOODOO
    VOTARY
    VOTING
    VOUCHED
    VOUDONS
    VOWELS
    VOYAGE
    VOYEURS
    VROUWS
    VUGHS
    VULGUS
    VULVAL
    VYINGLY
    WABBLY
    WACKIER
    WACKY
    WADDIE
    WADDLED
    WADED
    WADING
    WADMEL
    WADSET
    WAFER
    WAFFIE
    WAFFLER
    WAFTED
    WAFTURE
    WAGERS
    WAGGERY
    WAGGLES
    WAGON
    WAGTAIL
    WAIFED
    WAILER
    WAINS
    WAISTED
    WAITERS
    WAIVED
    WAKAME
    WAKEN
    WAKERS
    WALED
    WALING
    WALKOUT
    WALLA
    WALLED
    WALLIES
    WALLOWS
    WALRUS
    WAMBLE
    WAMEFUL
    WAMPUMS
    WANDERS
    WANEY
    WANGLER
    WANIEST
    WANKED
    WANLY
    WANNEST
    WANTERS
    WAPITI
    WARBLED
    WARDENS
    WARED
    WARIEST
    WARKING
    WARLORD
    WARMING
    WARMTHS
    WARNERS
    WARPED
    WARRANT
    WARRIOR
    WARSLED
    WARTHOG
    WARWORK
    WASHED
    WASHING
    WASHUPS
    WASPS
    WASTED
    WASTING
    WATAP
    WATCHED
    WATERER
    WATTER
    WATTS
    WAUGHTS
    WAULING
    WAVER
    WAVES
    WAVIES
    WAWLING
    WAXEN
    WAXIEST
    WAXWEED
    WAYLAID
    WAYWARD
    WEAKENS
    WEAKON
    WEALTH
    WEANERS
    WEARER
    WEARILY
    WEASAND
    WEASONS
    WEAVERS
    WEBBIER
    WEBCAST
    WEBFOOT
    WEBPAGE
    WECHT
    WEDDING
    WEDELS
    WEDGIER
    WEEDED
    WEEDING
    WEEKLY
    WEENIES
    WEEPER
    WEEPING
    WEETING
    WEEVILS
    WEFTS
    WEIGHS
    WEINERS
    WEIRDLY
    WEIRS
    WELCHES
    WELDING
    WELKIN
    WELLING
    WELSHER
    WELTING
    WENCHES
    WENNIER
    WERGILD
    WESTER
    WETBACK
    WETNESS
    WETTEST
    WHACKED
    WHACKY
    WHALES
    WHAMO
    WHANGS
    WHARFED
    WHATS
    WHEAL
    WHEEDLE
    WHEELS
    WHEEPLE
    WHEEZES
    WHELM
    WHELPS
    WHEREAS
    WHEREON
    WHERVES
    WHEWS
    WHICKER
    WHIFF
    WHIFFS
    WHILING
    WHIMSEY
    WHINERS
    WHINGER
    WHINS
    WHIPPY
    WHIRL
    WHIRR
    WHISH
    WHISK
    WHISKY
    WHISTS
    WHITENS
    WHITEYS
    WHITISH
    WHITY
    WHIZZY
    WHOLLY
    WHOOF
    WHOOPEE
    WHOOSH
    WHORE
    WHORL
    WHORTS
    WHUMPED
    WHYDAHS
    WICHES
    WICKET
    WICKYUP
    WIDDIES
    WIDELY
    WIDEOUT
    WIDGET
    WIDOWER
    WIELDED
    WIENERS
    WIFELY
    WIFTIER
    WIGEONS
    WIGGLE
    WIGGY
    WIGLETS
    WIGWAMS
    WILDED
    WILDISH
    WILFUL
    WILLED
    WILLFUL
    WILLOW
    WILTED
    WIMBLES
    WIMPISH
    WIMPY
    WINCES
    WINCHER
    WINDED
    WINDILY
    WINDOW
    WINDUP
    WINERY
    WINGBOW
    WINGING
    WINGTIP
    WINISH
    WINKLE
    WINNED
    WINNOW
    WINTER
    WINTLES
    WIPEOUT
    WIRABLE
    WIRERS
    WIRIEST
    WISDOM
    WISELY
    WISEST
    WISHES
    WISPIER
    WISPY
    WISTFUL
    WITCH
    WITES
    WITHERS
    WITHING
    WITLESS
    WITNEYS
    WITTOL
    WIVERN
    WIZARD
    WIZES
    WOADS
    WOBBLED
    WODGES
    WOFULLY
    WOLFER
    WOLFS
    WOMANED
    WOMBED
    WOMERA
    WONDERS
    WONNER
    WONTON
    WOODCUT
    WOODIER
    WOODMEN
    WOODY
    WOOFER
    WOOLED
    WOOLHAT
    WOOLLEN
    WOOLY
    WOORALI
    WOOZIER
    WORDIER
    WORKBAG
    WORKERS
    WORKS
    WORLDS
    WORMIL
    WORMY
    WORRITS
    WORSER
    WORST
    WORTHS
    WOULD
    WOVEN
    WOWSERS
    WRAITHS
    WRAPPER
    WRASSLE
    WRATHY
    WREATH
    WRECKED
    WREST
    WRETCH
    WRIER
    WRIGHT
    WRINGS
    WRISTY
    WRITHE
    WRITING
    WRONGER
    WROUGHT
    WRYLY
    WURZEL
    WUSSIES
    WYLED
    WYTED
    XANTHAN
    XENIA
    XENONS
    XEROSIS
    XERUS
    XYLEM
    XYLITOL
    XYLOSES
    XYSTI
    YABBER
    YACHT
    YACKING
    YAGER
    YAIRD
    YAKKING
    YAMMER
    YANGS
    YANQUIS
    YAPOK
    YAPPER
    YARDED
    YARDMEN
    YARNED
    YARROW
    YASMAKS
    YAULD
    YAUPON
    YAWED
    YAWLS
    YAWNS
    YAWPS
    YEALING
    YEARLY
    YEARS
    YECCH
    YEELINS
    YELLED
    YELLOWS
    YELPERS
    YENTA
    YEOMEN
    YERKS
    YESSING
    YEUKED
    YIELDED
    YINCE
    YIPPIES
    YIRRS
    YOBBOES
    YODEL
    YODLE
    YODLING
    YOGHURT
    YOGINS
    YOICKS
    YOKING
    YOMIM
    YONKERS
    YOUNKER
    YOUSE
    YOWES
    YOWLER
    YTTRIA
    YUCAS
    YUCKIER
    YUKKED
    YULANS
    YUPON
    YUPPY
    ZADDICK
    ZAFFERS
    ZAFTIG
    ZAIRE
    ZAMIAS
    ZANIER
    ZANZA
    ZAPPERS
    ZAPTIEH
    ZARIBA
    ZAZEN
    ZEALS
    ZEBECKS
    ZEBRAS
    ZECCHIN
    ZELKOVA
    ZENANAS
    ZEPHYRS
    ZEROES
    ZESTER
    ZESTING
    ZEUGMAS
    ZIGGED
    ZILCH
    ZILLS
    ZINCING
    ZINCOUS
    ZINES
    ZINGARI
    ZINGIER
    ZINKY
    ZIPPED
    ZIPPY
    ZITHER
    ZIZITH
    ZLOTIES
    ZOARIAL
    ZODIACS
    ZOECIUM
    ZOMBIES
    ZONALLY
    ZONER
    ZONKING
    ZONULAS
    ZOOGENY
    ZOOIER
    ZOOMING
    ZOONS
    ZORILLA
    ZOSTER
    ZOUNDS
    ZYDECO
    ZYGOSE
    ZYGOTIC
    ZYMOSAN
    ZYZZYVA
    
.. _session_10:

Tuesday In-class Exercises
--------------------------

Call greet so that it prints out::
 
    Hello Jackie
    Hello Nick

.. tabbed:: q1

    .. tab:: Question

        .. actex:: session_10_1
        
            def greet(x, y = ["Jackie", "Nick"], z = 1):
                for nm in y:
                    for i in range(z):
                        print (x + " " + nm)

    .. tab:: Answer
        
        .. actex:: session_10_1a

            def greet(x, y = ["Jackie", "Nick"], z = 1):
                for nm in y:
                    for i in range(z):
                        print (x + " " + nm)

            greet("Hello")
            
Call greet so that it prints out::
 
    Hello Prof. Resnick
    Hello Prof. Resnick
    Hello Prof. Resnick

.. tabbed:: q2

    .. tab:: Question
    
        .. actex:: session_10_2
    
            def greet(x, y = ["Jackie", "Nick"], z = 1):
                for nm in y:
                    for i in range(z):
                        print (x + " " + nm)

    .. tab:: Answer
    
        .. actex:: session_10_2a

            def greet(x, y = ["Jackie", "Nick"], z = 1):
                for nm in y:
                    for i in range(z):
                        print (x + " " + nm)

            greet("Hello", ["Prof. Resnick"], 3)

Define the function `t` so that it multiples its two arguments, but has default
values such that it produces the outputs specified

.. tabbed:: q3

    .. tab:: Question
    
        .. actex:: session_10_3
         
            t()
            #prints 1
            
            t(2)
            #prints 2
            
            t(2, 3)
            #prints 6

    .. tab:: Answer
    
        .. actex:: session_10_3a

            def t(x=1, y=1):
                return x*y
                
            print t()
            #prints 1
            
            print t(2)
            #prints 2
            
            print t(2, 3)
            #prints 6

                
Expand the definition of the function print_d so that it produces the following
outputs::

    #alphabetic order
    Jackie, 100
    Lara, 150
    Nick, 42
    
    # reverse order
    Nick, 42
    Lara, 150
    Jackie, 100
    
    # sorted by values
    Nick, 42
    Jackie, 100
    Lara, 150

.. tabbed:: q4

    .. tab:: Question
    
        .. actex:: session_10_4
        
            # change the definition of print_d
            def print_d(d):
                pairs = d.items()
                for (k, v) in pairs:
                    print(k + ", " + str(v))
            
            d = {"Nick" : 42, "Jackie": 100, "Lara": 150}        
        
            #alhabetic order
            print_d(d)
            
            # reverse order
            print_d(d, True)
            
            # sorted by values
            print_d(d, False, True)
        
    .. tab:: Answer
        
        .. actex:: session_10_4a
        
            # change the definition of print_d
            def print_d(d, reverse=False, by_value=False):
                pairs = d.items()
                if by_value:
                    if reverse:
                        s = sorted(pairs, None, lambda x: x[1], True)
                    else:
                        s = sorted(pairs, None, lambda x: x[1])
                    # we should have just been able to pass reverse as the
                    # fourth parameter to sorted, but there seems to be a 
                    # bug that when we pass False it still sorts in reverse
                    # order
                else:
                    if reverse:
                        s = sorted(pairs, None, lambda x: x[0], True)
                    else:
                        s = sorted(pairs, None, lambda x: x[0])
                
                for (k, v) in s:
                    print(k + ", " + str(v))
                
            d = {"Nick" : 42, "Jackie": 100, "Lara": 150}
        
            #alhabetic order
            print_d(d)
            
            # reverse order
            print_d(d, True)
            
            # sorted by values
            print_d(d, False, True)
            


Define a function filtered_count that takes a list as its first parameter and
a function as its second parameter. The function passed as the second value should be a boolean function that
takes a single parameter and returns True or False.

.. tabbed:: q5

    .. tab:: Question
    
        .. actex:: session_10_5
    
            def filtered_count(...
    

    .. tab:: Answer
    
        .. actex:: session_10_5a

            def filtered_count(L, f):
                
                count = 0
                
                for x in L:
                    if f(x):
                        count = count + 1 
                
                return count


            print(filtered_count([4, 2, 0, 5, 6, 5], lambda x: x > 3))
            # Should return 4, the count of items in the list that are bigger than 3
    
    
.. _session_11:

Thursday In-class Exercises
---------------------------

If you had trouble with the exercise at the bottom of the sorting chapter, I've broken
it up into several steps here. 

Step 1. Suppose you had this list, [8, 7, 6, 6, 4, 4, 3, 1, 0], already sorted, how would you make a list of just the best 5? (Hint: take a slice).

.. tabbed:: q6

    .. tab:: Question
   

        .. actex:: session_11_1
            
            L = [8, 7, 6, 6, 4, 4, 3, 1, 0]
    
    .. tab:: Answer
    
        .. actex:: session_11_1a
        
             L = [8, 7, 6, 6, 4, 4, 3, 1, 0]
             L[:5]
            

Now suppose the list wasn't sorted yet. How would get those same five elements from this list?

.. tabbed:: q7

    .. tab:: Question

        .. actex:: session_11_2

            L = [0, 1, 6, 7, 3, 6, 8, 4, 4]
            
    .. tab:: Answer
 
         .. actex:: session_11_2a

            L = [0, 1, 6, 7, 3, 6, 8, 4, 4]
            L2 = sorted(L, None, None, True)
            L2[:5]
    
        
    
Now make a dictionary of counts for how often these numbers appear in the lists.

.. tabbed:: q8

    .. tab:: Question

        .. actex:: session_11_3
    
            L = [0, 1, 6, 7, 3, 6, 8, 4, 4, 6, 1, 6, 6, 5, 4, 4, 3, 35, 4, 11]
        

    .. tab:: Answer
    
        .. actex:: session_11_3a

            L = [0, 1, 6, 7, 3, 6, 8, 4, 4, 6, 1, 6, 6, 5, 4, 4, 3, 35, 4, 11]
            d = {}
            for x in L:
                if x in d:
                    d[x] = d[x] + 1
                else:
                    d[x] = 1
            
            
Now sort the (number, count) pairs and keep just the top five pairs. Review
:ref:`Sorting a Dictionary <sort_dictionaries>` if you're not sure how to do this.

.. tabbed:: q9

    .. tab:: Question
    
        .. actex:: session_11_4

            L = [0, 1, 6, 7, 3, 6, 8, 4, 4, 6, 1, 6, 6, 5, 4, 4, 3, 35, 4, 11]
    
    .. tab:: Answer
    
        .. actex:: session_11_4a
        
            L = [0, 1, 6, 7, 3, 6, 8, 4, 4, 6, 1, 6, 6, 5, 4, 4, 3, 35, 4, 11]
        
            d = {}
            for x in L:
                if x in d:
                    d[x] = d[x] + 1
                else:
                    d[x] = 1

            s = sorted(d.items(), None, lambda x: x[1], True)
            
            print(s[:5])
            

Finally, generalize what you've done. Write a function that takes a string as a parameter and returns a list of the five
most frequent characters in the string. If you're amibitious write a few test cases for it, using import test and then test.testEqual.

.. tabbed:: q10

    .. tab:: Question

        .. actex:: session_11_5

    .. tab:: Answer
    
        .. actex:: session_11_5a
        
            def five_most_frequent(s):
                d = {}
                for x in s:
                    if x in d:
                        d[x] = d[x] + 1
                    else:
                        d[x] = 1
                
                s = sorted(d.items(), None, lambda x: x[1], True)
                res = []
                for (k, v) in s[:5]:
                    res.append(k)
                return res
                
            import test
            test.testEqual(five_most_frequent("aaaaaabbbbbccccdefggghijkk"), ['a', 'b', 'c', 'g', 'k'])                
             
.. _functions_review_5:

Functions Review
----------------

These are review problems that we worked on and discussed in section this week. Each problem asks you to define a function, specifies the input that the function takes, and what the function should do.

The problems AND the solutions are provided for you, since you worked on them in class. (Problems and questions you addressed in discussion may vary slightly by section!) We suggest that you try to do the problems again yourself before looking at the solutions (which are heavily commented to address questions that came up in the discussion group work).

1. Define (and call) a function called `` get_vowels `` which takes an **input** of a string and **returns the total number of vowels in the string**.

    .. tabbed:: func_review_1

        .. tab:: Problem

            .. actex:: fr_1

                # Write your code here!


                # Here's a sample function call.
                print get_vowels("Hello all") # This should print: 3

        .. tab:: Solution

            .. actex:: fr_1a

                def get_vowels(s):
                    vowels = "aeiou"
                    total = 0
                    for v in vowels:
                        total += s.count(v)
                    return total

                print get_vowels("Hello all")

#. Define (and call) a function called `` sum_a_list `` which **takes any list of integers** and **returns the sum of all integers in the list**.

    .. tabbed:: func_review_2

        .. tab:: Problem

            .. actex:: fr_2

                # Write your code here!


                # Here's a sample function call.
                print sum_a_list([1,4,7,5]) # this should print: 17

                # Extra practice: 
                # how would you change this function just a LITTLE 
                # so that the function could also take a string of digits
                # and return the sum of all those digits.
                # (Hint: to do this, you only have to type 5 more characters.)

        .. tab:: Solution

            .. actex:: fr_2a

                def sum_a_list(lt):
                    tot = 0
                    for i in lt:
                        tot = tot + i
                    return tot

                print sum_a_list(1,4,7,5])

                # Here's the version of the function that will work
                #   for EITHER a list of integers or a string of digits
                def sum_a_list_or_digitstring(lt):
                    tot = 0
                    for i in lt:
                        tot = tot + int(i)
                    return tot

                print sum_a_list_or_digitstring("1475")


#. Define (and call!) a function called ``common_word`` that **takes a string** and **prints a tuple** of **the most commonly used word in the string** and **the number of times that word is used**. (If there's more than one word that's used most frequently, the function should **print** all of those words.) 

    .. tabbed:: func_review_3

        .. tab:: Problem

            .. actex:: fr_3

                # Write your code here!


                # Here's a sample function call.
                common_word("hello hello hello is what they said to the class!") # should print: hello


                # For extra practice: you've done something like this before -- 
                # how would you change this function to print the LONGEST word in the string?



        .. tab:: Solution

            .. actex:: fr_3a

                def common_word(s):
                    d = {}
                    sp = s.split() # split my string by whitespace, so into 'words'
                    for w in sp:
                        if w in d:
                            d[w] = d[w] + 1
                        else:
                            d[w] = 1
                    kys = d.keys() # get all the keys from the dict you built, in a list
                    most_common = kys[0] # start at the beginning of the list -- this is the most common so far!
                    for k in d: # go through the keys in the dictionary
                        if d[k] > d[most_common]: # if the value of the key is bigger than the value of the most common key SO FAR, then you have a new most common key so far
                            most_common = k # so reassign the most_common key
                    for ky in d: # now that we know the value of the most common key, go through the keys of the dictionary again
                        if d[ky] == d[most_common]: # for every key that has the same value as the most common one
                            print ky, d[ky] # print the key and its value
                            # note that we do NOT return anything here!
                            # because we asked to print stuff out

                # Think further: what would happen if you put a return statement where that print statement is? why wouldn't that work?


#. Define (and call!) a function called ``smallest_value_name`` that **takes a dictionary** with key-value pairs of names and integer values, like this: ``{"Nick": 56, "Paul":73, "Jackie":42}``, and **returns the name associated with the *lowest integer value**. (So in the case of that example dictionary, the function should return ``Jackie``.)

    .. tabbed:: func_review_4

        .. tab:: Problem

            .. actex:: fr_4

                # Write your code here!

                # Here's a sample call
                df = {"Nick": 56, "Paul":73, "Jackie":42}
                pritn smallest_value_name(df) # should print: Jackie

        .. tab:: Solution

            .. actex:: fr_4a

                # Here's one solution
                def smallest_value_name(d):
                    kys = d.keys() # returns a list of the keys in the dictionary d
                    m = kys[0]
                    for k in kys:
                        if d[k] < d[m]:
                            m = k
                    return m

                # Here's another solution
                def smallest_val_name_diff(d):
                    its = d.items() # returns a list of tuples (key, value) in dictionary d and stores it in its
                    tn = its[0]
                    for t in its:
                        if t[1] < tn[1]:
                            tn = t
                    return tn[0]

                # Sample calls of these solution functions
                d_new = {"Nick": 56, "Paul":73, "Jackie":42, "Ellie":36}
                print smallest_val_name(d_new)

                print smallest_val_name_diff(d_new)
                # both these calls above print "Ellie"!


             