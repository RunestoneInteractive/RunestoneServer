..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Arithmetic Methods
------------------

We will conclude this chapter by adding a few more methods to our ``Fraction`` class.  In particular, we will implement
arithmetic.  To begin, consider what it means to add two fractions together.
Remember that you can only add fractions if they have the same denominator.  The easiest way to find a common denominator is
to multiply the two individual denominators together.  Anything we do to the denominator needs to the done to the numerator.  This gives us the following equation for fraction addition::

     a/b + c/d = (ad + cb)/bd


Our ``add`` method will take a ``Fraction`` as a parameter.  It will return a new ``Fraction`` representing the sum.  We
will use the equation shown above to compute the new numerator and the new denominator.  Since this equation will not
give us lowest terms, we will utilize a similar technique as was used in the ``simplify`` method to find the 
greatest common divisor and then divide each part of the new fraction.

.. sourcecode:: python

	def add(self,otherfraction):

	    newnum = self.num*otherfraction.den + self.den*otherfraction.num
	    newden = self.den * otherfraction.den

	    common = gcd(newnum,newden)

	    return Fraction(newnum//common,newden//common)

You can try the addition method and then modify the fractions and retry.


.. activecode:: fractions_add1

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

        def add(self,otherfraction):

            newnum = self.num*otherfraction.den + self.den*otherfraction.num
            newden = self.den * otherfraction.den

            common = gcd(newnum, newden)

            return Fraction(newnum // common, newden // common)

    f1 = Fraction(1, 2)
    f2 = Fraction(1, 4)

    f3 = f1.add(f2)
    print(f3)


One final modification to this method will be quite useful.  Instead invoking the ``add`` method, we can use the
addition operator "+".  This requires that we implement another special method, this time called ``__add__``.
The details of the method are the same.

.. sourcecode:: python

	def __add__(self, otherfraction):

	    newnum = self.num*otherfraction.den + self.den*otherfraction.num
	    newden = self.den * otherfraction.den

	    common = gcd(newnum, newden)

	    return Fraction(newnum // common, newden // common)

However, now we can perform addition in the same manner that we are used to with other numeric data.

.. sourcecode:: python

	f1 = Fraction(1, 2)
	f2 = Fraction(1, 4)

	f3 = f1 + f2    # calls the __add__ method of f1
	print(f3)

.. note::

    This workspace is provided for your convenience.  You can use this activecode window to try out anything you like.

    .. activecode:: scratch_cl_02	


