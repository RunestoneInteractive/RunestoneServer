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


Week 7: ends February 21
========================

For this week you have the following graded activities:

1. Do the multiple choice questions and exercises in the textbook chapters, including the ones at the bottom of the chapters, below the glossary. Don't forget to click **Save** for each of the exercises.

   * Before Tuesday's class:      
      * :ref:`Nested Data <nested_data_chap>`
      * :ref:`Indefinite Iteration <while_loop>`
   
   * Before Thursday's class:
      * No additional textbook reading


#. Turn in the reading response, by 8 PM the night before your registered section meets.

   * Read *The Most Human Human*, Chapter 10
   * :ref:`Reading response 6 <response_6>`

#. Save answers to the exercises in Problem Set 6:

   * :ref:`Problem Set 6 <problem_set_6>`

#. Supplemental exercises:

   * :ref:`In-class exercises Tuesday <session_12>`

.. _response_6:

Reading Response 6
------------------

In what situations do you encounter high surprisal? Low surprisal? What kind of conversations do you have that contain a lot of information? Explain (briefly).

.. actex:: rr_6_1

   # Fill in your response in between the triple quotes
   s = """

   """
  
Give an example of compression other than the ones Christian addresses. Explain. Why? In what situations does this occur?

.. actex:: rr_6_2

   # Fill in your response in between the triple quotes
   s = """

   """

Was there anything from this chapter you found confusing? If so, what? What are some ways we can apply some of these concepts to what we know about programming, aside from playing the Shannon Game?

.. actex:: rr_6_3

   # Fill in your response in between the triple quotes
   s = """

   """

.. _problem_set_6:

Problem Set 6
-------------

In the problem set for this week we will be creating a program that plays the Shannon game.

Before we work on the Shannon game, let's work through a few warm up questions to test your understanding of nested data, and 
to introduce you to a nested data structure that we'll be using later on in the
problem set.

1. (1 point) Follow the directions in the code to read and manipulate the nested data structure 'heuristics_dictionary'.

.. tabbed:: ps_6_1_tabs

    .. tab:: Problem

        .. activecode:: ps_6_1

            heuristics_dictionary = {
                'a':{
                    'priority':2,
                    'guesses':['b','c','d','n','p','s'],
                    },
                'q':{
                    'priority':1,
                    'guesses':['uu','a'],
                    },
                'ti':{
                    'priority':1,
                    'guesses':['e', 'a', 'g', 'd', 'r', 'n']   
                    }      
            }


            # In one line of code, print out the list 
            #of guesses associated with the key 'q'
            
            # In one line of code, add the letter 'z' 
            # to the guesses associated with 'q'.
            
            # Add a key 'tim' to the dictionary, where the value is a dictionary
            # with the same structure that the others have.

    .. tab:: Solution

        .. activecode:: ps_6_1_a

            heuristics_dictionary = {
                'a':{
                    'priority':2,
                    'guesses':['b','c','d','n','p','s'],
                    },
                'q':{
                    'priority':1,
                    'guesses':['uu','a'],
                    },
                'ti':{
                    'priority':1,
                    'guesses':['e', 'a', 'g', 'd', 'r', 'n']   
                    }      
            }


            # In one line of code, print out the list 
            #of guesses associated with the key 'q'
            print heuristics_dictionary['q']['guesses']
            
            # In one line of code, add the letter 'z' 
            # to the guesses associated with 'q'.
            heuristics_dictionary['q']['guesses'].append('z')

            # Add a key 'tim' to the dictionary, where the value is a dictionary
            # with the same structure that the others have.
            heuristics_dictionary['tim'] = {
                'priority':2,
                'guesses': ['e',' ']
            }            
    
2. (1 point) Count the number of consonants in the all the 'guesses' lists of the nested datastructure 'heuristics.'

.. tabbed:: ps_6_2_tabs

    .. tab:: Problem

        .. activecode:: ps_6_2
          
            heuristics_dictionary = {
                'a':{
                    'priority':2,
                    'guesses':['b','c','d','n','p','s'],
                    },
                'q':{
                    'priority':1,
                    'guesses':['uu','a'],
                    },
                'ti':{
                    'priority':1,
                    'guesses':['e', 'a', 'g', 'd', 'r', 'n']
                    }        
            }

            # write code to count the number of consonants
            
            # the correct answer is 10

    .. tab:: Solution

        .. activecode:: ps_6_2_a
          
            heuristics_dictionary = {
                'a':{
                    'priority':2,
                    'guesses':['b','c','d','n','p','s'],
                    },
                'q':{
                    'priority':1,
                    'guesses':['uu','a'],
                    },
                'ti':{
                    'priority':1,
                    'guesses':['e', 'a', 'g', 'd', 'r', 'n']
                    }        
            }

            # write code to count the number of consonants
            count = 0
            for key in heuristics_dictionary:
                for l in heuristics_dictionary[key]['guesses']:
                    if l not in 'aeiouu':
                        count = count + 1
            
            # the correct answer is 10
            print "There are "+str(count)+" consonants in heuristics_dictionary."
    
Later on you will be using a dictionary like the one you've just been working with, to make guesses in the Shannon game.
The idea is that if the most recent letter in a text was 'a', then you should guess for the next letter, in order,
b, c, d, n, p, and s. If none of those is right, you would fall back on some other guessing method to generate
more guesses. Similarly, if the most recent two letters were 'ti', then for the next letter you would
guess, in order, e, then a, g, d, r, and n.

3. (1 points) Invoke game using alternative guessers

.. tabbed:: ps_6_3_tabs

    .. tab:: Problem

        .. activecode:: ps_6_3
          
            ####Don't change this code; add and change code at the bottom #####
            import random
            
            def letter_frequencies(txt):
                d = {}
                for c in txt:
                    if c not in d:
                        d[c] = 1
                    elif c in alphabet:
                        d[c] = d[c] + 1
                    # don't bother tracking letters that aren't in our alphabet
                return d
            
            def guess(prev_txt, guessed_already):
                # guess a letter randomly
                idx = random.randrange(0, len(alphabet))
                return alphabet[idx]    
            
            
            def guess_no_dup(prev_txt, guessed_already):
                # guess a letter randomly until you find one that hasn't been guessed yet
                while True:
                    idx = random.randrange(0, len(alphabet))
                    candidate =  alphabet[idx]
                    if candidate not in guessed_already:
                        return candidate     
            
            def keys_sorted_by_value(d):
                in_order = sorted(d.items(), None, lambda x: x[1], True)
                res = []
                for (k, v) in in_order:
                    res.append(k)
                return res
            
            def guess_by_frequency(prev_txt, guessed_already):
                # return the best one that hasn't been guessed yet
                for let in keys_sorted_by_value(overall_freqs):
                    if let not in guessed_already:
                        return let
                return None # No unguessed letters left; shouldn't happen!   
                
            def game(txt, feedback=True, guesser = guess):
                """Plays one game"""
                
                # accumulate the text that's been revealed
                revealed_text = ""
                
                # accumulate the total guess count
                total_guesses = 0
                # accumulate the total characters to be guessed
                total_chars = 0
                
                # Loop through the letters in the text, making a guess for each
                for c in txt:
                    if c in alphabet: # skip letters not in our alphabet; don't have to guess them
                        total_chars = total_chars + 1
                        # accumulate the guesses made for this letter
                        guesses = ""
                        guessed = False
                        if feedback:
                            print "guessing " + c,
                        while not guessed:
                            # guess until you get it right
                            g = guesser(revealed_text, guesses)
                            guesses = guesses + g
                            if g == c:
                                guessed = True
                            if feedback:
                                print g, 
                        
                        total_guesses = total_guesses + len(guesses)
                        revealed_text = revealed_text + c
                        if feedback:
                            print(str(len(guesses)) + " guesses ")
            
                return total_chars, total_guesses
            
                
            # note, the last two characters are the single quote and double quote. They are
            # escaped, writen as \' and \", similar to how we have used escaping for tabs, \t,
            # and newlines, \n.
            alphabet = " !#$%&()*,-./0123456789:;?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]abcdefghijklmnopqrstuvwxyz\'\""
            caps = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            
            f = open('train.txt', 'r')
            overall_freqs = letter_frequencies(f.read())
            caps_freqs = {}
            for c in caps:
                if c in overall_freqs:
                    caps_freqs[c] = overall_freqs[c]
            sorted_caps = keys_sorted_by_value(caps_freqs)
            heuristics = {'q':{'priority': 1, 'guesses':['uu', 'a']}, '. ':{'priority': 2, 'guesses': sorted_caps}}
            txt1 = "Question. Everything."
            txt2 = "Try to guess as Holmes would what the next letter will be in this quite short text. Now is the time."
           
            #### Don't change any code above this line #####  
            
            print(game(txt1))
            
            #Invoke game on txt1 using the alternate guessers 
            #guess_no_dup and guess_by_frequency
            #(Note: if it's running too slow, try invoking it with the
            #feedback parameter set to False.)

    .. tab:: Solution

        .. activecode:: ps_6_3
          
            ####Don't change this code; add and change code at the bottom #####
            import random
            
            def letter_frequencies(txt):
                d = {}
                for c in txt:
                    if c not in d:
                        d[c] = 1
                    elif c in alphabet:
                        d[c] = d[c] + 1
                    # don't bother tracking letters that aren't in our alphabet
                return d
            
            def guess(prev_txt, guessed_already):
                # guess a letter randomly
                idx = random.randrange(0, len(alphabet))
                return alphabet[idx]    
            
            
            def guess_no_dup(prev_txt, guessed_already):
                # guess a letter randomly until you find one that hasn't been guessed yet
                while True:
                    idx = random.randrange(0, len(alphabet))
                    candidate =  alphabet[idx]
                    if candidate not in guessed_already:
                        return candidate     
            
            def keys_sorted_by_value(d):
                in_order = sorted(d.items(), None, lambda x: x[1], True)
                res = []
                for (k, v) in in_order:
                    res.append(k)
                return res
            
            def guess_by_frequency(prev_txt, guessed_already):
                # return the best one that hasn't been guessed yet
                for let in keys_sorted_by_value(overall_freqs):
                    if let not in guessed_already:
                        return let
                return None # No unguessed letters left; shouldn't happen!   
                
            def game(txt, feedback=True, guesser = guess):
                """Plays one game"""
                
                # accumulate the text that's been revealed
                revealed_text = ""
                
                # accumulate the total guess count
                total_guesses = 0
                # accumulate the total characters to be guessed
                total_chars = 0
                
                # Loop through the letters in the text, making a guess for each
                for c in txt:
                    if c in alphabet: # skip letters not in our alphabet; don't have to guess them
                        total_chars = total_chars + 1
                        # accumulate the guesses made for this letter
                        guesses = ""
                        guessed = False
                        if feedback:
                            print "guessing " + c,
                        while not guessed:
                            # guess until you get it right
                            g = guesser(revealed_text, guesses)
                            guesses = guesses + g
                            if g == c:
                                guessed = True
                            if feedback:
                                print g, 
                        
                        total_guesses = total_guesses + len(guesses)
                        revealed_text = revealed_text + c
                        if feedback:
                            print(str(len(guesses)) + " guesses ")
            
                return total_chars, total_guesses
            
                
            # note, the last two characters are the single quote and double quote. They are
            # escaped, writen as \' and \", similar to how we have used escaping for tabs, \t,
            # and newlines, \n.
            alphabet = " !#$%&()*,-./0123456789:;?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]abcdefghijklmnopqrstuvwxyz\'\""
            caps = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            
            f = open('train.txt', 'r')
            overall_freqs = letter_frequencies(f.read())
            caps_freqs = {}
            for c in caps:
                if c in overall_freqs:
                    caps_freqs[c] = overall_freqs[c]
            sorted_caps = keys_sorted_by_value(caps_freqs)
            heuristics = {'q':{'priority': 1, 'guesses':['uu', 'a']}, '. ':{'priority': 2, 'guesses': sorted_caps}}
            txt1 = "Question. Everything."
            txt2 = "Try to guess as Holmes would what the next letter will be in this quite short text. Now is the time."
           
            #### Don't change any code above this line #####  
            
            game(txt1, False, guess_no_dup)
            game(txt1, False, guess_by_frequency)
            
            #Invoke game on txt1 using the alternate guessers 
            #guess_no_dup and guess_by_frequency
            #(Note: if it's running too slow, try invoking it with the
            #feedback parameter set to False.)

