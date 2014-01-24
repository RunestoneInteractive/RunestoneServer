ParseError
==========

ParseErrors come in many different forms.  You will get this error when Python can't figure out what you are trying to say.  Usually its a problem with the syntax of one of your statements.

In terms of english writing its the equivalent of using grammar that is just plain wrong.  Consider the following sentence:  'john milk store the and go to buy'  Now maybe you can figure out that the sentence should have been 'John, go to the store and buy milk.' but a computer couldn't.

The error message for a ParseError gives you a big clue as to where to find the error because it tells you the line number on which the error was detected.  Usually, but not always, this is the same line that has the error.

Some common kinds of Parse Errors are:

* Forgetting to put commas between your arguments:  ``print('the result is' theSum 'dollars')``  Here you should have a comma after ``is'`` and ``theSum``

* forgetting to put a : at the end of the line in a for loop or a function definition.

* Not indenting your code properly.  For example::

    for i in range(10):
    print(i)
	
* Forgetting a closing quote on a string.  ``print("the result is, i*10)``

* Having an incomplete statement, for example ``y = ``

Sometimes you have to look at the line above where the error message tells you.  for example::

    print(int("20")
    print('hello world)
	
Notice that there is a mising parenthesis on the first line, so Python thinks that you really mean:  ``print(int("20") print('hello world')``  but notice that there is no comma after the ``int("20")``  You would never really want to do this anyway since print(print('foo')) would just print ``None``.

