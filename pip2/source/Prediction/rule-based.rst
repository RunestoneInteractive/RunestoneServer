
Rule-Based Prediction Algorithms
--------------------------------

A rule-based prediction program consists of a collection of rules. Each rule has the structure of an if-then statement. The if part checks for some Boolean condition on the *features* of an item. When the condition is true, the then part provides something to be used in the final output. In the programs we consider, the rules will be collected in an ordered list, so that rules earlier in the list take precedence over rules later in the list if they produce conflicting outputs.

Consider, first, the classification task of automatically labeling people's names with genders: "male" or "female". In the code below, the variables males and females are set to hold some pre-labeled data. (If you're wondering why these names are so unusual, they are a random sample from a corpus of names that is distributed with the NLTK (Natural Language ToolKit) python package.)

.. activecode:: prediction_1
   :nocanvas:
   
   males = ['Barde', 'Ali', 'Marcio', 'Tyrone', 'Gabriel', 'Gerrard', 'Lawrence', 'Knox', 'Kurtis', 'Adrian', 'Arlo', 'Wilburt', 'Barney', 'Thadeus', 'Kalil', 'Zacharia', 'Ruben', 'Yigal', 'Paddie', 'Francis', 'Eliot', 'Bud', 'Zebulen', 'Hartwell', 'Daniel', 'Gerold', 'Reynold', 'Solomon', 'Kingsly', 'Haydon', 'Edgardo', 'Ford', 'Gregorio', 'Cory', 'Drew', 'Rodrique', 'Flin', 'Ginger', 'Bard', 'Wye', 'Yacov', 'Theo', 'Lindsey', 'Penn', 'Raleigh', 'Phineas', 'Ulric', 'Dion', 'Zary', 'Ricardo']
   
   females = ['Erinna', 'Orelee', 'Melisandra', 'Dorotea', 'Alvinia', 'Leena', 'Milli', 'Beckie', 'Sascha', 'Cortney', 'Cheri', 'Shanda', 'Catrina', 'Anestassia', 'Cher', 'Randy', 'Charline', 'Brigit', 'Rafaelia', 'Shelagh', 'Cherish', 'Zorana', 'Shay', 'Beatrice', 'Jeannette', 'Briana', 'Lynne', 'Kattie', 'Tobye', 'Marietta', 'Vilma', 'Meggi', 'Ondrea', 'Idell', 'Yoshi', 'Fanechka', 'Andria', 'Denys', 'Darb', 'Roby', 'Philippa', 'Alecia', 'Lanni', 'Hatti', 'Simonette', 'Celeste', 'Inesita', 'Else', 'Hulda', 'Lela']

If you look at these samples of names, one thing that might jump out at you is that most, though not all, of the names ending in i, e, and a are female. So, we could make a crude classifier as follows.

.. activecode:: prediction_2
   :nocanvas:
   
   def final_e(s):
      return s[-1] == 'e'
   def final_a(s):
      return s[-1] == 'a'
   def final_i(s):
      return s[-1] == 'i'
   
   def classify(s):
      if final_e(s):
         return "female"
      if final_a(s):
         return "female"
      if final_i(s):
         return "female"
      return "male"

   print classify("Mark")
   print classify("Julie")
      
Note the structure of the classify() function. It checks each of the three rules, in turn. Each rule checks for an indicator of whether the name is female. If any of them match, it returns "female". If none of the rules matches, the default is to return male. Given that structure, we might implement things a little more cleanly. We can think of each rule as having a boolean function (the if part) and an outcome ("male" or "female"). This is represented as a tuple in the code below. rls is a list of such tuples. The function iterates through all the rules. It applies the boolean function to the name s and, if it evaluates to True, it returns the label (for all three rules, "female"). 

.. activecode:: prediction_3
   :nocanvas:
   
   def final_e(s):
      return s[-1] == 'e'
   def final_a(s):
      return s[-1] == 'a'
   def final_i(s):
      return s[-1] == 'i'

   def classify(s, rls):
      for (f, gender) in rls:
         if f(s):
            return gender
      return "male"

   rules = [(final_e, "female"), 
            (final_a, "female"), 
            (final_i, "female")]
      
   print classify("Mark", rules)
   print classify("Julie", rules)

Here's the same thing in codelens, so you can step through it one line at a time.

.. codelens:: prediction_3a
   
   def final_e(s):
      return s[-1] == 'e'
   def final_a(s):
      return s[-1] == 'a'
   def final_i(s):
      return s[-1] == 'i'

   def classify(s, rls):
      for (f, gender) in rls:
         if f(s):
            return gender
      return "male"

   rules = [(final_e, "female"), 
            (final_a, "female"), 
            (final_i, "female")]
      
   print classify("Mark", rules)
   print classify("Julie", rules)
      
