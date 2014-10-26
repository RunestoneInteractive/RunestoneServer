..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

.. _write_text_file_chap:

Writing Text Files
------------------

One of the most commonly performed data processing tasks is to read data from a file, manipulate it in some way, and then write the resulting data out to a new data file to be used for other purposes later.  
To accomplish this, the ``open`` function discussed above can also be used to create a new file prepared for writing.  
Note in :ref:`Table 1<filemethods1a>` above that the only difference between opening a file for writing and  opening a file for reading is the use of the ``'w'`` flag instead of the ``'r'`` flag as the second parameter.  
When we open a file for writing, a new, empty file with that name is created and made ready to accept our data. As before, the function returns a reference to the new file object.

:ref:`Table 2 <filemethods2a>` above shows one additional file method that we have not used thus far.  
The ``write`` method allows us to add data to a text file.  Recall that text files contain sequences of characters.  
We usually think of these character sequences as being the lines of the file where each line ends with the newline ``\n`` character.  
Be very careful to notice that the ``write`` method takes one parameter, a string.  When invoked, the characters of the string will be added to the end of the file.  
This means that it is the programmer's job to include the newline characters as part of the string if desired.

As an example, consider the ``qbdata.txt`` file once again.  Assume that we have been asked to provide a file consisting of only the names of the
quarterbacks.  In addition, the names should be in the order last name followed by first name with the names separated by a comma.  This
is a very common type of request, usually due to the fact that someone has a program that requires its data input format to be different from what is available.

To construct this file, we will approach the problem using a similar algorithm as above.  After opening the file, we will iterate thru the
lines, break each line into its parts, choose the parts that we need, and then output them.  Eventually, the output will be written to a file.

The program below solves part of the problem.  Notice that it reads the data and creates a string consisting of last name followed by a comma followed by the first name.  In this example, we simply print the lines as they are created.

.. activecode:: files_write01

    infile = open("qbdata.txt","r")
    # note: I have rewrittent the code to iterate using a for loop instead of a while loop; it's much simpler that way!
    # aline = infile.readline()
    # while aline:
    for aline in infile.readlines():
        items = aline.split()
        dataline = items[1] + ',' + items[0]
        print dataline
    #    aline = infile.readline()

    infile.close()

When we run this program, we see the lines of output on the screen.  Once we are satisfied that it is creating the appropriate output, the next step is to add the necessary pieces to produce an output file and write the data lines to it.  
To start, we need to open a new output file by adding another call to the ``open`` function, ``outfile = open("qbnames.txt",'w')``, using the ``'w'`` flag.  We can choose any file name we like.  
If the file does not exist, it will be created.  However, if the file does exist, it will be reinitialized as empty and you will lose any previous contents.  

Once the file has been created, we just need to call the ``write`` method passing the string that we wish to add to the file.  
In this case, the string is already being printed so we will just change the ``print`` into a call to the ``write`` method.  
However, there is one additional part of the data line that we need to include.  The newline character needs to be concatenated  to the end of the line.  
The entire line now becomes ``outfile.write(dataline + '\n')``.  The print statement automatically
outputs a newline character after whatever text it outputs, but the write method does not do that automatically. We also need to close the file when we are done.

The complete program is shown below.

.. note::
   Unfortunately, as described above, you can't actually write to a file when executing activecode in the browser. So for now, you'll just have to look at
   this program without being able to execute it.

.. sourcecode:: python

    infile = open("qbdata.txt","r")
    outfile = open("qbnames.txt","w")

    # note: I have rewrittent the code to iterate using a for loop instead of a while loop; it's much simpler that way!
    # aline = infile.readline()
    # while aline:
    for aline in infile:
        items = aline.split()
        dataline = items[1] + ',' + items[0]
        outfile.write(dataline + '\n')
    #    aline = infile.readline()

    infile.close()
    outfile.close()
    
    
The contents of the ``qbnames.txt`` file are as follows.

.. raw:: html

    <pre id="">
    McCoy,Colt
    Freeman,Josh
    Vick,Michael
    Schaub,Matt
    Rivers,Philip
    Hasselbeck,Matt
    Clausen,Jimmy
    Flacco,Joe
    Orton,Kyle
    Campbell,Jason
    Manning,Peyton
    Brees,Drew
    Ryan,Matt
    Cassel,Matt
    Sanchez,Mark
    Favre,Brett
    Garrard,David
    Manning,Eli
    Palmer,Carson
    Smith,Alex
    Henne,Chad
    Romo,Tony
    Cutler,Jay
    Kitna,Jon
    Brady,Tom
    Roethlisberger,Ben
    Collins,Kerry
    Anderson,Derek
    Fitzpatrick,Ryan
    McNabb,Donovan
    Kolb,Kevin
    Rodgers,Aaron
    Bradford,Sam
    Hill,Shaun
    </pre>
    
.. raw:: html

    <pre hidden id="qbdata.txt">
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
