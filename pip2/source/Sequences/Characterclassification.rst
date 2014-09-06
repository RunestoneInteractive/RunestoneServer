..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Character classification
------------------------

It is often helpful to examine a character and test whether it is upper- or
lowercase, or whether it is a character or a digit. The ``string`` module
provides several constants that are useful for these purposes. One of these,
``string.digits`` is equivalent to "0123456789".  It can be used to check if a character
is a digit using the ``in`` operator.

The string ``string.ascii_lowercase`` contains all of the ascii letters that the system
considers to be lowercase. Similarly, ``string.ascii_uppercase`` contains all of the
uppercase letters. ``string.punctuation`` comprises all the characters considered
to be punctuation. You can't actually run the code below in the browser (sorry, limitation of our environment, not
*all* of python has been implemented.) But the comments indicate what would be produced; later in the
semester you'll have facilities for actually executing it.

.. activecode:: seq_char_classification
    
    import string
    print string.ascii_lowercase
    print string.ascii_uppercase
    print string.digits
    print string.punctuation
    x = "a"
    y = "A"
    print x in string.ascii_lowercase  # True
    print x in string.ascii_uppercase  # False
    print y in string.ascii_lowercase  # False
    print y in string.ascii_uppercase  # True


For more information consult the ``string`` module documentation (see `Global Module Index <http://docs.python.org/py3k/py-modindex.html>`_).


.. note::

   This workspace is provided for your convenience.  You can use this activecode window to try out anything you like.

   .. activecode:: scratch_08_04

