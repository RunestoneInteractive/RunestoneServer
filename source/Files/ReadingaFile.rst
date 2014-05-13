..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Reading a File
~~~~~~~~~~~~~~

As an example, suppose we have a text file called ``qbdata.txt`` that contains
the following data representing statistics about NFL quarterbacks. Although it
would be possible to consider entering this data by hand each time it is used,
you can imagine that it would be time-consuming and error-prone to do this. In
addition, it is likely that there could be data from more quarterbacks and
other years. The format of the data file is as follows
::

    First Name, Last Name, Position, Team, Completions, Attempts, Yards, TDs Ints, Comp%, Rating

.. raw:: html

    <pre id="qbdata.txt">
    Colt McCoy QB CLE  135 222 1576    6   9   60.8%   74.5
    Josh Freeman QB TB 291 474 3451    25  6   61.4%   95.9
    Michael Vick QB PHI    233 372 3018    21  6   62.6%   100.2
    Matt Schaub QB HOU 365 574 4370    24  12  63.6%   92.0
    Philip Rivers QB SD    357 541 4710    30  13  66.0%   101.8
    Matt Hasselbeck QB SEA 266 444 3001    12  17  59.9%   73.2
    Jimmy Clausen QB CAR   157 299 1558    3   9   52.5%   58.4
    Joe Flacco QB BAL  306 489 3622    25  10  62.6%   93.6
    Kyle Orton QB DEN  293 498 3653    20  9   58.8%   87.5
    Jason Campbell QB OAK  194 329 2387    13  8   59.0%   84.5
    Peyton Manning QB IND  450 679 4700    33  17  66.3%   91.9
    Drew Brees QB NO   448 658 4620    33  22  68.1%   90.9
    Matt Ryan QB ATL   357 571 3705    28  9   62.5%   91.0
    Matt Cassel QB KC  262 450 3116    27  7   58.2%   93.0
    Mark Sanchez QB NYJ    278 507 3291    17  13  54.8%   75.3
    Brett Favre QB MIN 217 358 2509    11  19  60.6%   69.9
    David Garrard QB JAC   236 366 2734    23  15  64.5%   90.8
    Eli Manning QB NYG 339 539 4002    31  25  62.9%   85.3
    Carson Palmer QB CIN   362 586 3970    26  20  61.8%   82.4
    Alex Smith QB SF   204 342 2370    14  10  59.6%   82.1
    Chad Henne QB MIA  301 490 3301    15  19  61.4%   75.4
    Tony Romo QB DAL   148 213 1605    11  7   69.5%   94.9
    Jay Cutler QB CHI  261 432 3274    23  16  60.4%   86.3
    Jon Kitna QB DAL   209 318 2365    16  12  65.7%   88.9
    Tom Brady QB NE    324 492 3900    36  4   65.9%   111.0
    Ben Roethlisberger QB PIT  240 389 3200    17  5   61.7%   97.0
    Kerry Collins QB TEN   160 278 1823    14  8   57.6%   82.2
    Derek Anderson QB ARI  169 327 2065    7   10  51.7%   65.9
    Ryan Fitzpatrick QB BUF    255 441 3000    23  15  57.8%   81.8
    Donovan McNabb QB WAS  275 472 3377    14  15  58.3%   77.1
    Kevin Kolb QB PHI  115 189 1197    7   7   60.8%   76.1
    Aaron Rodgers QB GB    312 475 3922    28  11  65.7%   101.2
    Sam Bradford QB STL    354 590 3512    18  15  60.0%   76.5
    Shaun Hill QB DET  257 416 2686    16  12  61.8%   81.3
    </pre>

To open this file, we would call the ``open`` function. The variable,
``fileref``, now holds a reference to the file object returned by
``open``. When we are finished with the file, we can close it by using
the ``close`` method. After the file is closed any further attempts to
use ``fileref`` will result in an error.

    ::

            >>>fileref = open("qbdata.txt","r")
            >>>
            >>>fileref.close()
            >>>

