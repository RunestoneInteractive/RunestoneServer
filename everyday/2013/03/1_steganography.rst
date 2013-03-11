Hiding in Plain Sight
=====================

I have just come home from the 2013 SIGCSE conferece.  The Special Interest Group for Computer Science Education (SIGCSE) conference was in Denver this year.  One of the special features of this years conference was a screening of the movie Codebreaker.  Its a great movie about the life of Alan Turing, one of the fathers of Computer Science, and as the title suggests a pivitol figure in World War II.  Turing broke the code from the Nazi Enigma machine.  Here  is a picture of the machine that I took at the Deutches Museum in Munich Germany in 2011.  Turing was also arrested by the British government because he was gay. He ultimately killed himself; cutting short a life and career far too soon.  You should check out the trailer for the movie at `turingfilm.com <www.turingfilm.com>`_.

.. raw:: html

    <img src="../_static/secret.png" id="secret.png">

This reminded me of a topic that I have wanted to write about for a while now, **Stegnography.**  Take another look at the image of the enigma machine. Look really carefully.  Do you see anything amiss?  Can you find the phrase 'Python Rocks' anywhere in the image?  If you are not familiar with basic image processing check out this section `on image processing <http://interactivepython.org/courselib/static/thinkcspy/MoreAboutIteration/moreiteration.html#dimensional-iteration-image-processing>`_

.. actex:: imagefun1

It is there, I promise you.  Lets see if we can find it together.

Here's a silly example of steganography from my personal blog last summer when we were on a cruise and happened to be lucky enough to be part of the filiming of this season's Top Chef.  Of course we were under non-disclosure at the time so I wrote this with added emphasis:

> Last night we had our second phenomenal dinner in Qsine. **this is the restaurant that features the iPads, we were rewArDed by seeing someone faMous at the tAble next to us.** We didn’t intrude on her privacy since she was having dinner with her family and celebrating her father’s birthday.

Of course if you look at bolded sentence closely you will notice there are some odd capital letters.  If you put them all together you will see they spell out PADMA, one of the hosts of Top Chef.

