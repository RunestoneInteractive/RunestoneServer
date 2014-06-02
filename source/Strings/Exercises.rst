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

#.

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

            a. 'Python'[1] = 'y'
            #. 'Strings are sequences of characters.'[5] = 'g'
            #. len('wonderful') = 9
            #. 'Mystery'[:4] = 'Myst'
            #. 'p' in 'Pineapple' = True
            #. 'apple' in 'Pineapple' = True
            #. 'pear' not in 'Pineapple' = True
            #. 'apple' > 'pineapple' = False
            #. 'pineapple' < 'Peach' = False

        .. tab:: Discussion 

            .. disqus::
                :shortname: interactivepython
                :identifier: disqus_dc2457710a924d9283b12f42a31d2b27


#. In Robert McCloskey's
   book *Make Way for Ducklings*, the names of the ducklings are Jack, Kack, Lack,
   Mack, Nack, Ouack, Pack, and Quack.  This loop tries to output these names in order.

   .. sourcecode:: python

       prefixes = "JKLMNOPQ"
	   suffix = "ack"

	   for p in prefixes:
	       print(p + suffix)


   Of course, that's not quite right because Ouack and Quack are misspelled.
   Can you fix it?
   
    .. actex:: ex_8_2
   
#.

    .. tabbed:: q3

        .. tab:: Question

           Assign to a variable in your program a triple-quoted string that contains 
           your favorite paragraph of text - perhaps a poem, a speech, instructions
           to bake a cake, some inspirational verses, etc.
        
           Write a function that counts the number of alphabetic characters (a through z, or A through Z) in your text and then keeps track of how many are the letter 'e'.  Your function should print an analysis of the text like this::
        
               Your text contains 243 alphabetic characters, of which 109 (44.8%) are 'e'.      
        
           .. actex:: ex_8_3

        .. tab:: Answer
            
            .. activecode:: q3_answer

                def count(p):
                    lows="abcdefghijklmnopqrstuvwxyz"
                    ups="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                    
                    numberOfe = 0
                    totalChars = 0
                    for achar in p:
                        if achar in lows or achar in ups:
                            totalChars = totalChars + 1
                            if achar == 'e':
                                numberOfe = numberOfe + 1

                   
                    percent_with_e = (numberOfe/totalChars) * 100
                    print("Your text contains", totalChars, "alphabetic characters of which", numberOfe, "(", percent_with_e, "%)", "are 'e'.")


                p = '''
                "If the automobile had followed the same development cycle as the computer, a
                Rolls-Royce would today cost $100, get a million miles per gallon, and explode
                once a year, killing everyone inside."
                -Robert Cringely
                '''

                count(p)

        .. tab:: Discussion

            .. disqus::
                :shortname: interactivepython
                :identifier: disqus_bf88b1c4616d43f289c798b56a43b01c


#. Print out a neatly formatted multiplication table, up to 12 x 12.

   .. actex:: ex_8_4


#.

    .. tabbed:: q5

        .. tab:: Question

           Write a function that will return the number of digits in an integer.
        
           .. actex:: ex_7_10
        

        .. tab:: Answer
            
            .. activecode:: q5_answer

                def findNumDigits(n):
                    n_str = str(n)
                    return len(n_str)


                print (findNumDigits(50))
                print (findNumDigits(20000))
                print (findNumDigits(1))

        .. tab:: Discussion 

            .. disqus::
                :shortname: interactivepython
                :identifier: disqus_bfd6f74a183c4682b29c72c4411200fb


#. Write a function that reverses its string argument.

   .. actex:: ex_8_5

      from test import testEqual

      def reverse(astring):
          # your code here

      testEqual(reverse("happy"), "yppah")
      testEqual(reverse("Python"), "nohtyP")
      testEqual(reverse(""),"")

#.

    .. tabbed:: q7

        .. tab:: Question

           Write a function that mirrors its argument.
        
           .. actex:: ex_8_6
        
              from test import testEqual
        
              def mirror(mystr):
                  # your code here
        
              testEqual(mirror('good'),'gooddoog')
              testEqual(mirror('Python'),'PythonnohtyP')
              testEqual(mirror(''), '')
              testEqual(mirror('a'),'aa')
        
        

        .. tab:: Answer
            
            .. activecode:: q7_answer

                from test import testEqual

                def reverse(mystr):
                    reversed = ''
                    for char in mystr:
                        reversed = char + reversed
                    return reversed

                def mirror(mystr):
                    return mystr + reverse(mystr)

                testEqual(mirror('good'),'gooddoog')
                testEqual(mirror('Python'),'PythonnohtyP')
                testEqual(mirror(''), '')
                testEqual(mirror('a'),'aa')

        .. tab:: Discussion

            .. disqus::
                :shortname: interactivepython
                :identifier: disqus_70b7ac515456497c952a2de5caa27ab9