4. (1 points) write guess_after_q to guess u if previous letter was q

.. tabbed:: ps_6_4_tabs

    .. tab:: Problem

        .. activecode:: ps_6_4
          
            ####Don't change this code; add and change code at the bottom #####
            import random
            
            def letter_frequencies(txt):
                d = {}
                for c in txt:
                    if c not in d:
                        d[c] = 1
                    elif c in alphabet:
                        d[c] = d[c] + 1
                    # don't bother tracking letters that aren't in our alphabet
                return d
            
            def guess(prev_txt, guessed_already):
                # guess a letter randomly
                idx = random.randrange(0, len(alphabet))
                return alphabet[idx]    
            
            
            def guess_no_dup(prev_txt, guessed_already):
                # guess a letter randomly until you find one that hasn't been guessed yet
                while True:
                    idx = random.randrange(0, len(alphabet))
                    candidate =  alphabet[idx]
                    if candidate not in guessed_already:
                        return candidate     
            
            def keys_sorted_by_value(d):
                in_order = sorted(d.items(), None, lambda x: x[1], True)
                res = []
                for (k, v) in in_order:
                    res.append(k)
                return res
            
            def guess_by_frequency(prev_txt, guessed_already):
                # return the best one that hasn't been guessed yet
                for let in keys_sorted_by_value(overall_freqs):
                    if let not in guessed_already:
                        return let
                return None # No unguessed letters left; shouldn't happen!   
                
            def game(txt, feedback=True, guesser = guess):
                """Plays one game"""
                
                # accumulate the text that's been revealed
                revealed_text = ""
                
                # accumulate the total guess count
                total_guesses = 0
                # accumulate the total characters to be guessed
                total_chars = 0
                
                # Loop through the letters in the text, making a guess for each
                for c in txt:
                    if c in alphabet: # skip letters not in our alphabet; don't have to guess them
                        total_chars = total_chars + 1
                        # accumulate the guesses made for this letter
                        guesses = ""
                        guessed = False
                        if feedback:
                            print "guessing " + c,
                        while not guessed:
                            # guess until you get it right
                            g = guesser(revealed_text, guesses)
                            guesses = guesses + g
                            if g == c:
                                guessed = True
                            if feedback:
                                print g, 
                        
                        total_guesses = total_guesses + len(guesses)
                        revealed_text = revealed_text + c
                        if feedback:
                            print(str(len(guesses)) + " guesses ")
            
                return total_chars, total_guesses
            
                
            # note, the last two characters are the single quote and double quote. They are
            # escaped, writen as \' and \", similar to how we have used escaping for tabs, \t,
            # and newlines, \n.
            alphabet = " !#$%&()*,-./0123456789:;?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]abcdefghijklmnopqrstuvwxyz\'\""
            caps = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            
            f = open('train.txt', 'r')
            overall_freqs = letter_frequencies(f.read())
            caps_freqs = {}
            for c in caps:
                if c in overall_freqs:
                    caps_freqs[c] = overall_freqs[c]
            sorted_caps = keys_sorted_by_value(caps_freqs)
            heuristics = {'q':{'priority': 1, 'guesses':['uu', 'a']}, '. ':{'priority': 2, 'guesses': sorted_caps}}
            txt1 = "Question. Everything."
            txt2 = "Try to guess as Holmes would what the next letter will be in this quite short text. Now is the time."
           
            #### Don't change any code above this line #####  
            
            # Fill in the function definition below
            
            def u_after_q(prev_txt, guessed_already):
                # Fill this in.
                # If the most recent letter of prev_txt
                # was q, guess u.
                # Otherwise, get a from guess_by_frequency
                
            import test
            test.testEqual(u_after_q("This q", " eta"), "u")
            test.testEqual(u_after_q("This q", "uta "), "e")
            test.testEqual(u_after_q("This ", " e"), "t")
            
            # once you pass the tests, make calls to guess to see many fewer guesses
            # are needed with u_after_q than with guess_by_frequency

    .. tab:: Solution

        .. activecode:: ps_6_4_a
          
            ####Don't change this code; add and change code at the bottom #####
            import random
            
            def letter_frequencies(txt):
                d = {}
                for c in txt:
                    if c not in d:
                        d[c] = 1
                    elif c in alphabet:
                        d[c] = d[c] + 1
                    # don't bother tracking letters that aren't in our alphabet
                return d
            
            def guess(prev_txt, guessed_already):
                # guess a letter randomly
                idx = random.randrange(0, len(alphabet))
                return alphabet[idx]    
            
            
            def guess_no_dup(prev_txt, guessed_already):
                # guess a letter randomly until you find one that hasn't been guessed yet
                while True:
                    idx = random.randrange(0, len(alphabet))
                    candidate =  alphabet[idx]
                    if candidate not in guessed_already:
                        return candidate     
            
            def keys_sorted_by_value(d):
                in_order = sorted(d.items(), None, lambda x: x[1], True)
                res = []
                for (k, v) in in_order:
                    res.append(k)
                return res
            
            def guess_by_frequency(prev_txt, guessed_already):
                # return the best one that hasn't been guessed yet
                for let in keys_sorted_by_value(overall_freqs):
                    if let not in guessed_already:
                        return let
                return None # No unguessed letters left; shouldn't happen!   
                
            def game(txt, feedback=True, guesser = guess):
                """Plays one game"""
                
                # accumulate the text that's been revealed
                revealed_text = ""
                
                # accumulate the total guess count
                total_guesses = 0
                # accumulate the total characters to be guessed
                total_chars = 0
                
                # Loop through the letters in the text, making a guess for each
                for c in txt:
                    if c in alphabet: # skip letters not in our alphabet; don't have to guess them
                        total_chars = total_chars + 1
                        # accumulate the guesses made for this letter
                        guesses = ""
                        guessed = False
                        if feedback:
                            print "guessing " + c,
                        while not guessed:
                            # guess until you get it right
                            g = guesser(revealed_text, guesses)
                            guesses = guesses + g
                            if g == c:
                                guessed = True
                            if feedback:
                                print g, 
                        
                        total_guesses = total_guesses + len(guesses)
                        revealed_text = revealed_text + c
                        if feedback:
                            print(str(len(guesses)) + " guesses ")
            
                return total_chars, total_guesses
            
                
            # note, the last two characters are the single quote and double quote. They are
            # escaped, writen as \' and \", similar to how we have used escaping for tabs, \t,
            # and newlines, \n.
            alphabet = " !#$%&()*,-./0123456789:;?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]abcdefghijklmnopqrstuvwxyz\'\""
            caps = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            
            f = open('train.txt', 'r')
            overall_freqs = letter_frequencies(f.read())
            caps_freqs = {}
            for c in caps:
                if c in overall_freqs:
                    caps_freqs[c] = overall_freqs[c]
            sorted_caps = keys_sorted_by_value(caps_freqs)
            heuristics = {'q':{'priority': 1, 'guesses':['uu', 'a']}, '. ':{'priority': 2, 'guesses': sorted_caps}}
            txt1 = "Question. Everything."
            txt2 = "Try to guess as Holmes would what the next letter will be in this quite short text. Now is the time."
           
            #### Don't change any code above this line #####  
            
            # Fill in the function definition below
            
            def u_after_q(prev_txt, guessed_already):
                if len(prev_txt) > 1 and prev_txt[-1].lower() == 'q':
                    if 'uu' not in guessed_already:
                        return 'uu'
                return guess_by_frequency(prev_txt, guessed_already)
                
            import test
            test.testEqual(u_after_q("This q", " eta"), "u")
            test.testEqual(u_after_q("This q", "uta "), "e")
            test.testEqual(u_after_q("This ", " e"), "t")
            
            # once you pass the tests, make calls to guess to see many fewer guesses
            # are needed with u_after_q than with guess_by_frequency

            g1 = game(txt1, False, guess_by_frequency)
            g2 = game(txt1, False, u_after_q)

            diff = g1[1] - g2[1]
            print "There are "+str(diff)+" fewer guesses"

