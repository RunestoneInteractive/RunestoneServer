..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Objects are Mutable
-------------------

We can change the state of an object by making an assignment to one of its instance variables.
For example, we could change the numerator of the fraction by assigning a new
value to ``self.num``.  Likewise, we could do the same thing for ``self.den``.

One place where this type of modification makes sense is when we place a fraction in **lowest terms**.  Lowest terms simply
means that the numerator and denominator do not share any common factors.  For example, ``12/16`` is a fraction but it is
not in lowest terms since 2 can divide into both 12 and 16.  We call 2 a **common divisor**.  If we divide the numerator
and the denominator by a common divisor, we get an equivalent fraction.  If we divide by the **greatest common divisor**, 
we will get the lowest terms representation.  In this case 4 would be the greatest common divisor and the lowest terms
representation would be 3/4.

There is a very nice iterative method for computing the greatest common divisor of two integers.  Try to run the
function on a number of different examples.

.. activecode:: fractions_gcd

	def gcd(m, n):
	    while m % n != 0:
	        oldm = m
	        oldn = n

	        m = oldn
	        n = oldm % oldn
            
	    return n

	print(gcd(12, 16))


Now that we have a function that can help us with finding the greatest common divisor, we can use that to implement
a fraction method called ``simplify``.  We will ask the fraction "to put itself in lowest terms".

The ``simplify`` method will pass the numerator and the denominator to the ``gcd`` function to find the
greatest common divisor.  It will then modify itself by dividing its ``num`` and its ``den`` by that value.

.. activecode:: fractions_simplify

    def gcd(m, n):
        while m % n != 0:
            oldm = m
            oldn = n

            m = oldn
            n = oldm % oldn

        return n

    class Fraction:

        def __init__(self, top, bottom):

            self.num = top        # the numerator is on top
            self.den = bottom     # the denominator is on the bottom

        def __str__(self):
            return str(self.num) + "/" + str(self.den)

        def simplify(self):
            common = gcd(self.num, self.den)

            self.num = self.num // common
            self.den = self.den // common

    myfraction = Fraction(12, 16)

    print(myfraction)
    myfraction.simplify()
    print(myfraction)


There are two important things to note about this implementation.  First, the ``gcd`` function is not
a method of the class.  It does not belong to ``Fraction``.  Instead it is a function that is used by ``Fraction``
to assist in a task that needs to be performed.  This type of function is often called a **helper function**.  Second,
the ``simplify`` method does not return anything.  Its job is to modify the object itself.  This type of method is
known as a **mutator** method because it mutates or changes the internal state of the object. 



.. index:: equality, equality; deep, equality; shallow, shallow equality, deep equality      

