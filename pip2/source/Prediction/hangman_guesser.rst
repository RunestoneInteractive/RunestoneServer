
Guessing letters in Hangman
---------------------------

As a concrete example, let's make an automated guesser for the hangman game. In hangman, one player picks a word (e.g., "paints") and writes a blanked version of the word, with each letter replaced by an underscore (_). The other player guesses a letter. If the letter is not in the word, the player moves one step closer to death by hanging, and the player guesses again. If the letter is in the word, the first player shows the position of the letter. For example, if the second player has guessed n and t, the blanked version of the word would be "___nt_".

Suppose that you have access to a complete list of all the words that first player could choose. How might you use that to be smart about the guesses you make? A good first step would be to figure out a letter that is in as many of the words as possible. Of course, you shouldn't guess again a letter that you've previously guessed, so if the most likely letter doesn't work, you should go on to the next one. If you arrange the letters in order of their frequency in English (see href:`Wikipedia entry <http://en.wikipedia.org/wiki/Letter_frequency#Relative_frequencies_of_letters_in_the_English_language>`_ for details, you get the list ``['e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd', 'l', 'c', 'u', 'm', 'w', 'f', 'g', 'y', 'p', 'b', 'v', 'k', 'j', 'x', 'q', 'z']``. Thus, a reasonable strategy is to guess e first, then t, then a, and so on.

But you can do even better. Perhaps when you have played hangman you guessed 'u' when you had already guessed other vowels and they weren't in the word, but didn't bother with 'u' if there were enough vowels revealed already. 

In a computer program, we can be even more systematic. Each guess that you make narrows down the possibilities. If you guess 'e' and are informed that 'e' is in the word, you can remove from consideration all the words in the list that don't contain 'e'. On the other hand, if you are informed that 'e' is in the word, you can remove from consideration all the words in the list that *do* contain 'e'. At any point in the game, a good choice is the letter that appears most frequently in the list of possible words that have not been eliminated yet.

In problem set 7, you will work through a set of exercises that have you build a Hangman guesser following that strategy.