5. (1 point) Try guessing capitals first for a new sentence

.. tabbed:: ps_6_5_tabs

    .. tab:: Problem

        .. activecode:: ps_6_5
          
            ####Don't change this code; add and change code at the bottom #####
            import random
            
            def letter_frequencies(txt):
                d = {}
                for c in txt:
                    if c not in d:
                        d[c] = 1
                    elif c in alphabet:
                        d[c] = d[c] + 1
                    # don't bother tracking letters that aren't in our alphabet
                return d
            
            def guess(prev_txt, guessed_already):
                # guess a letter randomly
                idx = random.randrange(0, len(alphabet))
                return alphabet[idx]    
            
            
            def guess_no_dup(prev_txt, guessed_already):
                # guess a letter randomly until you find one that hasn't been guessed yet
                while True:
                    idx = random.randrange(0, len(alphabet))
                    candidate =  alphabet[idx]
                    if candidate not in guessed_already:
                        return candidate     
            
            def keys_sorted_by_value(d):
                in_order = sorted(d.items(), None, lambda x: x[1], True)
                res = []
                for (k, v) in in_order:
                    res.append(k)
                return res
            
            def guess_by_frequency(prev_txt, guessed_already):
                # return the best one that hasn't been guessed yet
                for let in keys_sorted_by_value(overall_freqs):
                    if let not in guessed_already:
                        return let
                return None # No unguessed letters left; shouldn't happen!   
                
            def game(txt, feedback=True, guesser = guess):
                """Plays one game"""
                
                # accumulate the text that's been revealed
                revealed_text = ""
                
                # accumulate the total guess count
                total_guesses = 0
                # accumulate the total characters to be guessed
                total_chars = 0
                
                # Loop through the letters in the text, making a guess for each
                for c in txt:
                    if c in alphabet: # skip letters not in our alphabet; don't have to guess them
                        total_chars = total_chars + 1
                        # accumulate the guesses made for this letter
                        guesses = ""
                        guessed = False
                        if feedback:
                            print "guessing " + c,
                        while not guessed:
                            # guess until you get it right
                            g = guesser(revealed_text, guesses)
                            guesses = guesses + g
                            if g == c:
                                guessed = True
                            if feedback:
                                print g, 
                        
                        total_guesses = total_guesses + len(guesses)
                        revealed_text = revealed_text + c
                        if feedback:
                            print(str(len(guesses)) + " guesses ")
            
                return total_chars, total_guesses
            
                
            # note, the last two characters are the single quote and double quote. They are
            # escaped, writen as \' and \", similar to how we have used escaping for tabs, \t,
            # and newlines, \n.
            alphabet = " !#$%&()*,-./0123456789:;?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]abcdefghijklmnopqrstuvwxyz\'\""
            caps = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            
            f = open('train.txt', 'r')
            overall_freqs = letter_frequencies(f.read())
            caps_freqs = {}
            for c in caps:
                if c in overall_freqs:
                    caps_freqs[c] = overall_freqs[c]
            sorted_caps = keys_sorted_by_value(caps_freqs)
            heuristics = {'q':{'priority': 1, 'guesses':['uu', 'a']}, '. ':{'priority': 2, 'guesses': sorted_caps}}
            txt1 = "Question. Everything."
            txt2 = "Try to guess as Holmes would what the next letter will be in this quite short text. Now is the time."
           
            #### Don't change any code above this line #####  
            
            # Fill in the function definition below
            
            def new_sentence_cap(prev_txt, guessed_already):
                # Fill this in.
                # If the most recent two letters of prev_txt
                # were a period followed by a space, try guessing
                # capitals, in order of their frequency.
                # If not capital letter works, get a from guess_by_frequency.
                # (Hint: the global variable sorted_caps already has
                # the capital letters in order of how frequently they occur in
                # the long text train.txt)
                
            import test
            test.testEqual(new_sentence_cap("Question. ", ""), "I")
            test.testEqual(new_sentence_cap("Question. ", "IH"), "T")
            test.testEqual(new_sentence_cap("This ", " et"), "a")

            # once you pass the tests, make calls to guess to see many fewer guesses
            # are needed with new_sentence_cap than with guess_by_frequency

    .. tab:: Solution

        .. activecode:: ps_6_5_a
          
            ####Don't change this code; add and change code at the bottom #####
            import random
            
            def letter_frequencies(txt):
                d = {}
                for c in txt:
                    if c not in d:
                        d[c] = 1
                    elif c in alphabet:
                        d[c] = d[c] + 1
                    # don't bother tracking letters that aren't in our alphabet
                return d
            
            def guess(prev_txt, guessed_already):
                # guess a letter randomly
                idx = random.randrange(0, len(alphabet))
                return alphabet[idx]    
            
            
            def guess_no_dup(prev_txt, guessed_already):
                # guess a letter randomly until you find one that hasn't been guessed yet
                while True:
                    idx = random.randrange(0, len(alphabet))
                    candidate =  alphabet[idx]
                    if candidate not in guessed_already:
                        return candidate     
            
            def keys_sorted_by_value(d):
                in_order = sorted(d.items(), None, lambda x: x[1], True)
                res = []
                for (k, v) in in_order:
                    res.append(k)
                return res
            
            def guess_by_frequency(prev_txt, guessed_already):
                # return the best one that hasn't been guessed yet
                for let in keys_sorted_by_value(overall_freqs):
                    if let not in guessed_already:
                        return let
                return None # No unguessed letters left; shouldn't happen!   
                
            def game(txt, feedback=True, guesser = guess):
                """Plays one game"""
                
                # accumulate the text that's been revealed
                revealed_text = ""
                
                # accumulate the total guess count
                total_guesses = 0
                # accumulate the total characters to be guessed
                total_chars = 0
                
                # Loop through the letters in the text, making a guess for each
                for c in txt:
                    if c in alphabet: # skip letters not in our alphabet; don't have to guess them
                        total_chars = total_chars + 1
                        # accumulate the guesses made for this letter
                        guesses = ""
                        guessed = False
                        if feedback:
                            print "guessing " + c,
                        while not guessed:
                            # guess until you get it right
                            g = guesser(revealed_text, guesses)
                            guesses = guesses + g
                            if g == c:
                                guessed = True
                            if feedback:
                                print g, 
                        
                        total_guesses = total_guesses + len(guesses)
                        revealed_text = revealed_text + c
                        if feedback:
                            print(str(len(guesses)) + " guesses ")
            
                return total_chars, total_guesses
            
                
            # note, the last two characters are the single quote and double quote. They are
            # escaped, writen as \' and \", similar to how we have used escaping for tabs, \t,
            # and newlines, \n.
            alphabet = " !#$%&()*,-./0123456789:;?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]abcdefghijklmnopqrstuvwxyz\'\""
            caps = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            
            f = open('train.txt', 'r')
            overall_freqs = letter_frequencies(f.read())
            caps_freqs = {}
            for c in caps:
                if c in overall_freqs:
                    caps_freqs[c] = overall_freqs[c]
            sorted_caps = keys_sorted_by_value(caps_freqs)
            heuristics = {'q':{'priority': 1, 'guesses':['uu', 'a']}, '. ':{'priority': 2, 'guesses': sorted_caps}}
            txt1 = "Question. Everything."
            txt2 = "Try to guess as Holmes would what the next letter will be in this quite short text. Now is the time."
           
            #### Don't change any code above this line #####  
            
            # Fill in the function definition below
            
            def new_sentence_cap(prev_txt, guessed_already):
                if len(prev_txt) >= 2 and prev_txt[-2:] == ". ":
                    for l in sorted_caps:
                        if l not in guessed_already:
                            return l
                return guess_by_frequency(prev_txt, guessed_already)
                
            import test
            test.testEqual(new_sentence_cap("Question. ", ""), "I")
            test.testEqual(new_sentence_cap("Question. ", "IH"), "T")
            test.testEqual(new_sentence_cap("This ", " et"), "a")

            # once you pass the tests, make calls to guess to see many fewer guesses
            # are needed with new_sentence_cap than with guess_by_frequency
            g1 = game(txt1, False, guess_by_frequency)
            g2 = game(txt1, False, new_sentence_cap)

            diff = g1[1] - g2[1]
            print "There are "+str(diff)+" fewer guesses"


