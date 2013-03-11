import cImage as myimage

fg = myimage.FileImage('enigma.jpg')
mess = myimage.FileImage('Message.jpeg')
newIm = myimage.EmptyImage(fg.getWidth(),fg.getHeight())

for row in range(fg.getHeight()):
    for col in range(fg.getWidth()):
        fgpix = fg.getPixel(col,row)
        fgr = fgpix.getRed()
        fgg = fgpix.getGreen()
        fgb = fgpix.getBlue()

        mspix = mess.getPixel(col,row)
        msr = mspix.getRed()
        msg = mspix.getGreen()
        msb = mspix.getBlue()

        if msr == 0:
            fgr = fgr & 0xfe
#            fgg = fgg & 0xfe
#            fgb = fgb & 0xfe
        else:
            fgr = fgr | 0x01
#            fgg = fgg | 0x01
#            fgb = fgb | 0x01

        newPix = myimage.Pixel(fgr,fgg,fgb)
        newIm.setPixel(col,row,newPix)

win = myimage.ImageWin("test",500,400)
newIm.draw(win)
newIm.save('secret.png')
win.exitOnClick()


# decIm = myimage.EmptyImage(fg.getWidth(),fg.getHeight())
#
# for row in range(fg.getHeight()):
#     for col in range(fg.getWidth()):
#         fgpix = newIm.getPixel(col,row)
#         fgr = fgpix.getRed()
#         fgg = fgpix.getGreen()
#         fgb = fgpix.getBlue()
#
#         if fgr % 2  == 1:
#             newPix = myimage.Pixel(255,255,255)
#         else:
#             newPix = myimage.Pixel(0,0,0)
#         decIm.setPixel(col,row,newPix)
#
# dwin = myimage.ImageWin("test",500,400)
# decIm.draw(dwin)
# win.exitOnClick()