"""
image.py
This module provides a simple interface to create a window, load an image and experiment 
with image based algorithms.  Many of which require pixel-by-pixel manipulation.  This
is a educational module, its not intended to replace the excellent Python Image Library, in fact 
it uses PIL.

The module and its interface and some of the code were inspired/copied by/from John Zelle's graphics.py 
which serves a similar purpose in the graphics primitive world.
"""

# Release Notes:
# Version 1.0   Fall 2005
#
# Brad Miller, Luther College
#
# Version 1.1   December 7, 2005
# Changes:
#   Modify class name for base image to be AbstractImage   This way we don't have a lower case
#      class name running around.  We still don't expect people to create an AbstractImage but
#      rather create an image through FileImage, ListImage, or EmptyImage.
#   Add ability to convert an image to a list
#   Add save function to write an image back to disk.
#
# Version 1.2  November 2007
# Changes:
#  Modify the setPosition function to position the image by the top left corner rather than
#    the center.
#  Add the exitOnClick method to ImageWin.  Use this as the last call in the program to
#    avoid early exits when running from the command line, and nasty hangs when running
#    from within IDLE
#
# Version 1.3  May 2008
# Changes:
#   Modify all code to be Python 3.0 ready.  -- still runs under 2.x
#   Modify all code so that if pil is not available then image.py will still
#   function using Tkimages.  N.B.  Tk restricts image types to gif or ppm
#

try:
    import tkinter
except:
    import Tkinter as tkinter

pilAvailable = True
try:
    from PIL import Image
    from PIL import ImageTk
except:
    pilAvailable = False

#import exceptions

# Borrow some ideas from Zelle
# create an invisible global main root for all windows
tk = tkinter
_imroot = tk.Tk()
_imroot.withdraw()

def formatPixel(data):
    if type(data) == tuple:
        return '{#%02x%02x%02x}'%data
    elif isinstance(data,Pixel):
        return '{#%02x%02x%02x}'%data.getColorTuple()

class ImageWin(tk.Canvas):
    """
    ImageWin:  Make a frame to display one or more images.
    """
    def __init__(self,title="image window",width=640,height=640):        
        """
        Create a window with a title, width and height.
        """
        master = tk.Toplevel(_imroot)
        master.protocol("WM_DELETE_WINDOW", self._close)
        #super(ImageWin, self).__init__(master, width=width, height=height)
        tk.Canvas.__init__(self, master, width=width, height=height)
        self.master.title(title)
        self.pack()
        master.resizable(0,0)
        self.foreground = "black"
        self.items = []
        self.mouseX = None
        self.mouseY = None
        self.bind("<Button-1>", self._onClick)
        self.height = height
        self.width = width
        self._mouseCallback = None
        self.trans = None
        _imroot.update()

    def _close(self):
        """Close the window"""
        self.master.destroy()
        self.quit()
        _imroot.update()

    def getMouse(self):
        """Wait for mouse click and return a tuple with x,y position in screen coordinates after
        the click"""
        self.mouseX = None
        self.mouseY = None
        while self.mouseX == None or self.mouseY == None:
            self.update()
        return ((self.mouseX,self.mouseY))

    def setMouseHandler(self, func):
        self._mouseCallback = func

    def _onClick(self, e):
        self.mouseX = e.x
        self.mouseY = e.y
        if self._mouseCallback:
            self._mouseCallback(e.x, e.y)

    def exitOnClick(self):
        """When the Mouse is clicked close the window and exit"""
        self.getMouse()
        self._close()
        
    def exitonclick(self):
        self.exitOnClick()