6. (2 points) Generalize the previous two functions

.. tabbed:: ps_6_6_tabs

    .. tab:: Problem

        .. activecode:: ps_6_6
          
            ####Don't change this code; add and change code at the bottom #####
            import random
            
            def letter_frequencies(txt):
                d = {}
                for c in txt:
                    if c not in d:
                        d[c] = 1
                    elif c in alphabet:
                        d[c] = d[c] + 1
                    # don't bother tracking letters that aren't in our alphabet
                return d
            
            def guess(prev_txt, guessed_already):
                # guess a letter randomly
                idx = random.randrange(0, len(alphabet))
                return alphabet[idx]    
            
            
            def guess_no_dup(prev_txt, guessed_already):
                # guess a letter randomly until you find one that hasn't been guessed yet
                while True:
                    idx = random.randrange(0, len(alphabet))
                    candidate =  alphabet[idx]
                    if candidate not in guessed_already:
                        return candidate     
            
            def keys_sorted_by_value(d):
                in_order = sorted(d.items(), None, lambda x: x[1], True)
                res = []
                for (k, v) in in_order:
                    res.append(k)
                return res
            
            def guess_by_frequency(prev_txt, guessed_already):
                # return the best one that hasn't been guessed yet
                for let in keys_sorted_by_value(overall_freqs):
                    if let not in guessed_already:
                        return let
                return None # No unguessed letters left; shouldn't happen!   
                
            def game(txt, feedback=True, guesser = guess):
                """Plays one game"""
                
                # accumulate the text that's been revealed
                revealed_text = ""
                
                # accumulate the total guess count
                total_guesses = 0
                # accumulate the total characters to be guessed
                total_chars = 0
                
                # Loop through the letters in the text, making a guess for each
                for c in txt:
                    if c in alphabet: # skip letters not in our alphabet; don't have to guess them
                        total_chars = total_chars + 1
                        # accumulate the guesses made for this letter
                        guesses = ""
                        guessed = False
                        if feedback:
                            print "guessing " + c,
                        while not guessed:
                            # guess until you get it right
                            g = guesser(revealed_text, guesses)
                            guesses = guesses + g
                            if g == c:
                                guessed = True
                            if feedback:
                                print g, 
                        
                        total_guesses = total_guesses + len(guesses)
                        revealed_text = revealed_text + c
                        if feedback:
                            print(str(len(guesses)) + " guesses ")
            
                return total_chars, total_guesses
            
                
            # note, the last two characters are the single quote and double quote. They are
            # escaped, writen as \' and \", similar to how we have used escaping for tabs, \t,
            # and newlines, \n.
            alphabet = " !#$%&()*,-./0123456789:;?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]abcdefghijklmnopqrstuvwxyz\'\""
            caps = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            
            f = open('train.txt', 'r')
            overall_freqs = letter_frequencies(f.read())
            caps_freqs = {}
            for c in caps:
                if c in overall_freqs:
                    caps_freqs[c] = overall_freqs[c]
            sorted_caps = keys_sorted_by_value(caps_freqs)
            heuristics = {'q':{'priority': 1, 'guesses':['uu', 'a']}, '. ':{'priority': 2, 'guesses': sorted_caps}}
            txt1 = "Question. Everything."
            txt2 = "Try to guess as Holmes would what the next letter will be in this quite short text. Now is the time."
           
            #### Don't change any code above this line #####  
            
            # Fill in the function definition below
            
            def heuristic_guesser(prev_txt, guessed_already):
                # We are providing the next line for you
                # print sorted_heuristics to see what it produces 
                sorted_heuristics = sorted(heuristics.items(), None, lambda x: x[1]['priority'], True)
                
                # Fill this in.
                # Generalize from the previous two problems. The dictionary 
                # heuristics contains information about what guesses to make when
                # the most recent revealed text matches one of the
                # dictionary's keys. Each key's value is a dictionary with a key
                # for the priority of that heuristic, and key for what guesses
                # to make. 
                
                # Your code should process the heuristics in order of
                # their priority (see the variable sorted_heuristics that
                # is provided for you in this function). 
                
                # If the key matches the most recent letter (or letters, 
                # if the key is more than one letter), then return 
                # the first letter in its guesses that has not been guessed yet.
                
            import test
            test.testEqual(heuristic_guesser("This q", " eta"), "u")
            test.testEqual(heuristic_guesser("This q", "u t"), "e")
            test.testEqual(heuristic_guesser("This ", " e"), "t")
            test.testEqual(heuristic_guesser("Question. ", ""), "I")
            test.testEqual(heuristic_guesser("Question. ", "IH"), "T")
            test.testEqual(heuristic_guesser("This ", " et"), "a")

            # once you pass the tests, make calls to guess to see many fewer guesses
            # are needed with heuristic_guesser
            
            # now add a few more entries into the heuristics dictionary, and try
            # running guess() again with heuristic_guesser, to see how much improvement 
            # the extra dictionary entries give you.

    .. tab:: Solution

        .. activecode:: ps_6_6_a
          
            ####Don't change this code; add and change code at the bottom #####
            import random
            
            def letter_frequencies(txt):
                d = {}
                for c in txt:
                    if c not in d:
                        d[c] = 1
                    elif c in alphabet:
                        d[c] = d[c] + 1
                    # don't bother tracking letters that aren't in our alphabet
                return d
            
            def guess(prev_txt, guessed_already):
                # guess a letter randomly
                idx = random.randrange(0, len(alphabet))
                return alphabet[idx]    
            
            
            def guess_no_dup(prev_txt, guessed_already):
                # guess a letter randomly until you find one that hasn't been guessed yet
                while True:
                    idx = random.randrange(0, len(alphabet))
                    candidate =  alphabet[idx]
                    if candidate not in guessed_already:
                        return candidate     
            
            def keys_sorted_by_value(d):
                in_order = sorted(d.items(), None, lambda x: x[1], True)
                res = []
                for (k, v) in in_order:
                    res.append(k)
                return res
            
            def guess_by_frequency(prev_txt, guessed_already):
                # return the best one that hasn't been guessed yet
                for let in keys_sorted_by_value(overall_freqs):
                    if let not in guessed_already:
                        return let
                return None # No unguessed letters left; shouldn't happen!   
                
            def game(txt, feedback=True, guesser = guess):
                """Plays one game"""
                
                # accumulate the text that's been revealed
                revealed_text = ""
                
                # accumulate the total guess count
                total_guesses = 0
                # accumulate the total characters to be guessed
                total_chars = 0
                
                # Loop through the letters in the text, making a guess for each
                for c in txt:
                    if c in alphabet: # skip letters not in our alphabet; don't have to guess them
                        total_chars = total_chars + 1
                        # accumulate the guesses made for this letter
                        guesses = ""
                        guessed = False
                        if feedback:
                            print "guessing " + c,
                        while not guessed:
                            # guess until you get it right
                            g = guesser(revealed_text, guesses)
                            guesses = guesses + g
                            if g == c:
                                guessed = True
                            if feedback:
                                print g, 
                        
                        total_guesses = total_guesses + len(guesses)
                        revealed_text = revealed_text + c
                        if feedback:
                            print(str(len(guesses)) + " guesses ")
            
                return total_chars, total_guesses
            
                
            # note, the last two characters are the single quote and double quote. They are
            # escaped, writen as \' and \", similar to how we have used escaping for tabs, \t,
            # and newlines, \n.
            alphabet = " !#$%&()*,-./0123456789:;?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]abcdefghijklmnopqrstuvwxyz\'\""
            caps = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            
            f = open('train.txt', 'r')
            overall_freqs = letter_frequencies(f.read())
            caps_freqs = {}
            for c in caps:
                if c in overall_freqs:
                    caps_freqs[c] = overall_freqs[c]
            sorted_caps = keys_sorted_by_value(caps_freqs)
            heuristics = {'q':{'priority': 1, 'guesses':['uu', 'a']}, '. ':{'priority': 2, 'guesses': sorted_caps}}
            txt1 = "Question. Everything."
            txt2 = "Try to guess as Holmes would what the next letter will be in this quite short text. Now is the time."
           
            #### Don't change any code above this line #####  
            
            # Fill in the function definition below
            
            def heuristic_guesser(prev_txt, guessed_already):
                sorted_heuristics = sorted(heuristics.items(), None, lambda x: x[1]['priority'], False)

                for key,value in sorted_heuristics:
                    key_length = len(key)
                    if len(prev_txt) >= key_length and prev_txt[-key_length:].lower() == key:
                        for l in value['guesses']:
                            if l not in guessed_already:
                                return l
                return guess_by_frequency(prev_txt, guessed_already)
                
            import test
            test.testEqual(heuristic_guesser("This q", " eta"), "u")
            test.testEqual(heuristic_guesser("This q", "u ta"), "e")
            test.testEqual(heuristic_guesser("This ", " e"), "t")
            test.testEqual(heuristic_guesser("Question. ", ""), "I")
            test.testEqual(heuristic_guesser("Question. ", "IH"), "T")
            test.testEqual(heuristic_guesser("This ", " et"), "a")

            # once you pass the tests, make calls to guess to see many fewer guesses
            # are needed with heuristic_guesser

            g1 = game(txt1, False, guess_by_frequency)
            g2 = game(txt1, False, heuristic_guesser)

            diff = g1[1] - g2[1]
            print "There are "+str(diff)+" fewer guesses"
            
            # now add a few more entries into the heuristics dictionary, and try
            # running guess() again with heuristic_guesser, to see how much improvement 
            # the extra dictionary entries give you.

            heuristics['u'] = {
                'priority':4,
                'guesses': ['e'],
            }
            heuristics['v'] = {
                'priority':4,
                'guesses': ['e'],
            }
            heuristics['th'] = {
                'priority':2,
                'guesses': ['e','i'],
            }

            g1 = game(txt1, False, guess_by_frequency)
            g2 = game(txt1, False, heuristic_guesser)

            diff = g1[1] - g2[1]
            print "There are "+str(diff)+" fewer guesses"

   