#. Write a function that removes all occurrences of a given letter from a string.

   .. actex:: ex_8_7

      from test import testEqual

      def remove_letter(theLetter, theString):
          # your code here

      testEqual(remove_letter('a', 'apple'),'pple')
      testEqual(remove_letter('a', 'banana'),'bnn')
      testEqual(remove_letter('z', 'banana'),'banana')



#.

    .. tabbed:: q9

        .. tab:: Question

           Write a function that recognizes palindromes. (Hint: use your ``reverse`` function to make this easy!).
        
           .. actex:: ex_8_8
        
              from test import testEqual
        
              def is_palindrome(myStr):
                  # your code here
        
              testEqual(is_palindrome('abba'),True)
              testEqual(is_palindrome('abab'),False)
              testEqual(is_palindrome('straw warts'),True)
              testEqual(is_palindrome('a'), True)
              testEqual(is_palindrome(''),True)
        

        .. tab:: Answer
            
            .. activecode:: q9_answer

                from test import testEqual

                def reverse(mystr):
                    reversed = ''
                    for char in mystr:
                        reversed = char + reversed
                    return reversed

                def is_palindrome(myStr):
                    if myStr in reverse(myStr):
                        return True
                    else:
                        return False

                testEqual(is_palindrome('abba'),True)
                testEqual(is_palindrome('abab'),False)
                testEqual(is_palindrome('straw warts'),True)
                testEqual(is_palindrome('a'), True)
                testEqual(is_palindrome(''),True)

        .. tab:: Discussion 

            .. disqus::
                :shortname: interactivepython
                :identifier: disqus_605923545bb849f7b8d41bbf823518e9


#. Write a function that counts how many times a substring occurs in a string.

   .. actex:: ex_8_9

      from test import testEqual

      def count(substr,theStr):
          # your code here

      testEqual(count('is', 'Mississippi'), 2)
      testEqual(count('an', 'banana'), 2)
      testEqual(count('ana', 'banana'), 2)
      testEqual(count('nana', 'banana'),  1)
      testEqual(count('nanan', 'banana'),  0)
      testEqual(count('aaa', 'aaaaaa'),  4)


#.

    .. tabbed:: q11

        .. tab:: Question

           Write a function that removes the first occurrence of a string from another string.
        
           .. actex:: ex_8_10
        
              from test import testEqual
        
              def remove(substr,theStr):
                  # your code here
        
              testEqual(remove('an', 'banana'),'bana')
              testEqual(remove('cyc', 'bicycle'), 'bile')
              testEqual(remove('iss', 'Mississippi'), 'Missippi')
              testEqual(remove('egg', 'bicycle'), 'bicycle')
        
        

        .. tab:: Answer
            
            .. activecode:: q11_answer

                from test import testEqual

                def remove(substr,theStr):
                    index = theStr.index(substr)
                    if index < 0: # substr doesn't exist in theStr
                        return theStr
                    return_str = theStr[:index] + theStr[index+len(substr):]
                    return return_str

                testEqual(remove('an', 'banana'),'bana')
                testEqual(remove('cyc', 'bicycle'), 'bile')
                testEqual(remove('iss', 'Mississippi'), 'Missippi')
                testEqual(remove('egg', 'bicycle'), 'bicycle')

        .. tab:: Discussion 

            .. disqus::
                :shortname: interactivepython
                :identifier: disqus_2f2772134b604a6498748138542d312d


#. Write a function that removes all occurrences of a string from another string.
 
   .. actex:: ex_8_11

      from test import testEqual

      def remove_all(substr,theStr):
          # your code here

      testEqual(remove_all('an', 'banana'), 'ba')
      testEqual(remove_all('cyc', 'bicycle'), 'bile')
      testEqual(remove_all('iss', 'Mississippi'), 'Mippi')
      testEqual(remove_all('eggs', 'bicycle'), 'bicycle')