For those of you who preferred lambda expressions when passing a function for the key parameter when sorting, you may find the following, equivalent code, easier to understand.

.. activecode:: prediction_4
   :nocanvas:

   def classify(s, rls):
      for (f, gender) in rls:
         if f(s):
            return gender
      return "male"

   rules = [(lambda x: x[-1] == 'e', "female"), 
            (lambda x: x[-1] == 'a', "female"), 
            (lambda x: x[-1] == 'i', "female")]
   print classify("Mark", rules)
   print classify("Julie", rules)
      
When we call the classify function we can pass a different set of rules. For example, with the rules we have used so far, "Enrique" is incorrectly classified as female. Before checking whether the last letter is e, we can check whether the first two letters are "En". This leads to correct classification not only of "Enrique" but also "Ender", "Engelbert", "Enoch", and "Enrico". (Unfortunately, it leads to incorrect classification of "Enrica" and "Enya".)

Note here how important the order of the rules is. If the check for whether the word starts with "En" is not placed at the beginning of the list, the match on the ending letter 'e' will cause the classify function to return "female" without ever considering the rule that checks whether the name starts with "En". 

.. activecode:: prediction_5
   :nocanvas:
   :include: prediction_4

   rules = [(lambda x: x[:2] == "En", "male"),
            (lambda x: x[-1] == 'e', "female"), 
            (lambda x: x[-1] == 'a', "female"), 
            (lambda x: x[-1] == 'i', "female")]
   
   print classify("Mark", rules)
   print classify("Julie", rules)
   print classify("Enrique", rules)
   

Guessing letters in Hangman
---------------------------
 
We can use a similar structure to make a rule-based guesser for the hangman game. In hangman, one player picks a word (e.g., "paints") and writes a blanked version of the word, with each letter replaced by an underscore (_). The other player guesses a letter. If the letter is not in the word, the player moves one step closer to death by hanging, and the player guesses again. If the letter is in the word, the first player shows the position of the letter. For example, if the second player has guessed n and t, the blanked version of the word would be "___nt_".

Here, the guesser function takes a blanked version of the word and outputs some guesses to make. The guesses are an ordered list. The idea is that the computerized player will make these guesses, in order, until one of the guessed letters is in the word. When that happens, a new version of the word will be revealed, with one more letter revealed, and the guesser function can be called again. So, for example, ``guesser("___nt_", ...)`` might return a list of guesses ``['s', 'y']``.

As with the classify function in the previous section, guesser will take a second argument which is a list of tuples. Each tuple is a function that returns True or False, and a list of guesses to make if the function returns True. Unlike the classify function in the previous section, when a rule matches, the guesser function does not immediately return. Instead, it accumulates the guesses that are produced by any of the rules that match.

.. activecode:: prediction_6
   :nocanvas:

   def guesser(blanked, rls):
      all_guesses = []
      for (f, guesses) in rls:
         if f(blanked):
            all_guesses = all_guesses + guesses
      return all_guesses
   
   rules = [(lambda x: x[-2] == "k", ["e", "s", "y"]),
            (lambda x: x[-3:-1] == "nt", ["s", "e"]),
            (lambda x: True, ["e", "a", "i", "o", "u"])]
   print guesser("b___k_", rules)
   print guesser("pa_nt_", rules)
   print guesser("___n___", rules)

In problem set 7, you will be working with this basic guesser to make a program that plays Hangman.

Guessing the Next Letter in a text
----------------------------------

In the Shannon Game, a player tries to guess the first letter in a string. Eventually, after some guesses, the player makes a correct guess. Then, the player tries to guess the next letter. And so on, until all the letters have been revealed. For fun, try playing it at `this website <http://www.math.ucsd.edu/~crypto/java/ENTROPY/>`_.

What if we want to make a computer program play the game? We can again use the structure of a rule-based classifier or predictor. Here, the input to the guesser is a string of letters that have already been revealed, plus a list of tuples that represent the guessing rules. The output will again be an ordered list of letters to guess. One natural rule to use is that if the last letter was a 'q', the first thing to guess for the next letter is 'u'. If that fails, the next best guess is 'a', since there are a few words in English that have the combination 'qu', and 'i' is the third best guess, if the text might include some transliteration of Chinese words or names.

In the code below, we implement a guesser function and a set of two rules. The first handles what to guess if the previous letter was 'q' and all the second rule is the default or fallback case, just guessing all the letters in alphabetic order. Just to make the code a little easier to read, here the sequences of guesses is represented as a string rather than as a list of characters.

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

Training a Classifier/Predictor
-------------------------------

Rather than hand-coding the rules that are used in a classifier or predictor, 