7. (1 point) Add heuristics to the dictionary

.. tabbed:: ps_6_7_tabs

    .. tab:: Problem

        .. activecode:: ps_6_7
           
            ####Don't change this code; add and change code at the bottom #####
            import random
            
            def letter_frequencies(txt):
                d = {}
                for c in txt:
                    if c not in d:
                        d[c] = 1
                    elif c in alphabet:
                        d[c] = d[c] + 1
                    # don't bother tracking letters that aren't in our alphabet
                return d
            
            def guess(prev_txt, guessed_already):
                # guess a letter randomly
                idx = random.randrange(0, len(alphabet))
                return alphabet[idx]    
            
            
            def guess_no_dup(prev_txt, guessed_already):
                # guess a letter randomly until you find one that hasn't been guessed yet
                while True:
                    idx = random.randrange(0, len(alphabet))
                    candidate =  alphabet[idx]
                    if candidate not in guessed_already:
                        return candidate     
            
            def keys_sorted_by_value(d):
                in_order = sorted(d.items(), None, lambda x: x[1], True)
                res = []
                for (k, v) in in_order:
                    res.append(k)
                return res
            
            def guess_by_frequency(prev_txt, guessed_already):
                # return the best one that hasn't been guessed yet
                for let in keys_sorted_by_value(overall_freqs):
                    if let not in guessed_already:
                        return let
                return None # No unguessed letters left; shouldn't happen!   
                
            def game(txt, feedback=True, guesser = guess):
                """Plays one game"""
                
                # accumulate the text that's been revealed
                revealed_text = ""
                
                # accumulate the total guess count
                total_guesses = 0
                # accumulate the total characters to be guessed
                total_chars = 0
                
                # Loop through the letters in the text, making a guess for each
                for c in txt:
                    if c in alphabet: # skip letters not in our alphabet; don't have to guess them
                        total_chars = total_chars + 1
                        # accumulate the guesses made for this letter
                        guesses = ""
                        guessed = False
                        if feedback:
                            print "guessing " + c,
                        while not guessed:
                            # guess until you get it right
                            g = guesser(revealed_text, guesses)
                            guesses = guesses + g
                            if g == c:
                                guessed = True
                            if feedback:
                                print g, 
                        
                        total_guesses = total_guesses + len(guesses)
                        revealed_text = revealed_text + c
                        if feedback:
                            print(str(len(guesses)) + " guesses ")
            
                return total_chars, total_guesses
            
                
            # note, the last two characters are the single quote and double quote. They are
            # escaped, writen as \' and \", similar to how we have used escaping for tabs, \t,
            # and newlines, \n.
            alphabet = " !#$%&()*,-./0123456789:;?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]abcdefghijklmnopqrstuvwxyz\'\""
            caps = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            
            f = open('train.txt', 'r')
            overall_freqs = letter_frequencies(f.read())
            caps_freqs = {}
            for c in caps:
                if c in overall_freqs:
                    caps_freqs[c] = overall_freqs[c]
            sorted_caps = keys_sorted_by_value(caps_freqs)
            heuristics = {'q':{'priority': 1, 'guesses':['uu', 'a']}, '. ':{'priority': 2, 'guesses': sorted_caps}}
            txt1 = "Question. Everything."
            txt2 = "Try to guess as Holmes would what the next letter will be in this quite short text. Now is the time."
           
            #### Don't change any code above this line #####  
            
            # Add to the heuristics dictionary entries for all the 
            # prefixes of the word 'time' (i.e., after a t, guess i, after ti guess m,
            # after tim guess e, and after time guess space or period
            
            import test
            test.testEqual(heuristics['ti']['guesses'][0], 'm')
            
            # We have provided a function, add_word, that generalizes what you
            # just did with 'time'. It automatically adds all
            # the prefixes for any word, with the next letter of the word as
            # the only guess.
            def add_word(w, pri = 2):
                """Takes a word w as input and adds all its prefixes to the 
                heuristics dictionary"""
                for i in range(len(w)-1):
                    prefix = w[:i+1]
                    next_let = w[i+1]
                    heuristics[prefix] = {'priority' : pri, 'guesses':[next_let]}
                heuristics[w] = {'priority' : pri, 'guesses':[' ', '.', ',']}
            
            # Invoke add_words as necessary to make the tests pass
            
            test.testEqual(heuristics['Ho']['priority'], 3)
            test.testEqual(heuristics['Ho']['guesses'][0], 'l')
            test.testEqual(heuristics['gue']['guesses'][0], 's')
            test.testEqual(heuristics['nex']['guesses'][0], 't')

    .. tab:: Solution

        .. activecode:: ps_6_7_a
           
            ####Don't change this code; add and change code at the bottom #####
            import random
            
            def letter_frequencies(txt):
                d = {}
                for c in txt:
                    if c not in d:
                        d[c] = 1
                    elif c in alphabet:
                        d[c] = d[c] + 1
                    # don't bother tracking letters that aren't in our alphabet
                return d
            
            def guess(prev_txt, guessed_already):
                # guess a letter randomly
                idx = random.randrange(0, len(alphabet))
                return alphabet[idx]    
            
            
            def guess_no_dup(prev_txt, guessed_already):
                # guess a letter randomly until you find one that hasn't been guessed yet
                while True:
                    idx = random.randrange(0, len(alphabet))
                    candidate =  alphabet[idx]
                    if candidate not in guessed_already:
                        return candidate     
            
            def keys_sorted_by_value(d):
                in_order = sorted(d.items(), None, lambda x: x[1], True)
                res = []
                for (k, v) in in_order:
                    res.append(k)
                return res
            
            def guess_by_frequency(prev_txt, guessed_already):
                # return the best one that hasn't been guessed yet
                for let in keys_sorted_by_value(overall_freqs):
                    if let not in guessed_already:
                        return let
                return None # No unguessed letters left; shouldn't happen!   
                
            def game(txt, feedback=True, guesser = guess):
                """Plays one game"""
                
                # accumulate the text that's been revealed
                revealed_text = ""
                
                # accumulate the total guess count
                total_guesses = 0
                # accumulate the total characters to be guessed
                total_chars = 0
                
                # Loop through the letters in the text, making a guess for each
                for c in txt:
                    if c in alphabet: # skip letters not in our alphabet; don't have to guess them
                        total_chars = total_chars + 1
                        # accumulate the guesses made for this letter
                        guesses = ""
                        guessed = False
                        if feedback:
                            print "guessing " + c,
                        while not guessed:
                            # guess until you get it right
                            g = guesser(revealed_text, guesses)
                            guesses = guesses + g
                            if g == c:
                                guessed = True
                            if feedback:
                                print g, 
                        
                        total_guesses = total_guesses + len(guesses)
                        revealed_text = revealed_text + c
                        if feedback:
                            print(str(len(guesses)) + " guesses ")
            
                return total_chars, total_guesses
            
                
            # note, the last two characters are the single quote and double quote. They are
            # escaped, writen as \' and \", similar to how we have used escaping for tabs, \t,
            # and newlines, \n.
            alphabet = " !#$%&()*,-./0123456789:;?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]abcdefghijklmnopqrstuvwxyz\'\""
            caps = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            
            f = open('train.txt', 'r')
            overall_freqs = letter_frequencies(f.read())
            caps_freqs = {}
            for c in caps:
                if c in overall_freqs:
                    caps_freqs[c] = overall_freqs[c]
            sorted_caps = keys_sorted_by_value(caps_freqs)
            heuristics = {'q':{'priority': 1, 'guesses':['uu', 'a']}, '. ':{'priority': 2, 'guesses': sorted_caps}}
            txt1 = "Question. Everything."
            txt2 = "Try to guess as Holmes would what the next letter will be in this quite short text. Now is the time."
           
            #### Don't change any code above this line #####  
            
            # Add to the heuristics dictionary entries for all the 
            # prefixes of the word 'time' (i.e., after a t, guess i, after ti guess m,
            # after tim guess e, and after time guess space or period

            heuristics['t'] = {
                'priority': 2,
                'guesses': ['i']
            }
            heuristics['ti'] = {
                'priority': 2,
                'guesses': ['m']
            }
            heuristics['tim'] = {
                'priority': 2,
                'guesses': ['e']
            }
            heuristics['time'] = {
                'priority': 2,
                'guesses': [' ','.']
            }
            
            import test
            test.testEqual(heuristics['ti']['guesses'][0], 'm')
            
            # We have provided a function, add_word, that generalizes what you
            # just did with 'time'. It automatically adds all
            # the prefixes for any word, with the next letter of the word as
            # the only guess.
            def add_word(w, pri = 2):
                """Takes a word w as input and adds all its prefixes to the 
                heuristics dictionary"""
                for i in range(len(w)-1):
                    prefix = w[:i+1]
                    next_let = w[i+1]
                    heuristics[prefix] = {'priority' : pri, 'guesses':[next_let]}
                heuristics[w] = {'priority' : pri, 'guesses':[' ', '.', ',']}
            
            # Invoke add_words as necessary to make the tests pass
            
            add_word('Hole',3)
            add_word('guess')
            add_word('next')
            #OR
            for w in txt2.split():
                add_word(w,3)
            
            test.testEqual(heuristics['Ho']['priority'], 3)
            test.testEqual(heuristics['Ho']['guesses'][0], 'l')
            test.testEqual(heuristics['gue']['guesses'][0], 's')
            test.testEqual(heuristics['nex']['guesses'][0], 't')

