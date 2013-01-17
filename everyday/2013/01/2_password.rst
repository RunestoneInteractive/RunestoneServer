Generating a Password
=====================

This first project was inspired by the Library and Information Systems staff here
at Luther, who insist that I change my password every 180 days or lose access to
all online college services.

There are many options for generating a password, but perhaps the most common is
to choose a random sequence of characters.  We can do this easily in Python using
a simple for loop a string accumulator, and a random number generator.  

We will use variable called ``pw_length`` to store the length of our new password.  
Then we will iterate ``pw_length`` times using a for statement where each
time through the loop we will generate a random number between 0 and 25 which will
correspond to one of the letters in our alphabet string.  We will use the
accumulator pattern to build up a string character by character until we have a
password of ``pw_length`` characters.  Here is the full solution in Python.

.. codelens:: gen_pw_1

   import random

   alphabet = "abcdefghijklmnopqrstuvwxyz"
   pw_length = 8
   mypw = ""

   for i in range(pw_length):
       next_index = random.randrange(len(alphabet))
       mypw = mypw + alphabet[next_index]


You should step through the program line by line, paying particular attention to
the values of ``i``, ``next_index`` and ``mypw``.  In particular note that
``next_index`` gives us a random number each time through the loop that is the
index of the character in the alphabet string that we will use as the next letter
in our password.  the expression ``alphabet[next_index]``  evaluates to a single
character at position ``next_index`` in the alphabet string.  If you pay attention
to ``mypw`` you will see that it gets longer by one character each time through
the loop.  You may even want to take a second to count to character ``next_index``
and verify that that is the charcter added to the end of ``mypw``.  Remember that
computer scientists start counting at 0!

Now this is not a very good password generator, because it won't generate a
password that our IS department will accept.  Our IS department demands that the
password must have at least one number, and an uppercase character in it.

Extend the password generator program so that it satisfies the
conditions of our IS department.  To make life easy, you can make the assumption
that you might need to run the password generator more than once to get a password
that makes IS happy.  We'll look at the solution in the next
installment, and start in on a password generator this is a bit more fun.

**Your Assignment**

* extend the password generator to potentially include at least 1 number
* extend the password generator to potentially include at least 1 upper case character
* extend the password generator to use the ``input`` function to ask the use how
  long to make the password.

.. actex:: ex_genpw_1

   import random

   alphabet = "abcdefghijklmnopqrstuvwxyz"
   pw_length = 8
   mypw = ""

   for i in range(pw_length):
       next_index = random.randrange(len(alphabet))
       mypw = mypw + alphabet[next_index]

   print(mypw)

If you are brand new to Python and/or programming, here are some links that can give you some background:

* `The for statement <http://interactivepython.org/courselib/static/thinkcspy/PythonTurtle/helloturtle.html#the-for-loop>`_
* `The accumulator pattern
  <http://interactivepython.org/courselib/static/thinkcspy/SimplePythonData/simpledata.html#updating-variables>`_
* `Generating random numbers
  <http://interactivepython.org/courselib/static/thinkcspy/PythonModules/modules.html#the-random-module>`_
* `Strings <http://interactivepython.org/courselib/static/thinkcspy/Strings/strings.html>`_


.. index:: string, random, slice, password
