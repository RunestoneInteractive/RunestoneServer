import cImage as myimage

fg = myimage.FileImage('ascii_secret.png')
newIm = myimage.EmptyImage(fg.getWidth(),fg.getHeight())

def bit_generator(fg):
    for row in range(fg.getHeight()):
        for col in range(fg.getWidth()):
            fgpix = fg.getPixel(col,row)
            fgr = fgpix.getRed()
            yield fgr & 1
            fgg = fgpix.getGreen()
            yield fgg & 1
            fgb = fgpix.getBlue()
            yield fgb & 1

mybits = bit_generator(fg)

done = False
mess = 0
n = 0
mess_str = ''
while not done:
    bit = mybits.next()
    mess = mess + bit * 2**n
    n += 1
    if n == 7:
        if mess == 0:
            done = True
        else:
            mess_str += chr(mess)
            mess = 0
            n = 0

print mess_str

