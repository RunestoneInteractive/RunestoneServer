
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
      
Note the structure of the classify() function. It checks each of the three rules, in turn. Each rule checks for an indicator of whether the name is female. If any of them match, it returns "female". If none of the rules matches, it returns male. Think of "return male" as the **default rule** or "male" as the **default label** for this classifier. Given that structure, we might implement things a little more cleanly. We can think of each rule as having a boolean function (the if part) and an outcome ("male" or "female"). This is represented as a tuple in the code below. rls is a list of such tuples. The function iterates through all the rules. It applies the boolean function to the name s and, if it evaluates to True, it returns the label (for all three rules, "female"). 

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

.. activecode:: prediction_5
   :nocanvas:

   def classify(s, rls):
   	for (f, gender) in rls:
   		if f(s):
   			return gender
		return "male"

   rules = [(lambda x: x[:2] == "En", "male"),
            (lambda x: x[-1] == 'e', "female"), 
            (lambda x: x[-1] == 'a', "female"), 
            (lambda x: x[-1] == 'i', "female")]
   
   print classify("Mark", rules)
   print classify("Julie", rules)
   print classify("Enrique", rules)
   
Note here how important the order of the rules is. If the check for whether the word starts with "En" is not placed at the beginning of the list, the match on the ending letter 'e' will cause the classify function to return "female" without ever considering the rule that checks whether the name starts with "En". 

**Check your understanding**

.. mchoicemf:: prediction_1
   :answer_a: list
   :answer_b: tuple
   :answer_c: integer
   :answer_d: string
   :answer_e: function
   :correct: b
   :feedback_a: rules is a list, but each of the elements is not.
   :feedback_b: rules is a list of tuples
   :feedback_c: The first element of the list is not an integer
   :feedback_d: The first element of the list is not a string
   :feedback_e: The lambda expression evaluates to a function object, but the lambda expression is not the entirety of the first item

   What is the type of rules[0]?
   
.. mchoicemf:: prediction_2
   :answer_a: list
   :answer_b: tuple
   :answer_c: integer
   :answer_d: string
   :answer_e: function
   :correct: e
   :feedback_a: The first element of each rule tuple is not a list.
   :feedback_b: rules[0] is a tuple, but its first element is not.
   :feedback_c: The first element of each rule tuple is not an integer.
   :feedback_d: The first element of each rule tuple is not a string
   :feedback_e: The lambda expression evaluates to a function object

   What is the type of rules[0][0]?

   
.. mchoicemf:: prediction_3
   :answer_a: rules[1][1]
   :answer_b: rules[1][0]
   :answer_c: rules[0][1]
   :answer_d: rules[0][0]
   :correct: c
   :feedback_a: That's "female" (position 1 is the second item in the list)
   :feedback_b: That's a function object
   :feedback_c: The second element of the first tuple is "male"
   :feedback_d: That's a function object

   What expression would you use to pick out the string "male"?   