.. activecode:: ps_6_7
   
    ####Don't change this code; add and change code at the bottom #####
    import random
    
    def letter_frequencies(txt):
        d = {}
        for c in txt:
            if c not in d:
                d[c] = 1
            elif c in alphabet:
                d[c] = d[c] + 1
            # don't bother tracking letters that aren't in our alphabet
        return d
    
    def guess(prev_txt, guessed_already):
        # guess a letter randomly
        idx = random.randrange(0, len(alphabet))
        return alphabet[idx]    
    
    
    def guess_no_dup(prev_txt, guessed_already):
        # guess a letter randomly until you find one that hasn't been guessed yet
        while True:
            idx = random.randrange(0, len(alphabet))
            candidate =  alphabet[idx]
            if candidate not in guessed_already:
                return candidate     
    
    def keys_sorted_by_value(d):
        in_order = sorted(d.items(), None, lambda x: x[1], True)
        res = []
        for (k, v) in in_order:
            res.append(k)
        return res
    
    def guess_by_frequency(prev_txt, guessed_already):
        # return the best one that hasn't been guessed yet
        for let in keys_sorted_by_value(overall_freqs):
            if let not in guessed_already:
                return let
        return None # No unguessed letters left; shouldn't happen!   
        
    def game(txt, feedback=True, guesser = guess):
        """Plays one game"""
        
        # accumulate the text that's been revealed
        revealed_text = ""
        
        # accumulate the total guess count
        total_guesses = 0
        # accumulate the total characters to be guessed
        total_chars = 0
        
        # Loop through the letters in the text, making a guess for each
        for c in txt:
            if c in alphabet: # skip letters not in our alphabet; don't have to guess them
                total_chars = total_chars + 1
                # accumulate the guesses made for this letter
                guesses = ""
                guessed = False
                if feedback:
                    print "guessing " + c,
                while not guessed:
                    # guess until you get it right
                    g = guesser(revealed_text, guesses)
                    guesses = guesses + g
                    if g == c:
                        guessed = True
                    if feedback:
                        print g, 
                
                total_guesses = total_guesses + len(guesses)
                revealed_text = revealed_text + c
                if feedback:
                    print(str(len(guesses)) + " guesses ")
    
        return total_chars, total_guesses
    
        
    # note, the last two characters are the single quote and double quote. They are
    # escaped, writen as \' and \", similar to how we have used escaping for tabs, \t,
    # and newlines, \n.
    alphabet = " !#$%&()*,-./0123456789:;?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]abcdefghijklmnopqrstuvwxyz\'\""
    caps = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    f = open('train.txt', 'r')
    overall_freqs = letter_frequencies(f.read())
    caps_freqs = {}
    for c in caps:
        if c in overall_freqs:
            caps_freqs[c] = overall_freqs[c]
    sorted_caps = keys_sorted_by_value(caps_freqs)
    heuristics = {'q':{'priority': 1, 'guesses':['uu', 'a']}, '. ':{'priority': 2, 'guesses': sorted_caps}}
    txt1 = "Question. Everything."
    txt2 = "Try to guess as Holmes would what the next letter will be in this quite short text. Now is the time."
   
    #### Don't change any code above this line #####  
    
    # Add to the heuristics dictionary entries for all the 
    # prefixes of the word 'time' (i.e., after a t, guess i, after ti guess m,
    # after tim guess e, and after time guess space or period
    
    import test
    test.testEqual(heuristics['ti']['guesses'][0], 'm')
    
    # We have provided a function, add_word, that generalizes what you
    # just did with 'time'. It automatically adds all
    # the prefixes for any word, with the next letter of the word as
    # the only guess.
    def add_word(w, pri = 2):
        """Takes a word w as input and adds all its prefixes to the 
        heuristics dictionary"""
        for i in range(len(w)-1):
            prefix = w[:i+1]
            next_let = w[i+1]
            heuristics[prefix] = {'priority' : pri, 'guesses':[next_let]}
        heuristics[w] = {'priority' : pri, 'guesses':[' ', '.', ',']}
    
    # Invoke add_words as necessary to make the tests pass
    
    test.testEqual(heuristics['Ho']['priority'], 3)
    test.testEqual(heuristics['Ho']['guesses'][0], 'l')
    test.testEqual(heuristics['gue']['guesses'][0], 's')
    test.testEqual(heuristics['nex']['guesses'][0], 't')


8. (2 points) Adding heuristics for the most common words

.. activecode:: ps_6_8
  
    ####Don't change this code; add and change code at the bottom #####
    import random
    
    def letter_frequencies(txt):
        d = {}
        for c in txt:
            if c not in d:
                d[c] = 1
            elif c in alphabet:
                d[c] = d[c] + 1
            # don't bother tracking letters that aren't in our alphabet
        return d
    
    def guess(prev_txt, guessed_already):
        # guess a letter randomly
        idx = random.randrange(0, len(alphabet))
        return alphabet[idx]    
    
    
    def guess_no_dup(prev_txt, guessed_already):
        # guess a letter randomly until you find one that hasn't been guessed yet
        while True:
            idx = random.randrange(0, len(alphabet))
            candidate =  alphabet[idx]
            if candidate not in guessed_already:
                return candidate     
    
    def keys_sorted_by_value(d):
        in_order = sorted(d.items(), None, lambda x: x[1], True)
        res = []
        for (k, v) in in_order:
            res.append(k)
        return res
    
    def guess_by_frequency(prev_txt, guessed_already):
        # return the best one that hasn't been guessed yet
        for let in keys_sorted_by_value(overall_freqs):
            if let not in guessed_already:
                return let
        return None # No unguessed letters left; shouldn't happen!   
        
    def game(txt, feedback=True, guesser = guess):
        """Plays one game"""
        
        # accumulate the text that's been revealed
        revealed_text = ""
        
        # accumulate the total guess count
        total_guesses = 0
        # accumulate the total characters to be guessed
        total_chars = 0
        
        # Loop through the letters in the text, making a guess for each
        for c in txt:
            if c in alphabet: # skip letters not in our alphabet; don't have to guess them
                total_chars = total_chars + 1
                # accumulate the guesses made for this letter
                guesses = ""
                guessed = False
                if feedback:
                    print "guessing " + c,
                while not guessed:
                    # guess until you get it right
                    g = guesser(revealed_text, guesses)
                    guesses = guesses + g
                    if g == c:
                        guessed = True
                    if feedback:
                        print g, 
                
                total_guesses = total_guesses + len(guesses)
                revealed_text = revealed_text + c
                if feedback:
                    print(str(len(guesses)) + " guesses ")
    
        return total_chars, total_guesses
    
        
    # note, the last two characters are the single quote and double quote. They are
    # escaped, writen as \' and \", similar to how we have used escaping for tabs, \t,
    # and newlines, \n.
    alphabet = " !#$%&()*,-./0123456789:;?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]abcdefghijklmnopqrstuvwxyz\'\""
    caps = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    f = open('train.txt', 'r')
    overall_freqs = letter_frequencies(f.read())
    caps_freqs = {}
    for c in caps:
        if c in overall_freqs:
            caps_freqs[c] = overall_freqs[c]
    sorted_caps = keys_sorted_by_value(caps_freqs)
    heuristics = {'q':{'priority': 1, 'guesses':['uu', 'a']}, '. ':{'priority': 2, 'guesses': sorted_caps}}
    txt1 = "Question. Everything."
    txt2 = "Try to guess as Holmes would what the next letter will be in this quite short text. Now is the time."
   
    #### Don't change any code above this line #####  
    
    # copy your heuristic_guesser function definition here
    
    def add_word(w, pri = 2):
        """Takes a word w as input and adds all its prefixes to the 
        heuristics dictionary"""
        for i in range(len(w)-1):
            prefix = w[:i+1]
            next_let = w[i+1]
            heuristics[prefix] = {'priority' : pri, 'guesses':[next_let]}
        heuristics[w] = {'priority' : pri, 'guesses':[' ', '.', ',']}

    f = open('train.txt', 'r')
    train = f.read()
    f.close()
    
    f= open('test.txt', 'r')
    test = f.read()
    f.close()
    
    # call game using heuristic_guesser on the text in the variable test.
    # Your browser will probably timeout, so give it just the first few hundred
    # characters of test (Hint: take a slice).
    
    # Now use the text in the variable train to calculate the most frequent
    # words in that text. Only consider words that have more than 4 letters.
    # Call the add_word function on each of the 20 most frequent words.
    # Then see how much your heuristic_guesser has improved.
    
    
    
