Generating a Password
=====================


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

