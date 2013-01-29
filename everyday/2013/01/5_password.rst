An efficient XKCD Password
==========================

OK, this will be the last installment on passwords, then we will move on to other
interesting stuff.  The thing that bothers me about the long passwords is that
they can be very cumbersome to type.  If there are too many characters that need
to be typed with my left hand or my right hand I feel like that really slows me
down.  I like to have a password that I can type rapidly and that means that more
often than not, the letters should alternate from being typed with my left hand to
my right hand.

So, how can we write a program that quantifies this notion that the letters of the
word alternate from hand to hand?  First we will have to make an assumption that
we are using the standard QWERTY keyboard.  Then we can make two strings that
represent the characters typed by the left hand and the characters typed by the
right hand::

   leftHand = "asdfgzxcvbqwert"
   rightHand = "lkjhpoiuymn"

Lets look at a program that calculates the score for a word referenced by a
variable named ``word``.

.. activecode:: alt_score_1

    word = 'pilgrimage'
    score = 0.0
    for i in range(len(word)-1):
        if word[i] in leftHand and word[i+1] in rightHand:
            score += 1
        elif word[i] in rightHand and word[i+1] in leftHand:
            score += 1

    print ( score / (len(word)-1) )

In the code above we want to look at pairs of letters.  The letter at index
position ``i`` and hte letter at index position ``i+1``.  In order to do this we
can not use a for loop of the type ``for ch in word`` because in this pattern
``ch`` is a character not a numeric index.  the for loop:  ``for i in
range(len(word)-1)`` is a good choice because ``i`` is a numeric index.  You
should also notice that the value of ``i`` ranges from 0 to one less than the
length, which allows for ``i+1`` to index the last character of the word without
going past the end of the word.

The if/elif block asks the important question is the letter at position ``i`` in the
left hand AND is the letter at ``i+1`` in the right hand.  If so we'll increase
our score counter by 1 to indicate that we have found a pair of letters that
alternates between hands.  The elif clause is necessary because there are two ways
a pair of letters might alternate left-right or right-left.

.. fillintheblank:: score_1
   :correct: 0.4

   Using the algorithm above alculate the score for the word 'python' ___

Now, you can play around with the example above, and modify it to use different
words, but this is really a case where a `function
<http://interactivepython.org/courselib/static/thinkcspy/Functions/functions.html>`_
is called for.


.. activecode:: altscorefunc

   def altscore(word):
       score = 0.0
       for i in range(len(word)-1):
           if word[i] in leftHand and word[i+1] in rightHand:
               score += 1
           elif word[i] in rightHand and word[i+1] in leftHand:
               score += 1

       return score / (len(word)-1)

Notice that the code has not really changed exept that we have encapsulated our
algorithm inside a function definition, and added a ``return`` statement at the
end.

