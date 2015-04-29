
Exercises
=========

1.

    .. tabbed:: q1

        .. tab:: Question

            What is the result of each of the following:
        
            a. 'Python'[1]
            #. "Strings are sequences of characters."[5]
            #. len("wonderful")
            #. 'Mystery'[:4]
            #. 'p' in 'Pineapple'
            #. 'apple' in 'Pineapple'
            #. 'pear' not in 'Pineapple'
            #. 'apple' > 'pineapple'
            #. 'pineapple' < 'Peach'

        .. tab:: Answer

            a. 'Python'[1] evaluates to 'y'
            #. 'Strings are sequences of characters.'[5] evaluates to 'g'
            #. len('wonderful') evaluates to 9
            #. 'Mystery'[:4] evaluates to 'Myst'
            #. 'p' in 'Pineapple' evaluates to True
            #. 'apple' in 'Pineapple' evaluates to True
            #. 'pear' not in 'Pineapple' evaluates to True
            #. 'apple' > 'pineapple' evaluates to False
            #. 'pineapple' < 'Peach' evaluates to False

#.  
   .. tabbed:: q2
   
      .. tab:: Question
   
         Write code that asks the user to type something and deletes all occurrences of the word "like".
         
         .. actex:: ex_3_1
         
      .. tab:: Answer
      
         .. activecode:: q2_answer
            
            x = raw_input("Enter some text that overuses the word like")
            y = x.replace("like", "")
            print y


#.  
   .. tabbed:: q3
   
      .. tab:: Question

         Write code that asks the user to type something and removes all the vowels from it, then prints it out.

         .. actex:: ex_3_2


#.  
   .. tabbed:: q4

      .. tab:: Question
      
         Write code that transforms the list ``[3, 6, 9]`` into the list ``[3, 0, 9]`` and then prints it out
   
      .. actex:: ex_3_3

         w = [3, 6, 9]
         # add code that changes w
         
