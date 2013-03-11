import cImage as myimage

fg = myimage.FileImage('secret.png')
newIm = myimage.EmptyImage(fg.getWidth(),fg.getHeight())

for row in range(fg.getHeight()):
    for col in range(fg.getWidth()):
        fgpix = fg.getPixel(col,row)
        fgr = fgpix.getRed()
        fgg = fgpix.getGreen()
        fgb = fgpix.getBlue()
                
        if fgr % 2 == 0: #and fgg % 2 == 0:
            newPix = myimage.Pixel(255,255,255)
        else:
            newPix = myimage.Pixel(0,0,0)
        newIm.setPixel(col,row,newPix)

win = myimage.ImageWin("test",500,400)
newIm.draw(win)
win.exitOnClick()