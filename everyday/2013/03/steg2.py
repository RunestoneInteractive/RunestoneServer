import cImage as myimage

fg = myimage.FileImage('Foreground.jpeg')
newIm = myimage.EmptyImage(fg.getWidth(),fg.getHeight())
#mess = input('whats the message? ')
mess = '''My Favorite Quotes from Horton Hears a Who:  I meant what I said and I said what I meant. An elephant's faithful one hundred percent.
   or
That Horton is a menace. He has those kids using their imagination. It's sick!'''

import random

def bit_generator(mess):
    for ch in mess:
        ascii = ord(ch)
        ct = 0
        while ct < 7:
            yield ascii & 1
            ascii = ascii >> 1
            ct += 1
    for i in range(7):
        yield 0
    while True:
        yield random.randrange(1)

bitstream = bit_generator(mess)

def setbit(oldbyte,newbit):
    print newbit
    if newbit:
        return oldbyte | newbit
    else:
        return oldbyte & 0b11111110

for row in range(fg.getHeight()):
    for col in range(fg.getWidth()):
        fgpix = fg.getPixel(col,row)
        fgr = fgpix.getRed()
        fgg = fgpix.getGreen()
        fgb = fgpix.getBlue()

        redbit = bitstream.next()
        fgr = setbit(fgr,redbit)

        greenbit = bitstream.next()
        fgg = setbit(fgg,greenbit)

        bluebit = bitstream.next()
        fgb = setbit(fgb,bluebit)

        newPix = myimage.Pixel(fgr,fgg,fgb)
        newIm.setPixel(col,row,newPix)

win = myimage.ImageWin("test",500,400)
newIm.draw(win)
newIm.save('ascii_secret.png')
win.exitOnClick()