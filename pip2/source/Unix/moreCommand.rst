..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".


The more Command
-----------------

The ``more`` Unix command allows you to see the contents of a *file*.

``ls`` lists all the files inside your current directory, the directory you're accessing in a command prompt.

Once you're in a directory, you can access all the files in that directory, and one of the things you can do is look at the raw contents of that file. So if you are in a folder ``SI_106`` with a file called ``lecture-5-notes.txt`` inside, and you want to see what is written in that file IN your command prompt, you could type at the prompt:

``more lecture-5-notes.txt``

This command opens a special text editor in your command line. You'll see a ``:`` sign at the bottom of the window. You can hit the down arrow button to keep looking at more of the file until you reach the end. When you want to quit the text editor, and go back to your normal command prompt to make other commands or do something else, type the letter ``q``.

At this point, we won't be discussing exactly how to edit files inside this kind of command line text editor, but it's useful to remember that typing ``q`` when you're in the view created by ``more`` will get you out of that view and back to your working directory.

Why is this useful? Among other reasons, this can help you figure out what files you want to work with by getting a quick glimpse of them. ``ls`` shows you all the names of files in a directory, but maybe you need to look at the contents of a file specifically to remember what's in it.