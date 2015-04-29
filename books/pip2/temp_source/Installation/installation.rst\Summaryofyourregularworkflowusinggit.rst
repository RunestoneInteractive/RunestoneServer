..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Summary of your regular workflow using git
------------------------------------------

1. Each working session begins with a *clean working directory*: there should be no loose ends in your class code folder, everything should be **saved** and **committed**. Check to make sure that you finished your last session, by typing ``git status``. If it shows changed files that still need to be commited, resolve that before getting started.

2. Pull in any code updates from the instructors, by typing ``git pull upstream master`` in the command prompt.

3. Edit your files.

4. Add new and changed files with ``git add ...`` commands.

5. Commit your changes locally with ``git commit ...``.

