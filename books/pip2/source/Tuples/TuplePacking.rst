..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Tuple Packing
-------------

Wherever python expects a single value, if multiple expressions are provided, separated
by commas, they are automatically **packed** into a tuple. For example, we could
have omitted the parentheses when first assigning a tuple to the variable julia.

.. sourcecode:: python

    julia = ("Julia", "Roberts", 1967, "Duplicity", 2009, "Actress", "Atlanta, Georgia")
    # or equivalently
    julia = "Julia", "Roberts", 1967, "Duplicity", 2009, "Actress", "Atlanta, Georgia"
    


**Check your understanding**

.. mchoicema:: test_questiontuples_1
   :answer_a: print julia['city']
   :answer_b: print julia[-1]
   :answer_c: print julia(-1)
   :answer_d: print julia(6)
   :answer_e: print julia[7]
   :correct: b
   :feedback_a: julia is a tuple, not a dictionary; indexes must be integers
   :feedback_b: [-1] picks out the last item in the sequence
   :feedback_c: Index into tuples using square brackets. julia(-1) will try to treat julia as a function call, with -1 as the parameter value.
   :feedback_d: Index into tuples using square brackets. julia(-1) will try to treat julia as a function call, with -1 as the parameter value.
   :feedback_e: Indexing starts at 0. You want the seventh item, which is julia[6]

   Which of the following statements will output Atlanta, Georgia
