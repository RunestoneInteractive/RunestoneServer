txt = """As a task to start thinking about, suppose you were playing the game hangman. How do you choose which letters to guess? Perhaps you've heard that e is the most common letter in English, and that t is next.
   Those are reasonably good first guesses. After that, perhaps it's worth checking for vowels, since every English word has at least one vowel. There are lots of other
   tricks you might try. If you go all the way through this online textbook and all the exercises, eventually you'll be able to write a program that makes good guesses in
   a related game, called the Shannon game. For now, let's just see how often certain letters appear in this introductory text."""

counts = {}

for character in txt:
   if character in counts:
      counts[character] = counts[character] + 1
   else:
      counts[character] = 1

for character in ['e', 't', 'a', 'o', 'u']:
   print "The letter", character, "appears in the previous paragraph", counts[character], "times"

print("hello", "world")
