..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

.. _less_chap:

The cat and less commands
-------------------------

The ``cat`` and ``less`` Unix commands both allow you to see the contents of a *file*. Why are these commands useful? Among other reasons, this can help you figure out what files you want to work with by getting a quick glimpse of their contents. ``ls`` shows you all the names of files in a directory, but maybe you need to look at the contents of a file specifically to remember what's in it.

Once you're in a directory, you can access all the files in that directory, and one of the things you can do is look at the raw contents of that file. So if you are in a folder with a file called ``sample.txt`` inside it, and you want to see what is written in that file IN your command prompt, you could type at the prompt:

``cat sample.txt``

If the file has a lot of lines in it, you'll see them scroll by faster than your eye can process them. The less command lets you move forward and back in a more controlled manner.

``less sample.txt``

This command opens a special text viewer in your terminal window. You'll see a ``:`` at the bottom left of your screen. If the file has more lines than fit in your terminal window, you can hit the down arrow button or the space bar to see more. Press the up arrow or page up to see previous text. When you want to quit the text editor, and go back to your normal command prompt to make other commands or do something else, type the letter ``q`` (q for ``quit``).

The ``cat`` command also lets you concatenate multiple files together. For example, the following command displays the combined contents of files sample1.txt and sample.txt.

``cat sample1.txt sample2.txt``


.. image:: Figures/less.JPG