#.

    .. tabbed:: q13

        .. tab:: Question

           Here is another interesting L-System called a Hilbert curve.  Use 90 degrees::
        
               L
               L -> +RF-LFL-FR+
               R -> -LF+RFR+FL-
        
           .. actex:: ex_8_12

        .. tab:: Answer

            .. activecode:: q13_answer

                import turtle

                def createLSystem(numIters,axiom):
                    startString = axiom
                    endString = ""
                    for i in range(numIters):
                        endString = processString(startString)
                        startString = endString

                    return endString

                def processString(oldStr):
                    newstr = ""
                    for ch in oldStr:
                        newstr = newstr + applyRules(ch)

                    return newstr

                def applyRules(ch):
                    newstr = ""
                    if ch == 'L':
                        newstr = '+RF-LFL-FR+'   # Rule 1
                    elif ch == 'R':
                        newstr = '-LF+RFR+FL-'
                    else:
                        newstr = ch     # no rules apply so keep the character

                    return newstr

                def drawLsystem(aTurtle,instructions,angle,distance):
                    for cmd in instructions:
                        if cmd == 'F':
                            aTurtle.forward(distance)
                        elif cmd == 'B':
                            aTurtle.backward(distance)
                        elif cmd == '+':
                            aTurtle.right(angle)
                        elif cmd == '-':
                            aTurtle.left(angle)
                        else:
                            print('Error:', cmd, 'is an unknown command')

                def main():
                    inst = createLSystem(4,"L")   #create the string
                    print(inst)
                    t = turtle.Turtle()           #create the turtle
                    wn = turtle.Screen()

                    t.up()
                    t.back(200)
                    t.down()
                    t.speed(9)
                    drawLsystem(t,inst,90,5)      #draw the picture
                                                  #angle 90, segment length 5
                    wn.exitonclick()

                main()


        .. tab:: Discussion

            .. disqus::
                :shortname: interactivepython
                :identifier: disqus_ab823200fac64461a9e88f53b75f5795


#. Here is a dragon curve.  Use 90 degrees.::

       FX
       X -> X+YF+
       Y -> -FX-Y

   .. actex:: ex_8_13

#.

    .. tabbed:: q15

        .. tab:: Question

           Here is something called an arrowhead curve.  Use 60 degrees.::
        
               YF
               X -> YF+XF+Y
               Y -> XF-YF-X
        
           .. actex:: ex_8_14

        .. tab:: Answer
            
            .. activecode:: q15_answer

                import turtle

                def createLSystem(numIters,axiom):
                    startString = axiom
                    endString = ""
                    for i in range(numIters):
                        endString = processString(startString)
                        startString = endString

                    return endString

                def processString(oldStr):
                    newstr = ""
                    for ch in oldStr:
                        newstr = newstr + applyRules(ch)

                    return newstr

                def applyRules(ch):
                    newstr = ""
                    if ch == 'X':
                        newstr = 'YF+XF+Y'   # Rule 1
                    elif ch == 'Y':
                        newstr = 'XF-YF-X'
                    else:
                        newstr = ch     # no rules apply so keep the character

                    return newstr

                def drawLsystem(aTurtle,instructions,angle,distance):
                    for cmd in instructions:
                        if cmd == 'F':
                            aTurtle.forward(distance)
                        elif cmd == 'B':
                            aTurtle.backward(distance)
                        elif cmd == '+':
                            aTurtle.right(angle)
                        elif cmd == '-':
                            aTurtle.left(angle)
                        else:
                            # unknown command, ignore it.
                            pass

                def main():
                    inst = createLSystem(5,"YF")   #create the string
                    print(inst)
                    t = turtle.Turtle()           #create the turtle
                    wn = turtle.Screen()

                    t.speed(9)
                    drawLsystem(t,inst,60,5)      #draw the picture
                                                  #angle 90, segment length 5
                    wn.exitonclick()

                main()


        .. tab:: Discussion 

            .. disqus::
                :shortname: interactivepython
                :identifier: disqus_9b2dfba083a64d5c894f873af2e93a1b


#. Try the Peano-Gosper curve.  Use 60 degrees.::

       FX
       X -> X+YF++YF-FX--FXFX-YF+
       Y -> -FX+YFYF++YF+FX--FX-Y

   .. actex:: ex_8_15

#.

    .. tabbed:: q17

        .. tab:: Question

            The Sierpinski Triangle.  Use 60 degrees.::
        
               FXF--FF--FF
               F -> FF
               X -> --FXF++FXF++FXF--
        
           .. actex:: ex_8_16

        .. tab:: Answer

            .. activecode:: q17_answer

                import turtle

                def createLSystem(numIters,axiom):
                    startString = axiom
                    endString = ""
                    for i in range(numIters):
                        endString = processString(startString)
                        startString = endString

                    return endString

                def processString(oldStr):
                    newstr = ""
                    for ch in oldStr:
                        newstr = newstr + applyRules(ch)

                    return newstr

                def applyRules(ch):
                    newstr = ""
                    if ch == 'F':
                        newstr = 'FF'   # Rule 1
                    elif ch == 'X':
                        newstr = '--FXF++FXF++FXF--'
                    else:
                        newstr = ch     # no rules apply so keep the character

                    return newstr

                def drawLsystem(aTurtle,instructions,angle,distance):
                    for cmd in instructions:
                        if cmd == 'F':
                            aTurtle.forward(distance)
                        elif cmd == 'B':
                            aTurtle.backward(distance)
                        elif cmd == '+':
                            aTurtle.right(angle)
                        elif cmd == '-':
                            aTurtle.left(angle)
                        else:
                            # unknown command, ignore it.
                            pass

                def main():
                    inst = createLSystem(5,"FXF--FF--FF")   #create the string
                    print(inst)
                    t = turtle.Turtle()           #create the turtle
                    wn = turtle.Screen()
                    t.up()
                    t.back(200)
                    t.right(90)
                    t.forward(100)
                    t.left(90)
                    t.down()
                    t.speed(9)

                    drawLsystem(t,inst,60,5)      #draw the picture
                                                  #angle 90, segment length 5
                    wn.exitonclick()

                main()


        .. tab:: Discussion 

            .. disqus::
                :shortname: interactivepython
                :identifier: disqus_912a5f19d3964dc2af7a067dcd832c7e


