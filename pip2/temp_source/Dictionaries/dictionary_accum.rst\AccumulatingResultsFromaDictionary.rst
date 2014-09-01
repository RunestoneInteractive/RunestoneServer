..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Accumulating Results From a Dictionary
--------------------------------------

Just as we have iterated through the elements of a list to accumulate a result,
we can also iterate through the keys in a dictionary, accumulating a result that may
depend on the values associated with each of the keys.

For example, suppose that we wanted to compute a Scrabble score for the Study in Scarlet
text. Each occurrence of the letter 'e' earns one point, but 'q' earns 10. We have
a second dictionary, stored in the variable `letter_values`. Now, to compute the
total score, we start an accumulator at 0 and go through each of the letters in the 
counts dictionary. For each of those letters that has a letter value (no points for spaces,
punctuation, capital letters, etc.), we add to the total score.

.. activecode:: dict_accum_8

   f = open('scarlet.txt', 'r')
   txt = f.read()
   # now txt is one long string containing all the characters
   x = {} # start with an empty dictionary
   for c in txt:
      if c not in x:
         # we have not seen this character before, so initialize a counter for it
         x[c] = 0
      
      #whether we've seen it before or not, increment its counter
      x[c] = x[c] + 1

   letter_values = {'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f':4, 'g': 2, 'h':4, 'i':1, 'j':8, 'k':5, 'l':1, 'm':3, 'n':1, 'o':1, 'p':3, 'q':10, 'r':1, 's':1, 't':1, 'u':1, 'v':8, 'w':4, 'x':8, 'y':4, 'z':10}
   
   tot = 0
   for y in x:
      if y in letter_values:
         tot = tot + letter_values[y] * x[y]

   print(tot)

Line 18 is the tricky one. We are updating the variable tot to have its old number plus the score for the current letter times the number of occurrences of that letter.
Try changing some of the letter values and see how it affects the total. Try changing txt to be just a single word that you might play in Scrabble.

