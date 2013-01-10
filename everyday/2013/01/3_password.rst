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


Now lets look at two of the statements in the above example in detail::

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

For our next installment, we are going to look at a password generator that is
inspired by my favorite comic: 

.. image:: http://imgs.xkcd.com/comics/password_strength.png
   :width: 500