#. Write a function that implements a substitution cipher.  In a substitution
   cipher one letter is substituted for another to garble the message.  For
   example A -> Q, B -> T, C -> G etc.  your function should take two
   parameters, the message you want to encrypt, and a string that represents
   the mapping of the 26 letters in the alphabet.  Your function should
   return a string that is the encrypted version of the message.

   .. actex:: ex_8_17

#.

    .. tabbed:: q19

        .. tab:: Question

           Write a function that decrypts the message from the previous exercise.  It
           should also take two parameters.  The encrypted message,
           and the mixed up alphabet.  The function should return a string that is
           the same as the original unencrypted message.
        
           .. actex:: ex_8_18

        .. tab:: Answer

            .. activecode:: q19_answer

                def encrypt(message, cipher):
                    alphabet = "abcdefghijklmnopqrstuvwxyz"
                    encrypted = ''
                    for char in message:
                        if char == ' ':
                            encrypted = encrypted + ' '
                        else:
                            pos = alphabet.index(char)
                            encrypted = encrypted + cipher[pos]
                    return encrypted

                def decrypt(encrypted, cipher):
                    alphabet = "abcdefghijklmnopqrstuvwxyz"
                    decrypted = ''
                    for char in encrypted:
                        if char == ' ':
                            decrypted = decrypted + ' '
                        else:
                            pos = cipher.index(char)
                            decrypted = decrypted + alphabet[pos]
                    return decrypted


                cipher = "badcfehgjilknmporqtsvuxwzy"

                encrypted = encrypt('hello world', cipher)
                print encrypted

                decrypted = decrypt(encrypted, cipher)
                print(decrypted)

        .. tab:: Discussion

            .. disqus::
                :shortname: interactivepython
                :identifier: disqus_d7d1ca00bfff4e7bacf886386fb3302e


#. Write a function called  ``removeDups`` that takes a string and creates a new string by only adding those characters that are not already present.  In other words,
   there will never be a duplicate letter added to the new string.

   .. actex:: ex_8_19

      def removeDups(astring):
          # your code here

      
      print(removeDups("mississippi"))   #should print misp


#.

    .. tabbed:: q21

        .. tab:: Question

           Write a function called ``rot13`` that uses the Caesar cipher to encrypt a message.
           The Caesar cipher works like a substitution cipher but each character is replaced
           by the character 13 characters to 'its right' in the alphabet.  So for example
           the letter a becomes the letter n.  If a letter is past the middle of the alphabet
           then the counting wraps around to the letter a again, so n becomes a, o becomes b
           and so on.  *Hint:* Whenever you talk about things wrapping around its a good idea
           to think of modulo arithmetic.
        
           .. actex:: ex_8_20
        
              def rot13(mess):
                  # Your code here
        
              print(rot13('abcde'))
              print(rot13('nopqr'))
              print(rot13(rot13('Since rot13 is symmetric you should see this message')))

        .. tab:: Answer
            
            .. activecode:: q21_answer

                def rot13(mess):
                    alphabet = 'abcdefghijklmnopqrstuvwxyz'
                    encrypted = ''
                    for char in mess:
                        if char == ' ':
                            encrypted = encrypted + ' '
                        else:
                            rotated_index = alphabet.index(char) + 13
                            if rotated_index < 26:
                                encrypted = encrypted + alphabet[rotated_index]
                            else:
                                encrypted = encrypted + alphabet[rotated_index % 26]
                    return encrypted

                print(rot13('abcde'))
                print(rot13('nopqr'))
                print(rot13(rot13('since rot thirteen is symmetric you should see this message')))

        .. tab:: Discussion 

            .. disqus::
                :shortname: interactivepython
                :identifier: disqus_49e1151bb7864a3287a6b6ae1c84db16