class Pixel(object):
    """This simple class abstracts the RGB pixel values."""
    def __init__(self, red, green, blue):
        super(Pixel, self).__init__()
        self.__red = red
        self.__green = green
        self.__blue = blue
        self.max = 255

    def getRed(self):
        """Return the red component of the pixel"""
        return self.__red

    def getGreen(self):
        """Return the green component of the pixel"""
        return self.__green

    def getBlue(self):
        """Return the blue component of the pixel"""
        return self.__blue

    def getColorTuple(self):
        """Return all color information as a tuple"""
        return (self.__red, self.__green, self.__blue)

    def setRed(self,red):
        """Modify the red component"""
        if self.max >= red >= 0:
            self.__red = red
        else:
            raise ValueError("Error:  pixel value %d is out of range" % red)

    def setGreen(self,green):
        """Modify the green component"""
        if self.max >= green >= 0:
            self.__green = green
        else:
            raise ValueError("Error:  pixel value %d is out of range" % green)

    def setBlue(self,blue):
        """Modify the blue component"""
        if self.max >= blue >= 0:
            self.__blue = blue
        else:
            raise ValueError("Error:  pixel value %d is out of range" % blue)

    def __getitem__(self,key):
        """Allow new style pixel class to act like a color tuple:
           0 --> red
           1 --> green
           2 --> blue
        """
        if key == 0:
            return self.__red
        elif key == 1:
            return self.__green
        elif key == 2:
            return self.__blue
        else:
            raise ValueError("Error %d Index out of range" % key)

    def setRange(self,pmax):
        """docstring for setRange"""
        if pmax == 1.0:
            self.max = 1.0
        elif pmax == 255:
            self.max = 255
        else:
            raise ValueError("Error range must be 1.0 or 256")

    def __str__(self):
        return str(self.getColorTuple())

    def __repr__(self):
        """docstring for __repr__"""
        return str(self.getColorTuple())

    red = property(getRed, setRed, None, "I'm the red property.")
    green = property(getGreen, setGreen, None, "I'm the green property.")
    blue = property(getBlue, setBlue, None, "I'm the blue property.")

class AbstractImage(object):
    """
    Create an image.  The image may be created in one of four ways:
    1. From an image file such as gif, jpg, png, ppm  for example: i = image('fname.jpb)
    2. From a list of lists
    3. From another image object
    4. By specifying the height and width to create a blank image.
    """
    imageCache = {} # tk photoimages go here to avoid GC while drawn 
    imageId = 1
    def __init__(self,fname=None,data=[],imobj=None,height=0,width=0):
        """
        An image can be created using any of the following keyword parameters. When image creation is 
        complete the image will be an rgb image.
        fname:  A filename containing an image.  Can be jpg, gif, and others
        data:  a list of lists representing the image.  This might be something you construct by
        reading an asii format ppm file, or an ascii art file and translate into rgb yourself.
        imobj:  Make a copy of another image.
        height:
        width: Create a blank image of a particular height and width.
        """
        super(AbstractImage, self).__init__()

        # if PIL is available then use the PIL functions otherwise fall back to Tk
        if pilAvailable:
            self.loadImage = self.loadPILImage
            self.createBlankImage = self.createBlankPILImage
            self.setPixel = self.setPILPixel
            self.getPixel = self.getPILPixel
            self.save = self.savePIL
        else:
            self.loadImage = self.loadTkImage
            self.createBlankImage = self.createBlankTkImage
            self.setPixel = self.setTkPixel
            self.getPixel = self.getTkPixel
            self.save = self.saveTk

        if fname:
            self.loadImage(fname)
            self.imFileName = fname
        elif data:
            height = len(data)
            width = len(data[0])
            self.createBlankImage(height,width)
            for row  in range(height):
                for col in range(width):
                    self.setPixel(col,row,Pixel(data[row][col]))
        elif height > 0 and width > 0:
            self.createBlankImage(height,width)
        elif imobj:
            self.im = imobj.copy()

        if pilAvailable:
            self.width,self.height = self.im.size
        else:
            self.width = self.im.width()
            self.height = self.im.height()
        self.centerX = self.width/2+3     # +3 accounts for the ~3 pixel border in Tk windows
        self.centerY = self.height/2+3
        self.id = None

    def loadPILImage(self,fname):
        self.im = Image.open(fname)
        ni = self.im.convert("RGB")
        self.im = ni

    def loadTkImage(self,fname):
        sufstart = fname.rfind('.')
        if sufstart < 0:
            suffix = ""
        else:
            suffix = fname[sufstart:]
        if suffix not in ['.gif', '.ppm']:
            raise ValueError("Bad Image Type: %s : Without PIL, only .gif or .ppm files are allowed" % suffix)
        self.im = tkinter.PhotoImage(file=fname)

    def createBlankPILImage(self,height,width):
        self.im = Image.new("RGB",(width,height))
        ni = self.im.convert("RGB")
        self.im = ni

    def createBlankTkImage(self,height,width):
        self.im = tkinter.PhotoImage(height=height,width=width)


    def copy(self):
        """Return a copy of this image"""
        newI = AbstractImage(imobj=self.im)
        return newI


    def clone(self):
         """Return a copy of this image"""
         newI = AbstractImage(imobj=self.im)
         return newI

    def getHeight(self):
        """Return the height of the image"""
        return self.height

    def getWidth(self):
        """Return the width of the iamge"""
        return self.width

    def getTkPixel(self,x,y):
        """Get a pixel at the given x,y coordinate.  The pixel is returned as an rgb color tuple
        for eaxamplle foo.getPixel(10,10) --> (10,200,156) """
        p = [int(j) for j in self.im.get(x,y).split()]
        return Pixel(p[0],p[1],p[2])

    def setTkPixel(self,x,y,pixel):
        """Set the color of a pixel at position x,y.  The color must be specified as an rgb tuple (r,g,b) where 
        the rgb values are between 0 and 255."""
        if x < self.getWidth() and y < self.getHeight():
            self.im.put(formatPixel(pixel.getColorTuple()),(x,y))
        else:
            raise ValueError("Pixel index out of range.")

    def getPILPixel(self,x,y):
        """docstring for getPILPIxel"""
        p = self.im.getpixel((x,y))
        return Pixel(p[0],p[1],p[2])

    def setPILPixel(self,x,y,pixel):
        """docstring for setPILPixel"""
        if x < self.getWidth() and y < self.getHeight():
            self.im.putpixel((x,y),pixel.getColorTuple())
        else:
            raise ValueError("Pixel index out of range")

    def setPosition(self,x,y):
        """Set the position in the window where the top left corner of the window should be."""
        self.top = y
        self.left = x
        self.centerX = x + (self.width/2)+3
        self.centerY = y + (self.height/2)+3

    def getImage(self):
        if pilAvailable:
            return ImageTk.PhotoImage(self.im)
        else:
            return self.im

    def draw(self,win):
        """Draw this image in the ImageWin window."""
        ig = self.getImage()
        self.imageCache[self.imageId] = ig # save a reference else Tk loses it...
        AbstractImage.imageId = AbstractImage.imageId + 1
        self.canvas=win
        self.id = self.canvas.create_image(self.centerX,self.centerY,image=ig)
        _imroot.update()

    def saveTk(self,fname=None,ftype='gif'):
        if fname == None:
            fname = self.imFileName
        sufstart = fname.rfind('.')
        if sufstart < 0:
            suffix = ""
        else:
            suffix = fname[sufstart:]
        if suffix == "":
            suffix = "."+ftype
            fname = fname+suffix
        if suffix not in ['.gif', '.ppm']:
            raise ValueError("Without PIL, only .gif or .ppm files are allowed")
        try:
            self.im.write(fname,format=ftype)            
        except:
            print("Error saving, Could Not open ", fname, " to write.")

    def savePIL(self,fname=None,ftype='jpg'):
        if fname == None:
            fname = self.imFileName
        sufstart = fname.rfind('.')
        if sufstart < 0:
            suffix = ""
        else:
            suffix = fname[sufstart:]
        if suffix == "":
            suffix = "."+ftype
            fname = fname+suffix
        try:
            self.im.save(fname)            
        except:
            print("Error saving, Could Not open ", fname, " to write.")


    def toList(self):
        """
        Convert the image to a List of Lists representation
        """
        res = []
        for i in range(self.height):
            res.append([])
            for j in range(self.width):
                res[i].append(self.getPixel(j,i))
        return res


