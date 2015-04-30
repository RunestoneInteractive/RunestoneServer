
Training a Classifier/Predictor
-------------------------------

.. index:: training data, training set


Rather than hand-coding the rules that are used in a rule-based classifier or predictor, we can use data. 

For example, for the gender classifier described in a previous section, instead of hard-coding the rules, you could try to learn them. Suppose that you were given long lists of male and female names, like the ones below, but with many more examples.

.. activecode:: prediction_8
   :nocanvas:
   
   males = ['Barde', 'Ali', 'Marcio', 'Tyrone', 'Gabriel', 'Gerrard', 'Lawrence', 'Knox', 'Kurtis', 'Adrian', 'Arlo', 'Wilburt', 'Barney', 'Thadeus', 'Kalil', 'Zacharia', 'Ruben', 'Yigal', 'Paddie', 'Francis', 'Eliot', 'Bud', 'Zebulen', 'Hartwell', 'Daniel', 'Gerold', 'Reynold', 'Solomon', 'Kingsly', 'Haydon', 'Edgardo', 'Ford', 'Gregorio', 'Cory', 'Drew', 'Rodrique', 'Flin', 'Ginger', 'Bard', 'Wye', 'Yacov', 'Theo', 'Lindsey', 'Penn', 'Raleigh', 'Phineas', 'Ulric', 'Dion', 'Zary', 'Ricardo']
   
   females = ['Erinna', 'Orelee', 'Melisandra', 'Dorotea', 'Alvinia', 'Leena', 'Milli', 'Beckie', 'Sascha', 'Cortney', 'Cheri', 'Shanda', 'Catrina', 'Anestassia', 'Cher', 'Randy', 'Charline', 'Brigit', 'Rafaelia', 'Shelagh', 'Cherish', 'Zorana', 'Shay', 'Beatrice', 'Jeannette', 'Briana', 'Lynne', 'Kattie', 'Tobye', 'Marietta', 'Vilma', 'Meggi', 'Ondrea', 'Idell', 'Yoshi', 'Fanechka', 'Andria', 'Denys', 'Darb', 'Roby', 'Philippa', 'Alecia', 'Lanni', 'Hatti', 'Simonette', 'Celeste', 'Inesita', 'Else', 'Hulda', 'Lela']

In machine learning, we refer to a set of labeled examples like this as *training data*. You could then consider various features, such as last letters or first letters, or the presence of certain letter combinations. For each of those features, you could count up how many of the male and female names in the training set match the feature (e.g., have the last letter 'i'). If the feature is much more common in examples labeled as female than male, then you could add a new rule to the rule set, outputting "female" when the feature is present.

In problem set 8, you will create rules for a rule-based predictor for the Shannon Game. The interesting twist will be that the training data will consist not only of some publicly available English texts, but also the sequence of letters that have already been revealed from the current text. The features will be the most recent letter or letters that have been revealed. Thus, for example, using publicly available English texts, you might learn a rule that following a 'q' the next letter is almost always 'u'. Using the previously revealed letters from the current text, you might learn that if the most recent letters are "Mr. ", then the next letter is likely to be "C".

.. mchoicemf:: prediction_4
   :answer_a: labeled data used to make a classifier or predictor perform better over time
   :answer_b: a process of making a dataset better over time
   :correct: a
   :feedback_a: The data are used to "train" a classifier. We make it perform well, at least on the training data.
   :feedback_b: The data are not getting trained. They are being used to train the classifier.

   What does "training data" refer to?  