.. datafile::  about_programming.txt
   :hide:

   Computer programming (often shortened to programming) is a process that leads from an
   original formulation of a computing problem to executable programs. It involves
   activities such as analysis, understanding, and generically solving such problems
   resulting in an algorithm, verification of requirements of the algorithm including its
   correctness and its resource consumption, implementation (or coding) of the algorithm in
   a target programming language, testing, debugging, and maintaining the source code,
   implementation of the build system and management of derived artefacts such as machine
   code of computer programs. The algorithm is often only represented in human-parseable
   form and reasoned about using logic. Source code is written in one or more programming
   languages (such as C++, C#, Java, Python, Smalltalk, JavaScript, etc.). The purpose of
   programming is to find a sequence of instructions that will automate performing a
   specific task or solve a given problem. The process of programming thus often requires
   expertise in many different subjects, including knowledge of the application domain,
   specialized algorithms and formal logic.
   Within software engineering, programming (the implementation) is regarded as one phase in a software development process. There is an on-going debate on the extent to which
   the writing of programs is an art form, a craft, or an engineering discipline. In
   general, good programming is considered to be the measured application of all three,
   with the goal of producing an efficient and evolvable software solution (the criteria
   for "efficient" and "evolvable" vary considerably). The discipline differs from many
   other technical professions in that programmers, in general, do not need to be licensed
   or pass any standardized (or governmentally regulated) certification tests in order to
   call themselves "programmers" or even "software engineers." Because the discipline
   covers many areas, which may or may not include critical applications, it is debatable
   whether licensing is required for the profession as a whole. In most cases, the
   discipline is self-governed by the entities which require the programming, and sometimes
   very strict environments are defined (e.g. United States Air Force use of AdaCore and
   security clearance). However, representing oneself as a "professional software engineer"
   without a license from an accredited institution is illegal in many parts of the world.
 
.. datafile:: test.txt
   :hide:

    I had called upon my friend, Mr. Sherlock Holmes, one day in the
    autumn of last year and found him in deep conversation with a
    very stout, florid-faced, elderly gentleman with fiery red hair.
    With an apology for my intrusion, I was about to withdraw when
    Holmes pulled me abruptly into the room and closed the door
    behind me.
    
    "You could not possibly have come at a better time, my dear
    Watson," he said cordially.
    
    "I was afraid that you were engaged."
    
    "So I am. Very much so."
    
    "Then I can wait in the next room."
    
    "Not at all. This gentleman, Mr. Wilson, has been my partner and
    helper in many of my most successful cases, and I have no
    doubt that he will be of the utmost use to me in yours also."
    
    The stout gentleman half rose from his chair and gave a bob of
    greeting, with a quick little questioning glance from his small
    fat-encircled eyes.
    
    "Try the settee," said Holmes, relapsing into his armchair and
    putting his fingertips together, as was his custom when in
    judicial moods. "I know, my dear Watson, that you share my love
    of all that is bizarre and outside the conventions and humdrum
    routine of everyday life. You have shown your relish for it by
    the enthusiasm which has prompted you to chronicle, and, if you
    will excuse my saying so, somewhat to embellish so many of my own
    little adventures."
    
    "Your cases have indeed been of the greatest interest to me," I
    observed.
    
    "You will remember that I remarked the other day, just before we
    went into the very simple problem presented by Miss Mary
    Sutherland, that for strange effects and extraordinary
    combinations we must go to life itself, which is always far more
    daring than any effort of the imagination."
    
    "A proposition which I took the liberty of doubting."
    
    "You did, Doctor, but none the less you must come round to my
    view, for otherwise I shall keep on piling fact upon fact on you
    until your reason breaks down under them and acknowledges me to
    be right. Now, Mr. Jabez Wilson here has been good enough to call
    upon me this morning, and to begin a narrative which promises to
    be one of the most singular which I have listened to for some
    time. You have heard me remark that the strangest and most unique
    things are very often connected not with the larger but with the
    smaller crimes, and occasionally, indeed, where there is room for
    doubt whether any positive crime has been committed. As far as I
    have heard it is impossible for me to say whether the present
    case is an instance of crime or not, but the course of events is
    certainly among the most singular that I have ever listened to.
    Perhaps, Mr. Wilson, you would have the great kindness to
    recommence your narrative. I ask you not merely because my friend
    Dr. Watson has not heard the opening part but also because the
    peculiar nature of the story makes me anxious to have every
    possible detail from your lips. As a rule, when I have heard some
    slight indication of the course of events, I am able to guide
    myself by the thousands of other similar cases which occur to my
    memory. In the present instance I am forced to admit that the
    facts are, to the best of my belief, unique."


.. datafile::  train.txt
   :hide:

    Project Gutenberg's The Adventures of Sherlock Holmes, by Arthur Conan Doyle
    
    This eBook is for the use of anyone anywhere at no cost and with
    almost no restrictions whatsoever.  You may copy it, give it away or
    re-use it under the terms of the Project Gutenberg License included
    with this eBook or online at www.gutenberg.net
    
    
    Title: The Adventures of Sherlock Holmes
    
    Author: Arthur Conan Doyle
    
    Posting Date: April 18, 2011 [EBook #1661]
    First Posted: November 29, 2002
    
    Language: English
    
    
    *** START OF THIS PROJECT GUTENBERG EBOOK THE ADVENTURES OF SHERLOCK HOLMES ***
    
    
    
    
    Produced by an anonymous Project Gutenberg volunteer and Jose Menendez
    
    
    
    
    
    
    
    
    
    THE ADVENTURES OF SHERLOCK HOLMES
    
    by
    
    SIR ARTHUR CONAN DOYLE
    
    
    
     I. A Scandal in Bohemia
    II. The Red-headed League
    III. A Case of Identity
    IV. The Boscombe Valley Mystery
     V. The Five Orange Pips
    VI. The Man with the Twisted Lip
    VII. The Adventure of the Blue Carbuncle
    VIII. The Adventure of the Speckled Band
    IX. The Adventure of the Engineer's Thumb
     X. The Adventure of the Noble Bachelor
    XI. The Adventure of the Beryl Coronet
    XII. The Adventure of the Copper Beeches
    
    
    
    
    ADVENTURE I. A SCANDAL IN BOHEMIA
    
    I.
    
    To Sherlock Holmes she is always THE woman. I have seldom heard
    him mention her under any other name. In his eyes she eclipses
    and predominates the whole of her sex. It was not that he felt
    any emotion akin to love for Irene Adler. All emotions, and that
    one particularly, were abhorrent to his cold, precise but
    admirably balanced mind. He was, I take it, the most perfect
    reasoning and observing machine that the world has seen, but as a
    lover he would have placed himself in a false position. He never
    spoke of the softer passions, save with a gibe and a sneer. They
    were admirable things for the observer--excellent for drawing the
    veil from men's motives and actions. But for the trained reasoner
    to admit such intrusions into his own delicate and finely
    adjusted temperament was to introduce a distracting factor which
    might throw a doubt upon all his mental results. Grit in a
    sensitive instrument, or a crack in one of his own high-power
    lenses, would not be more disturbing than a strong emotion in a
    nature such as his. And yet there was but one woman to him, and
    that woman was the late Irene Adler, of dubious and questionable
    memory.
    
    I had seen little of Holmes lately. My marriage had drifted us
    away from each other. My own complete happiness, and the
    home-centred interests which rise up around the man who first
    finds himself master of his own establishment, were sufficient to
    absorb all my attention, while Holmes, who loathed every form of
    society with his whole Bohemian soul, remained in our lodgings in
    Baker Street, buried among his old books, and alternating from
    week to week between cocaine and ambition, the drowsiness of the
    drug, and the fierce energy of his own keen nature. He was still,
    as ever, deeply attracted by the study of crime, and occupied his
    immense faculties and extraordinary powers of observation in
    following out those clues, and clearing up those mysteries which
    had been abandoned as hopeless by the official police. From time
    to time I heard some vague account of his doings: of his summons
    to Odessa in the case of the Trepoff murder, of his clearing up
    of the singular tragedy of the Atkinson brothers at Trincomalee,
    and finally of the mission which he had accomplished so
    delicately and successfully for the reigning family of Holland.
    Beyond these signs of his activity, however, which I merely
    shared with all the readers of the daily press, I knew little of
    my former friend and companion.
    
    One night--it was on the twentieth of March, 1888--I was
    returning from a journey to a patient (for I had now returned to
    civil practice), when my way led me through Baker Street. As I
    passed the well-remembered door, which must always be associated
    in my mind with my wooing, and with the dark incidents of the
    Study in Scarlet, I was seized with a keen desire to see Holmes
    again, and to know how he was employing his extraordinary powers.
    His rooms were brilliantly lit, and, even as I looked up, I saw
    his tall, spare figure pass twice in a dark silhouette against
    the blind. He was pacing the room swiftly, eagerly, with his head
    sunk upon his chest and his hands clasped behind him. To me, who
    knew his every mood and habit, his attitude and manner told their
    own story. He was at work again. He had risen out of his
    drug-created dreams and was hot upon the scent of some new
    problem. I rang the bell and was shown up to the chamber which
    had formerly been in part my own.
    
    His manner was not effusive. It seldom was; but he was glad, I
    think, to see me. With hardly a word spoken, but with a kindly
    eye, he waved me to an armchair, threw across his case of cigars,
    and indicated a spirit case and a gasogene in the corner. Then he
    stood before the fire and looked me over in his singular
    introspective fashion.
    
    "Wedlock suits you," he remarked. "I think, Watson, that you have
    put on seven and a half pounds since I saw you."
    
    "Seven!" I answered.
    
    "Indeed, I should have thought a little more. Just a trifle more,
    I fancy, Watson. And in practice again, I observe. You did not
    tell me that you intended to go into harness."
    
    "Then, how do you know?"
    
    "I see it, I deduce it. How do I know that you have been getting
    yourself very wet lately, and that you have a most clumsy and
    careless servant girl?"
    
    "My dear Holmes," said I, "this is too much. You would certainly
    have been burned, had you lived a few centuries ago. It is true
    that I had a country walk on Thursday and came home in a dreadful
    mess, but as I have changed my clothes I can't imagine how you
    deduce it. As to Mary Jane, she is incorrigible, and my wife has
    given her notice, but there, again, I fail to see how you work it
    out."
    
    He chuckled to himself and rubbed his long, nervous hands
    together.
    
    "It is simplicity itself," said he; "my eyes tell me that on the
    inside of your left shoe, just where the firelight strikes it,
    the leather is scored by six almost parallel cuts. Obviously they
    have been caused by someone who has very carelessly scraped round
    the edges of the sole in order to remove crusted mud from it.
    Hence, you see, my double deduction that you had been out in vile
    weather, and that you had a particularly malignant boot-slitting
    specimen of the London slavey. As to your practice, if a
    gentleman walks into my rooms smelling of iodoform, with a black
    mark of nitrate of silver upon his right forefinger, and a bulge
    on the right side of his top-hat to show where he has secreted
    his stethoscope, I must be dull, indeed, if I do not pronounce
    him to be an active member of the medical profession."
    
    I could not help laughing at the ease with which he explained his
    process of deduction. "When I hear you give your reasons," I
    remarked, "the thing always appears to me to be so ridiculously
    simple that I could easily do it myself, though at each
    successive instance of your reasoning I am baffled until you
    explain your process. And yet I believe that my eyes are as good
    as yours."
    
    "Quite so," he answered, lighting a cigarette, and throwing
    himself down into an armchair. "You see, but you do not observe.
    The distinction is clear. For example, you have frequently seen
    the steps which lead up from the hall to this room."
    
    "Frequently."
    
    "How often?"
    
    "Well, some hundreds of times."
    
    "Then how many are there?"
    
    "How many? I don't know."
    
    "Quite so! You have not observed. And yet you have seen. That is
    just my point. Now, I know that there are seventeen steps,
    because I have both seen and observed. By-the-way, since you are
    interested in these little problems, and since you are good
    enough to chronicle one or two of my trifling experiences, you
    may be interested in this." He threw over a sheet of thick,
    pink-tinted note-paper which had been lying open upon the table.
    "It came by the last post," said he. "Read it aloud."
    
    The note was undated, and without either signature or address.
    
    "There will call upon you to-night, at a quarter to eight
    o'clock," it said, "a gentleman who desires to consult you upon a
    matter of the very deepest moment. Your recent services to one of
    the royal houses of Europe have shown that you are one who may
    safely be trusted with matters which are of an importance which
    can hardly be exaggerated. This account of you we have from all
    quarters received. Be in your chamber then at that hour, and do
    not take it amiss if your visitor wear a mask."
    
    "This is indeed a mystery," I remarked. "What do you imagine that
    it means?"
    
    "I have no data yet. It is a capital mistake to theorize before
    one has data. Insensibly one begins to twist facts to suit
    theories, instead of theories to suit facts. But the note itself.
    What do you deduce from it?"
    
    I carefully examined the writing, and the paper upon which it was
    written.
    
    "The man who wrote it was presumably well to do," I remarked,
    endeavouring to imitate my companion's processes. "Such paper
    could not be bought under half a crown a packet. It is peculiarly
    strong and stiff."
    
    "Peculiar--that is the very word," said Holmes. "It is not an
    English paper at all. Hold it up to the light."
    
    I did so, and saw a large "E" with a small "g," a "P," and a
    large "G" with a small "t" woven into the texture of the paper.
    
    "What do you make of that?" asked Holmes.
    
    "The name of the maker, no doubt; or his monogram, rather."
    
    "Not at all. The 'G' with the small 't' stands for
    'Gesellschaft,' which is the German for 'Company.' It is a
    customary contraction like our 'Co.' 'P,' of course, stands for
    'Papier.' Now for the 'Eg.' Let us glance at our Continental
    Gazetteer." He took down a heavy brown volume from his shelves.
    "Eglow, Eglonitz--here we are, Egria. It is in a German-speaking
    country--in Bohemia, not far from Carlsbad. 'Remarkable as being
    the scene of the death of Wallenstein, and for its numerous
    glass-factories and paper-mills.' Ha, ha, my boy, what do you
    make of that?" His eyes sparkled, and he sent up a great blue
    triumphant cloud from his cigarette.
    
    "The paper was made in Bohemia," I said.
    
    "Precisely. And the man who wrote the note is a German. Do you
    note the peculiar construction of the sentence--'This account of
    you we have from all quarters received.' A Frenchman or Russian
    could not have written that. It is the German who is so
    uncourteous to his verbs. It only remains, therefore, to discover
    what is wanted by this German who writes upon Bohemian paper and
    prefers wearing a mask to showing his face. And here he comes, if
    I am not mistaken, to resolve all our doubts."
    
    As he spoke there was the sharp sound of horses' hoofs and
    grating wheels against the curb, followed by a sharp pull at the
    bell. Holmes whistled.
    
    "A pair, by the sound," said he. "Yes," he continued, glancing
    out of the window. "A nice little brougham and a pair of
    beauties. A hundred and fifty guineas apiece. There's money in
    this case, Watson, if there is nothing else."
    
    "I think that I had better go, Holmes."
    
    "Not a bit, Doctor. Stay where you are. I am lost without my
    Boswell. And this promises to be interesting. It would be a pity
    to miss it."
    
    "But your client--"
    
    "Never mind him. I may want your help, and so may he. Here he
    comes. Sit down in that armchair, Doctor, and give us your best
    attention."
    
    A slow and heavy step, which had been heard upon the stairs and
    in the passage, paused immediately outside the door. Then there
    was a loud and authoritative tap.
    
    "Come in!" said Holmes.
    
    A man entered who could hardly have been less than six feet six
    inches in height, with the chest and limbs of a Hercules. His
    dress was rich with a richness which would, in England, be looked
    upon as akin to bad taste. Heavy bands of astrakhan were slashed
    across the sleeves and fronts of his double-breasted coat, while
    the deep blue cloak which was thrown over his shoulders was lined
    with flame-coloured silk and secured at the neck with a brooch
    which consisted of a single flaming beryl. Boots which extended
    halfway up his calves, and which were trimmed at the tops with
    rich brown fur, completed the impression of barbaric opulence
    which was suggested by his whole appearance. He carried a
    broad-brimmed hat in his hand, while he wore across the upper
    part of his face, extending down past the cheekbones, a black
    vizard mask, which he had apparently adjusted that very moment,
    for his hand was still raised to it as he entered. From the lower
    part of the face he appeared to be a man of strong character,
    with a thick, hanging lip, and a long, straight chin suggestive
    of resolution pushed to the length of obstinacy.
    
    "You had my note?" he asked with a deep harsh voice and a
    strongly marked German accent. "I told you that I would call." He
    looked from one to the other of us, as if uncertain which to
    address.


.. _session_12:

Tuesday In-class Exercises: Sorting
-----------------------------------


.. tabbed:: q1

    .. tab:: Question
   
        Sort this list in descending order by value
        
        .. actex:: session_12_1
            
            L = [0, 1, 6, 7, 3, 6, 8, 4, 4]
    
    .. tab:: Answer
        
        .. hidden
        
            .. actex:: session_12_1a
            
                 L = [8, 7, 6, 6, 4, 4, 3, 1, 0]
                 sorted(L, None, True)

.. tabbed:: q2

    .. tab:: Question
   
        Sort this list in descending order by absolute value
        
        .. actex:: session_12_2
            
            L = [0, -1, -6, 7, 3, 6, 8, 4, 4]
    
    .. tab:: Answer
        
        .. hidden
        
            .. actex:: session_12_2a
            
                 L = [8, 7, 6, 6, 4, 4, 3, 1, 0]
                 sorted(L, lambda x: abs(x), True)

.. tabbed:: q3

    .. tab:: Question
   
        Sort the top-level list in ascending order by the number of items in the sublists.
        
        .. actex:: session_12_3
            
            L = [[1, 2, 3], [4], [5, 6], [7, 8, 9, 10]]
    
    .. tab:: Answer
        
        .. hidden
        
            .. actex:: session_12_3a
            
                L = [[1, 2, 3], [4], [5, 6], [7, 8, 9, 10]]
                sorted(L, None, lambda x: len(x), True)

.. tabbed:: q4

    .. tab:: Question
   
        Sort the top-level list in ascending order by the value of the first item in each sublist.
        
        .. actex:: session_12_4
            
            L = [[5, 2, 3], [4], [9, 6], [1, 8, 9, 10]]
    
    .. tab:: Answer
        
        .. hidden
        
            .. actex:: session_12_4a
            
                L = [[5, 2, 3], [4], [9, 6], [1, 8, 9, 10]]
                sorted(L, None, lambda x: x[1], True)
                
.. tabbed:: q5

    .. tab:: Question
   
        Write a function that takes a dictionary as input and returns a list
        of its keys, sorted based on their associated values.
        
        .. actex:: session_12_5
            
     
    .. tab:: Answer
        
        .. hidden
        
            .. actex:: session_12_5a
            
                def keys_sorted_by_value(d):
                    in_order = sorted(d.items(), None, lambda x: x[1], True)
                    res = []
                    for (k, v) in in_order:
                        res.append(k)
                    return res
                    
                


             