class FileImage(AbstractImage):
    def __init__(self,thefile):
        super(FileImage, self).__init__(fname = thefile)

if not pilAvailable:
    class Image(FileImage):
        pass
    
class EmptyImage(AbstractImage):
    def __init__(self,cols,rows):
        super(EmptyImage, self).__init__(height = rows, width = cols)

class ListImage(AbstractImage):
    def __init__(self,thelist):
        super(ListImage, self).__init__(data=thelist)

# Example program  Read in an image and calulate the negative.
if __name__ == '__main__':
    win = ImageWin("My Window",480,640)
    oImage = FileImage('lcastle.jpg')
    print(oImage.getWidth(), oImage.getHeight())
    oImage.draw(win)
    myImage = oImage.copy()

    for row in range(myImage.getHeight()):
        for col in range(myImage.getWidth()):
             v = myImage.getPixel(col,row)
             v.red = 255 - v.red
             v.green = 255 - v.green
             v.blue = 255 - v.blue
#             x = map(lambda x: 255-x, v)
             myImage.setPixel(col,row,v)
    myImage.setPosition(myImage.getWidth()+1,0)
    myImage.draw(win)
    print(win.getMouse())
    myImage.save('/Users/bmiller/tmp/testfoo.jpg')
    print(myImage.toList())
    win.exitOnClick()


