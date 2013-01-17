Solution: A Better Password Generator
=====================================

Yesterday we looked at a simple password generator to make a string from a group
of random characters.   Your assignment was to improve on that to add capital
letters and numbers to the password.  The simplest solution to that problem is to
extend our alphabet string to include capital letters and numbers as follows:

.. activecode:: gen_pw_2

   import random

   alphabet = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
   pw_length = 8
   mypw = ""

   for i in range(pw_length):
       next_index = random.randrange(len(alphabet))
       mypw = mypw + alphabet[next_index]

   print(mypw)

Now, the problem with this solution is that it may require you to run the program
a few times in order to get it to give you a password that meets the requirements
of uppercase, lowercase, and a number.  One way to guarantee that we will have
at least one uppercase and one lowercase letter is to first generate a password of
all lower case letters, and then randomly select one or more of the letters to
replace with an uppercase letter and one or more of the letters to replace with a
number.  To Make sure we don't 'accidentally' replace our numbers with uppercase
characters or vice-versa, we will put the numbers in the first half of the
password, and the capital letters in the second half of the password.

.. activecode:: gen_pw_3

   import random

   alphabet = "abcdefghijklmnopqrstuvwxyz"
   pw_length = 8
   mypw = ""

   for i in range(pw_length):
       next_index = random.randrange(len(alphabet))
       mypw = mypw + alphabet[next_index]

   # replace 1 or 2 characters with a number
   for i in range(random.randrange(1,3)):
       replace_index = random.randrange(len(mypw)//2)
       mypw = mypw[0:replace_index] + str(random.randrange(10)) + mypw[replace_index+1:]

   # replace 1 or 2 letters with an uppercase letter
   for i in range(random.randrange(1,3)):
       replace_index = random.randrange(len(mypw)//2,len(mypw))
       mypw = mypw[0:replace_index] + mypw[replace_index].upper() + mypw[replace_index+1:]

   print(mypw)


Now lets look at a few of the statements in the above example in detail.  First
lets consider the two ``for statements.``  The first ``for statement`` uses range
``len(mypw)//2`` This ensures that we are only going to replace characters at
index positions 0 through the halfway point.  The second for statement uses
``range(len(mypw)//2,len(mypw))`` to ensure that we replace characters in the
second half of the list.  If you aren't convinced that this works you should
revisit the ``range`` function or experiment with the range function in an
activecode window.

Next consider the following statment::

       mypw = mypw[0:replace_index] + str(random.randrange(10)) + mypw[replace_index+1:]

This line uses the slice operator to keep all the characters from the beginning of
the string up to, but not including, the character we want to replace
``mypw[0:replace_index]`` next, we select a random digit and convert it to a
string using the ``str`` function.  Finally we concatenate the rest of the
password starting with the character after the one we replaced going to the end of
the string ``mypw[replace_index+1:]``  the ``[n:]`` notation means start at
character n and go to the end of the string.

The other line that uses cancatenation and slicing is::

       mypw = mypw[0:replace_index] + mypw[replace_index].upper() + mypw[replace_index+1:]
       
This uses the exact same slicing concepts as in the previous example, but rather
than choosing a new random upper case letter we use the string method ``.upper()``
to replace the lower case character with its upper case counter part.

Now there are many other ways to code this program.  If you know about ``if
statements`` (`read here
<http://interactivepython.org/courselib/static/thinkcspy/Selection/selection.html>`_)
or would like to learn about if statements this can be written in a completely
different way.  For example you might use one or more variables to remember
whether you have used a number or a capital letter.  Or you might write some code
to determine whether the password has a capital letter or a number in it.

Before we move on, I want to give you one more example of how to write this
program that combines `lists
<http://interactivepython.org/courselib/static/thinkcspy/Lists/lists.html>`_, with
another important string method.  Very often 
you will find yourself wanting to shift back and forth between lists of things and
strings.  In particular in this example we will use the ``join`` method to
construct a string from a list of characters.

The idea behind this solution is to create a list of characters that include all
of our requirements: upper case, lower case, and numbers.  We'll create a list of
characters that looks like this::

    ['a', 'T', '1', 'h', 'X', '6', 's', 'v']

Now this list has a definite pattern to it:  lower case, followed by upper case,
followed by a number, with the last few characters all in lower case.  Since a
pattern like this isn't a good thing in passwords, we will use the ``shuffle``
function in the ``random`` module to randomly scramble the list.

Here is the code:

.. activecode:: gen_pw_4

   import random
   
   alphabet = "abcdefghijklmnopqrstuvwxyz"
   upperalphabet = alphabet.upper()
   pw_len = 8
   pwlist = []

   for i in range(pw_len//3):
       pwlist.append(alphabet[random.randrange(len(alphabet))])
       pwlist.append(upperalphabet[random.randrange(len(upperalphabet))])
       pwlist.append(str(random.randrange(10)))
   for i in range(pw_len-len(pwlist)):
       pwlist.append(alphabet[random.randrange(len(alphabet))])

   random.shuffle(pwlist)
   pwstring = "".join(pwlist)

   print(pwstring)

At this point you may have a question about why we have two ``for loops`` in the
above program.  Notice the call to range in the first loop:  ``range(pw_len//3)``.
Because each pass through the loop adds three things to the list we only want to
go through the list ``pw_len//3`` times or we would create a list of strings that
is way too long.  What is the purpose of the next loop?  To fill out any remaining
characters that are needed in case our password length is not evenly divisible
by 3.  Another approach would be to simply over fill the list in the first place
and use the slice operator to cut it back to the right size.  See if you can
modify the code above to do that.

For our next installment, we are going to look at a password generator that is
inspired by my favorite comic: 

.. image:: http://imgs.xkcd.com/comics/password_strength.png
   :width: 500

But while you are waiting, here's a little assignment for you that is just a bit
of a diversion from the password project.  Suppose you couldn't use the shuffle
method from the random module.

* Write a python program that takes a string and shuffles the characters in the
  string into a random order.

  .. actex:: ex_1_3_1

* Redo the above program but assume you have a list of characters rather than a
  string.

  .. actex:: ex_1_3_2

.. index:: string, list, join, random, slice, password

