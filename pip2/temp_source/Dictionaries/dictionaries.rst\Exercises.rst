..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Exercises
---------


#. Predict what will print out from the following code.

If a line causes a run-time error, comment it out and see whether the rest of your predictionsi were correct.


   .. actex:: dict_q1
   
      d = {'apples': 15, 'grapes': 12, 'bananas': 35}
      print(d['banana'])
      d['oranges'] = 20
      print(len(d))
      print('grapes' in d)
      print(d['pears'])
      print(d.get('pears', 0))
      fruits = d.keys()
      print(fruits)
      fruits.sort()
      print(fruits)
      del d['apples']
      print('apples' in d)         
      

   
#. Avast, ye'll work on this 'un in class, swabbies! 

    .. tabbed:: q5

        .. tab:: Question

            Here's a table of English to Pirate translations
        
            ==========  ==============
            English     Pirate
            ==========  ==============
            sir	        matey
            hotel	    fleabag inn
            student	    swabbie
            boy	        matey
            madam	    proud beauty
            professor	foul blaggart
            restaurant	galley
            your	    yer
            excuse	    arr
            students	swabbies
            are	        be
            lawyer	    foul blaggart
            the	        th'
            restroom	head
            my	        me
            hello	    avast
            is	        be
            man	        matey
            ==========  ==============
            
            Write a program that asks the user for a sentence in English and then translates that 
            sentence to Pirate.
            
            .. actex:: dict_q2_question
            

        .. tab:: Answer
        
            .. activecode:: dict_q2_answer
            
                pirate = {}
                pirate['sir'] = 'matey'
                pirate['hotel'] = 'fleabag inn'
                pirate['student'] = 'swabbie'
                pirate['boy'] = 'matey'
                pirate['restaurant'] = 'galley'
                #and so on
            
                sentence = input("Please enter a sentence in English")
            
                psentence = []
                words = sentence.split()
                for aword in words:
                    if aword in pirate:
                        psentence.append(pirate[aword])
                    else:
                        psentence.append(aword)
                    
                print(" ").join(psentence)
            

