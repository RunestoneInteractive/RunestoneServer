Hiding in Plain Sight
=====================

I have just come home from the 2013 SIGCSE conferece.  The Special Interest Group for Computer Science Education (SIGCSE) conference was in Denver this year.  One of the special features of this years conference was a screening of the movie Codebreaker.  Its a great movie about the life of Alan Turing, one of the fathers of Computer Science, and as the title suggests a pivitol figure in World War II.  Turing broke the code from the Nazi Enigma machine.  Here  is a picture of the machine that I took at the Deutches Museum in Munich Germany in 2011.  Turing was also arrested by the British government because he was gay. He ultimately killed himself; cutting short a life and career far too soon.  You should check out the trailer for the movie at `turingfilm.com <www.turingfilm.com>`_.

.. raw:: html

    <img src="../../_static/secret.png" id="secret.png">

This reminded me of a topic that I have wanted to write about for a while now, **Stegnography.**  Take another look at the image of the enigma machine. Look really carefully.  Do you see anything amiss?  Can you find the phrase 'Python Rocks' anywhere in the image?  If you are not familiar with basic image processing check out this section `on image processing <http://interactivepython.org/courselib/static/thinkcspy/MoreAboutIteration/moreiteration.html#dimensional-iteration-image-processing>`_  Its going to come in handy later in this post.

.. actex:: imagefun1

It is there, I promise you.  Lets see if we can find it together.

Here's a silly example of steganography from my personal blog last summer when we were on a cruise and happened to be lucky enough to be part of the filiming of this season's Top Chef.  Of course we were under non-disclosure at the time so I wrote this with added emphasis:

    Last night we had our second phenomenal dinner in Qsine. **this is the restaurant that features the iPads, we were rewArDed by seeing someone faMous at the tAble next to us.** We didn’t intrude on her privacy since she was having dinner with her family and celebrating her father’s birthday.

Of course if you look at bolded sentence closely you will notice there are some odd capital letters.  If you put them all together you will see they spell out PADMA, one of the hosts of Top Chef.  Captitalization is a bit obvious, you can use other techniques like italicizing, or using the first letter of each sentance.  The point is that the message is right there in plain site, for anyone to decode, if they know how you are hiding the message.

Hiding a message in an image is a bit different, and to understand whats going on in the image of the enigma machine lets start with how an image is represented.  The first thing to remember is that every pixel in the image is composed of some red, some green, and some blue.  The values for red, green, and blue are specified as integers in the range 0..255.  why 0 and 255?  Figure 1 shows you an 8 bit binary number.  Its an 8 bit number because there are 8 zeros or ones that make up this number.  The way that we convert a binary number into a decimal number is the following.  Mulitply the number (0 or 1) in the top box by the power of 2 below.

.. figure:: binary.png
   :align: center
   
So, for the example in figure we would have:

.. math::

   1 \cdot 2^7 + 0 \cdot 2^6 + 0 \cdot 2^5 + 1 \cdot 2^4 + 0 \cdot 2^3 + 1 \cdot 2^2 + 0 \cdot 2^1 + 1 \cdot 2^0 = 149

The bigest number we can represent in 8 bits would be ``11111111`` or 255.  You do the math.  The smallest number is ``00000000``.  Now, some bits are more important than others.  Which bits in our system have the biggest impact on the magnitude of the number?  The left most bit!  The leftmost bit is either 0 or 1 times :math:`2^7`  Thats a swing of 128 depending on whether that bit is 0 or 1. Therefore we call that bit the **most significant bit**.  On the other hand, the **least significant bit** is the bit on the right because that is just 0 or 1 times :math:`2^0`  which is a swing of only 1.

.. admonition:: Note

   In some computer systems the most significant bit is the one on the left, just as we said above, but in other computer systems the bit on the right is most significant bit.  Computer systems with the most significant bit on the left are called "big-endian" machines, while those with the most significant bit on the right are called "little-endian" machines.

So why all this fuss aout most or least significant bits?  When specifying red, green and blue values, how much difference will it make if you change the right-most bit on the amount of red you are adding to a pixel?  It amounts to a change of 0.392 percent.  Less than one half of one percent in the amount of red.  In fact that is less than the human eye can detect, particularly in a system where the human eye doesn't even see individual pixels! -- Yay retina displays!

To send our secret message we are going to take over the least significant bit of the amount of red color information in order to encode an image within an image!  Since we only have a single bit of information to work with our secret image will be a simple black and white image that spells out our secret message.

The algorithm to extract the message is easy.  We iterate over every pixel in our original image.  Get the red value for that pixel.  An easy way to see whether the least significant bit in the pixel is 1 or 0 is to test if the number is odd or even. If the pixel is even we color it white.  If the pixel is odd we will color it black.  The full program is shown below.

.. activecode:: decode1

   import image

   fg = image.Image('secret.png')
   newIm = image.EmptyImage(fg.getWidth(),fg.getHeight())

   for row in range(fg.getHeight()):
       for col in range(fg.getWidth()):
           fgpix = fg.getPixel(col,row)
           fgr = fgpix.getRed()
                
           if fgr % 2 == 0: 
               newPix = image.Pixel(255,255,255)
           else:
               newPix = image.Pixel(0,0,0)
           newIm.setPixel(col,row,newPix)

   win = image.ImageWin(500,400)
   newIm.draw(win)
   win.exitOnClick()


Hopefully you got the message.  Now, there are a few caveats to think about with this.  program, in fact if you have python running on your own computer try the following experiment.  Save the original secret image by right clicking and choosing save image as.   Save it as a 'jpg' file instead of a png file.  Now download and run the decode software on your own computer.  If you haven't been through the `image processing section <http://interactivepython.org/courselib/static/thinkcspy/MoreAboutIteration/moreiteration.html#dimensional-iteration-image-processing>`_  then you'll need to go back there and follow the instructions for downloading the ``cImage`` module.  Although thats going to be a bit of work for an experiment that will fail dramatically.  If you convert the image to jpg as I've suggested and run the decode program you'll end up with an image that looks something like this:

.. figure:: lossy_secret.png
   :align: center
   
   jpeg's algorithms 'lossed' my message.

The reason for this is that the jpeg compression algorithm is called a 'lossy' algorithm.  which means that some of your color information could be lost as the image is compressed.  Although you can't see it with your eye because the jpeg algorithms play exactly the same trick as our steganography does.  They rely on the fact that you can change some of the bits without the viewer being aware of it.  PNG images on the other hand use a lossless compression, this means that you do not lose any information and even our minor 'bit twiddling' is preserved.

Here is a new image, and an image containing the secret message.  See if you can figure out how to create the secret message.

.. actex:: make_message

   import image
   
Since we have demonstrated that we can use a few bits here and there for our own purposes, its important to realize that we can use these bits to encode anything!  We can use the bits to encode another image, as we have already done, or we can encode text, or audio, or even video.


