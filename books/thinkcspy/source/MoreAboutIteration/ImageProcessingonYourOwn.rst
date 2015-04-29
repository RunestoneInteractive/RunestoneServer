..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

.. qnum::
   :prefix: iter-10-
   :start: 1

Image Processing on Your Own
----------------------------

If you want to try some image processing on your own, outside of the textbook you can do so using the cImage module.  You can download ``cImage.py`` from `The github page <https://github.com/bnmnetp/cImage>`_ .   If you put ``cImage.py`` in the same folder as your program you can then do the following to be fully compatible with the code in this book.

.. sourcecode:: python

   import cImage as image
   img = image.Image("myfile.gif")

.. admonition:: Note

   One important caveat about using ``cImage.py`` is that it will only work with GIF files unless you also install the Python Image Library.  The easiest version to install is called ``Pillow``.  If you have the ``pip`` command installed on your computer this is really easy to install, with ``pip install pillow`` otherwise you will need to follow the instructions on the `Python Package Index <https://pypi.python.org/pypi/Pillow/>`_ page.  With Pillow installed you will be able to use almost any kind of image that you download.




.. note::

  This workspace is provided for your convenience.  You can use this activecode window to try out anything you like.

  .. activecode:: scratch_07_05


