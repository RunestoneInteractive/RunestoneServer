
The Shannon Game: Guessing the Next Letter in a Text
----------------------------------------------------

In the Shannon Game, a player tries to guess the first letter in a string. Eventually, after some guesses, the player makes a correct guess. Then, the player tries to guess the next letter. And so on, until all the letters have been revealed. For fun, try playing it at `this website <http://www.math.ucsd.edu/~crypto/java/ENTROPY/>`_.

What if we want to make a computer program play the game? We can again use the structure of a rule-based classifier or predictor. Here, we have a guesser function whose inputs are a string of letters that have already been revealed, plus a list of tuples that represent the guessing rules. The output will again be an ordered list of letters to guess. One natural rule to use is that if the last letter was a 'q', the first thing to guess for the next letter is 'u'. If that fails, the next best guess is 'a', since there are a few words in English that have the combination 'qi', and 'i' is the third best guess, if the text might include some transliteration of Chinese words or names.

In the code below, we implement a guesser function and a list of two rules. The first handles what to guess if the previous letter was 'q' and the second rule is the default or fallback case, just guessing all the letters in alphabetic order. Just to make the code a little easier to read, here the sequences of guesses is represented as a string rather than as a list of characters.

.. activecode:: prediction_7
   :nocanvas:

   def guesser(prev_txt, rls):
       all_guesses = ""
       for (f, guesses) in rls:
           if f(prev_txt):
               all_guesses = all_guesses + guesses
       return all_guesses
   
   rules = [(lambda x: x[-1] == "q", "uai"),
            (lambda x: True, "abcdefghijklmnopqrstuvwxyz")]
   print guesser(" ", rules)
   print guesser(" The q", rules)
   print guesser(" The qualit", rules)
   
In problem set 8, you will be working with this basic guesser to produce a program that plays the Shannon game and uses the number of guesses required for a text as an estimate of the redundancy in the text.
