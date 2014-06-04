#  h t m l F r a m e . p y
#
#  Chris Meyers. 09/25/2013
#
# Holder for attributes to be applied to a template and
# a simple function to apply attributes to template and
# send it to the <div> for display

from pg_logger import setHTML

dft_template = """
<html><body>
<h3>%(banner)s</h3>
<div>%(item1)s</div>
<div>%(item2)s</div>
<div>%(item3)s</div>
</html></body>
"""

class HtmlFrame :
    def __init__ (self, template=dft_template, banner="") :
        self.outputOn = True
        self.template = template
        self.banner   = banner
        self.item1 = self.item2 = self.item3 = ""

    def makeEofPage(self) :
        pass
            
    def makeFrame (self,template=None) :
        if not template : template = self.template
        content = template % self.__dict__
        setHTML(content)

