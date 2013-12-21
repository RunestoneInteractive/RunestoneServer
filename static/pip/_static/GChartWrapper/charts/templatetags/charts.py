"""
Django templatetags for chart and note types
Now takes an as argument
If the as argument is 'img', it will return a XHTML <img/>
If the as argument is 'url', it will simply return the url of the chart
If the as argument is anything else, the chart will be loaded into the context
and named what the as argument is

{% chart ... [as url|img|varname] %}
...
{% endchart %}

Example:

    {% chart Pie3D 1 2 3 4 5 as pie %}
        {% label A B C D %}
        {% color green %}
    {% endchart %}

    {% pie %} # The chart obj itself
    {% pie.image %} # The PIL instance
    {% pie.checksum %} # An SHA1 checksum

The FancyNode powers the tag for Note,Pin,Text and Bubble charts
The <type> argument is one of the chart types in lower case

    {% <type> ... [as url|img|varname]%}
    
    Example:
        {% bubble icon_text_big snack bb $2.99 ffbb00 black as img %}
    """

from django.template import Library,Node
from django.template import resolve_variable
import GChartWrapper

register = Library()

class GenericNode(Node):
    def __init__(self, args):
        self.args = map(unicode,args)
    def render(self,context):
        for n,arg in enumerate(self.args):
            if arg in context:
                self.args[n] = resolve_variable(arg, context)
            elif arg[0] == '"' and arg[-1] == '"':
                self.args[n] = arg[1:-1]
            elif arg[0] == "'" and arg[-1] == "'":
                self.args[n] = arg[1:-1]
        return self.post_render(context)
    def post_render(self, context): return self.args
    
def attribute(parser, token):
    return GenericNode(token.split_contents())

for tag in GChartWrapper.constants.TTAGSATTRS:
    register.tag(tag, attribute)

class ChartNode(Node):
    def __init__(self, tokens, nodelist):
        self.type = None
        self.tokens = []
        self.mode = None
        if tokens and len(tokens)>1:
            self.type = tokens[1]   
            if tokens[-2] == 'as':
                self.mode = tokens[-1]
                self.tokens = tokens[2:-2]
            else:
                self.tokens = tokens[2:]
        self.nodelist = nodelist
    def render(self, context): 
        args = []
        kwargs = {}
        for t in self.tokens:
            try:
                args.append(resolve_variable(t,context))
            except:        
                try:
                    args.append(float(t))
                except:
                    arg = str(t)
                    if arg.find('=')>-1:
                        k,v = arg.split('=')[:2]
                        kwargs[k] = v
                    else:
                        args.append(arg)   
        if len(args) == 1 and type(args[0]) in map(type,[[],()]):
            args = args[0]   
        if self.type in dir(GChartWrapper):
            chart = getattr(GChartWrapper,self.type)(args,**kwargs)
        elif self.type in GChartWrapper.constants.TYPES:
            chart = GChartWrapper.GChart(self.type,args,**kwargs)
        else:
            raise TypeError('Chart type %s not recognized'%self.type)
        imgkwargs = {}
        for n in self.nodelist:
            rend = n.render(context)           
            if type(rend) == type([]):
                if rend[0] == 'img':
                    for k,v in map(lambda x: x.split('='), rend[1:]):
                        imgkwargs[k] = v
                    continue
                if rend[0] == 'axes':
                    getattr(getattr(chart, rend[0]), rend[1])(*rend[2:])
                else:
                    if isinstance(rend[1], list) or isinstance(rend[1], tuple):
                        getattr(chart, rend[0])(*rend[1])
                    else:
                        getattr(chart, rend[0])(*rend[1:])
        if self.mode:
            if self.mode == 'img':  
                return chart.img(**imgkwargs)
            elif self.mode == 'url':  
                return str(chart)
            else:  
                context[self.mode] = chart
        else:
            return chart.img(**imgkwargs)

def make_chart(parser, token):
    nodelist = parser.parse(('endchart',))
    parser.delete_first_token()
    tokens = token.contents.split()
    return ChartNode(tokens,nodelist)
    
register.tag('chart', make_chart)

class FancyNode(GenericNode):
    cls = None
    def post_render(self,context):
        mode = None
        self.args = self.args[1:]
        if self.args[-2] == 'as':
            mode = self.args[-1]
            self.args = self.args[:-2]
        for n,arg in enumerate(self.args):
            self.args[n] = arg.replace('\\n','\n').replace('\\r','\r')
        G = self.cls(*self.args)
        if mode:
            if mode == 'img':  
                return G.img()
            if mode == 'url':  
                return str(G)
            else:  
                context[mode] = G
        else:
            return G.img()
        
class NoteNode(FancyNode):
    cls = GChartWrapper.Note
def note(parser, token):
    return NoteNode(token.split_contents())
register.tag(note)

class PinNode(FancyNode):
    cls = GChartWrapper.Pin
def pin(parser, token):
    return PinNode(token.split_contents())
register.tag(pin)

class TextNode(FancyNode):
    cls = GChartWrapper.Text
def text(parser, token):
    return TextNode(token.split_contents())
register.tag(text)

class BubbleNode(FancyNode):
    cls = GChartWrapper.Bubble
def bubble(parser, token):
    return BubbleNode(token.split_contents())
register.tag(bubble)