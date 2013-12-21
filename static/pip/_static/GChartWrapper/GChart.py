# (modified by Philip Guo to remove utf-8 dependencies and unnecessary imports)

################################################################################
#  GChartWrapper - v0.8
#  Copyright (C) 2009  Justin Quick <justquick@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License version 3 as published
#  by the Free Software Foundation.
#
#  Thanks to anyone who does anything for this project.
#  If you have even the smallest revision, please email me at above address.
################################################################################
"""
GChartWrapper - Google Chart API Wrapper

The wrapper can render the URL of the Google chart based on your parameters.
With the chart you can render an HTML img tag to insert into webpages on the fly,
show it directly in a webbrowser, or save the chart PNG to disk. New versions
can generate PIL PngImage instances.

Example

    >>> G = GChart('lc',['simpleisbetterthancomplexcomplexisbetterthancomplicated'])
    >>> G.title('The Zen of Python','00cc00',36)
    >>> G.color('00cc00')
    >>> str(G)
    'http://chart.apis.google.com/chart?
        chd=e:simpleisbetterthancomplexcomplexisbetterthancomplicated
        &chs=300x150
        &cht=lc
        &chtt=The+Zen+of+Python'    
    >>> G.image() # PIL instance
    <PngImagePlugin.PngImageFile instance at ...>
    >>> 1#G.show() # Webbrowser open
    True
    >>> G.save('tmp.png') # Save to disk
    'tmp.png'

See tests.py for unit test and other examples
"""
from GChartWrapper.constants import *
from GChartWrapper.encoding import Encoder
from copy import copy

def lookup_color(color):
    """
    Returns the hex color for any valid css color name
    
    >>> lookup_color('aliceblue')
    'F0F8FF'
    """
    if color is None: return
    color = color.lower()
    if color in COLOR_MAP:
        return COLOR_MAP[color]
    return color

def color_args(args, *indexes):
    """
    Color a list of arguments on particular indexes
    
    >>> c = color_args([None,'blue'], 1)
    >>> c.next()
    None
    >>> c.next()
    '0000FF'
    """
    for i,arg in enumerate(args):
        if i in indexes:
            yield lookup_color(arg)
        else:
            yield arg


class Axes(dict):
    """
    Axes attribute dictionary storage

    Use this class via GChart(...).axes
    Methods are taken one at a time, like so:
    
    >>> G = GChart()
    >>> G.axes.type('xy')
    {}
    >>> G.axes.label(1,'Label1') # X Axis
    {}
    >>> G.axes.label(2,'Label2') # Y Axis
    {}
    """
    def __init__(self, parent):
        self.parent = parent
        self.data = {'ticks':[],'labels':[],'positions':[],
            'ranges':[],'styles':[]}
        dict.__init__(self)

    def tick(self, index, length):
        """
        Add tick marks in order of axes by width
        APIPARAM: chxtc     <axis index>,<length of tick mark>
        """
        assert int(length) <= 25, 'Width cannot be more than 25'
        self.data['ticks'].append('%s,%d'%(index,length))
        return self.parent
    
    def type(self, atype):
        """
        Define the type of axes you wish to use
        atype must be one of x,t,y,r
        APIPARAM: chxt
        """
        for char in atype:
            assert char in 'xtyr', 'Invalid axes type: %s'%char
        if not ',' in atype:
            atype = ','.join(atype)
        self['chxt'] = atype
        return self.parent
    __call__ = type
    
    def label(self, index, *args):
        """
        Label each axes one at a time
        args are of the form <label 1>,...,<label n>
        APIPARAM: chxl
        """
        self.data['labels'].append(
            str('%s:|%s'%(index, '|'.join(map(str,args)) )).replace('None','')
        )
        return self.parent
        
    def position(self, index, *args):
        """
        Set the label position of each axis, one at a time
        args are of the form <label position 1>,...,<label position n>
        APIPARAM: chxp
        """
        self.data['positions'].append(
            str('%s,%s'%(index, ','.join(map(str,args)))).replace('None','')
        )
        return self.parent
        
    def range(self, index, *args):
        """
        Set the range of each axis, one at a time
        args are of the form <start of range>,<end of range>,<interval>
        APIPARAM: chxr
        """
        self.data['ranges'].append('%s,%s'%(index,
                                    ','.join(map(smart_str, args))))
        return self.parent
        
    def style(self, index, *args):
        """
        Add style to your axis, one at a time
        args are of the form::
            <axis color>,
            <font size>,
            <alignment>,
            <drawing control>,
            <tick mark color>
        APIPARAM: chxs
        """
        args = color_args(args, 0)
        self.data['styles'].append(
            ','.join([str(index)]+list(map(str,args)))
        )
        return self.parent

    def render(self):
        """Render the axes data into the dict data"""
        for opt,values in self.data.items():
            if opt == 'ticks':
                self['chxtc'] = '|'.join(values)
            else:
                self['chx%s'%opt[0]] = '|'.join(values)
        return self    
        
class GChart(dict):
    """Main chart class

    Chart type must be valid for cht parameter
    Dataset can be any python iterable and be multi dimensional
    Kwargs will be put into chart API params if valid"""
    def __init__(self, ctype=None, dataset=[], **kwargs):
        self._series = kwargs.pop('series',None)
        self.lines,self.fills,self.markers,self.scales = [],[],[],[]
        self._geo,self._ld = '',''
        self._dataset = dataset
        dict.__init__(self)
        if ctype:
            self['cht'] = self.check_type(ctype)
        self._encoding = kwargs.pop('encoding', None)
        self._scale = kwargs.pop('scale', None)
        self._apiurl = kwargs.pop('apiurl', APIURL)
        for k in kwargs:
            assert k in APIPARAMS, 'Invalid chart parameter: %s' % k
        self.update(kwargs)
        self.axes = Axes(self)
    
    @classmethod
    def fromurl(cls, qs):
        """
        Reverse a chart URL or dict into a GChart instance
        
        >>> G = GChart.fromurl('http://chart.apis.google.com/chart?...')
        >>> G
        <GChartWrapper.GChart instance at...>
        >>> G.image().save('chart.jpg','JPEG')
        """
        if isinstance(qs, dict):
            return cls(**qs)
        return cls(**dict(parse_qsl(qs[qs.index('?')+1:])))
        
    ###################
    # Callables
    ###################
    def map(self, geo, country_codes):
        """
        Creates a map of the defined geography with the given country/state codes
        Geography choices are africa, asia, europe, middle_east, south_america, and world
        ISO country codes can be found at http://code.google.com/apis/chart/isocodes.html
        US state codes can be found at http://code.google.com/apis/chart/statecodes.html
        APIPARAMS: chtm & chld
        """
        assert geo in GEO, 'Geograpic area %s not recognized'%geo
        self._geo = geo
        self._ld = country_codes
        return self
        
    def level_data(self, *args):
        """
        Just used in QRCode for the moment
        args are error_correction,margin_size
        APIPARAM: chld
        """
        assert args[0].lower() in 'lmqh', 'Unknown EC level %s'%level
        self['chld'] = '%s|%s'%args
        return self
        
    def bar(self, *args):
        """
        For bar charts, specify bar thickness and spacing with the args
        args are <bar width>,<space between bars>,<space between groups>
        bar width can be relative or absolute, see the official doc
        APIPARAM: chbh
        """
        self['chbh'] = ','.join(map(str,args))
        return self
        
    def encoding(self, arg):
        """
        Specifies the encoding to be used for the Encoder
        Must be one of 'simple','text', or 'extended'
        """
        self._encoding = arg
        return self
        
    def output_encoding(self, encoding):
        """
        Output encoding to use for QRCode encoding
        Must be one of 'Shift_JIS','UTF-8', or 'ISO-8859-1'
        APIPARAM: choe
        """
        assert encoding in ('Shift_JIS','UTF-8','ISO-8859-1'),\
            'Unknown encoding %s'%encoding
        self['choe'] = encoding
        return self
        
    def scale(self, *args):
        """
        Scales the data down to the given size
        args must be of the form::
            <data set 1 minimum value>,
            <data set 1 maximum value>,
            <data set n minimum value>,
            <data set n maximum value>
        will only work with text encoding!
        APIPARAM: chds
        """
        self._scale =  [','.join(map(smart_str, args))]
        return self
        
    def dataset(self, data, series=''):
        """
        Update the chart's dataset, can be two dimensional or contain string data
        """
        self._dataset = data
        self._series = series
        return self
        
    def marker(self, *args):
        """
        Defines markers one at a time for your graph
        args are of the form::
            <marker type>,
            <color>,
            <data set index>,
            <data point>,
            <size>,
            <priority>
        see the official developers doc for the complete spec
        APIPARAM: chm
        """
        if len(args[0]) == 1:
            assert args[0] in MARKERS, 'Invalid marker type: %s'%args[0]
        assert len(args) <= 6, 'Incorrect arguments %s'%str(args)
        args = color_args(args, 1)
        self.markers.append(','.join(map(str,args)) )
        return self
        
    def margin(self, left, right, top, bottom, lwidth=0, lheight=0):
        """
        Set margins for chart area
        args are of the form::
            <left margin>,
            <right margin>,
            <top margin>,
            <bottom margin>|
            <legend width>,
            <legend height>
        
        APIPARAM: chma
        """
        self['chma'] = '%d,%d,%d,%d'  % (left, right, top, bottom)
        if lwidth or lheight:
            self['chma'] += '|%d,%d' % (lwidth, lheight)
        return self
    
    def line(self, *args):
        """
        Called one at a time for each dataset
        args are of the form::
            <data set n line thickness>,
            <length of line segment>,
            <length of blank segment>
        APIPARAM: chls
        """
        self.lines.append(','.join(['%.1f'%x for x in map(float,args)]))
        return self
        
    def fill(self, *args):
        """
        Apply a solid fill to your chart
        args are of the form <fill type>,<fill style>,...
        fill type must be one of c,bg,a
        fill style must be one of s,lg,ls
        the rest of the args refer to the particular style
        APIPARAM: chf
        """
        a,b = args[:2]
        assert a in ('c','bg','a'), 'Fill type must be bg/c/a not %s'%a
        assert b in ('s','lg','ls'), 'Fill style must be s/lg/ls not %s'%b
        if len(args) == 3:
            args = color_args(args, 2)
        else:
            args = color_args(args, 3,5)
        self.fills.append(','.join(map(str,args)))
        return self
        
    def grid(self, *args):
        """
        Apply a grid to your chart
        args are of the form::
            <x axis step size>,
            <y axis step size>,
            <length of line segment>,
            <length of blank segment>
            <x offset>,
            <y offset>
        APIPARAM: chg
        """
        grids =  map(str,map(float,args))
        self['chg'] = ','.join(grids).replace('None','')
        return self
        
    def color(self, *args):
        """
        Add a color for each dataset
        args are of the form <color 1>,...<color n>
        APIPARAM: chco
        """
        args = color_args(args, *range(len(args)))
        self['chco'] = ','.join(args)
        return self
        
    def type(self, type):
        """
        Set the chart type, either Google API type or regular name
        APIPARAM: cht
        """
        self['cht'] = self.check_type(str(type))
        return self
        
    def label(self, *args):
        """
        Add a simple label to your chart
        call each time for each dataset
        APIPARAM: chl
        """
        if self['cht'] == 'qr':
            self['chl'] = ''.join(map(str,args))
        else:
            self['chl'] = '|'.join(map(str,args))
        return self
        
    def legend(self, *args):
        """
        Add a legend to your chart
        call each time for each dataset
        APIPARAM: chdl
        """
        self['chdl'] = '|'.join(args)
        return self
        
    def legend_pos(self, pos):
        """
        Define a position for your legend to occupy
        APIPARAM: chdlp
        """
        assert pos in LEGEND_POSITIONS, 'Unknown legend position: %s'%pos
        self['chdlp'] = str(pos)
        return self
        
    def title(self, title, *args):
        """
        Add a title to your chart
        args are optional style params of the form <color>,<font size>
        APIPARAMS: chtt,chts
        """
        self['chtt'] = title
        if args:
            args = color_args(args, 0)
            self['chts'] = ','.join(map(str,args))
        return self

    def size(self,*args):
        """
        Set the size of the chart, args are width,height and can be tuple
        APIPARAM: chs
        """
        if len(args) == 2:
            x,y = map(int,args)
        else:
            x,y = map(int,args[0])
        self.check_size(x,y)
        self['chs'] = '%dx%d'%(x,y)
        return self
   
    def orientation(self, angle):
        """
        Set the chart dataset orientation
        angle is <angle in radians>
        APIPARAM: chp
        """
        self['chp'] = '%f'%angle
        return self
    position = orientation
    
    def render(self):
        """
        Renders the chart context and axes into the dict data
        """
        self.update(self.axes.render())
        encoder = Encoder(self._encoding, None, self._series)
        if not 'chs' in self:
            self['chs'] = '300x150'
        else:
            size = self['chs'].split('x')
            assert len(size) == 2, 'Invalid size, must be in the format WxH'
            self.check_size(*map(int,size))
        assert 'cht' in self, 'No chart type defined, use type method'
        self['cht'] = self.check_type(self['cht'])
        if ('any' in dir(self._dataset) and self._dataset.any()) or self._dataset:
            self['chd'] = encoder.encode(self._dataset)
        elif not 'choe' in self:
            assert 'chd' in self, 'You must have a dataset, or use chd'
        if self._scale:
            assert self['chd'].startswith('t'),\
                'You must use text encoding with chds'
            self['chds'] = ','.join(self._scale)
        if self._geo and self._ld:
            self['chtm'] = self._geo
            self['chld'] = self._ld
        if self.lines:
            self['chls'] = '|'.join(self.lines)
        if self.markers:
            self['chm'] = '|'.join(self.markers)
        if self.fills:
            self['chf'] = '|'.join(self.fills)

    ###################
    # Checks
    ###################
    def check_size(self,x,y):
        """
        Make sure the chart size fits the standards
        """
        assert x <= 1000, 'Width larger than 1,000'
        assert y <= 1000, 'Height larger than 1,000'
        assert x*y <= 300000, 'Resolution larger than 300,000'
        
    def check_type(self, type):
        """Check to see if the type is either in TYPES or fits type name

        Returns proper type
        """
        if type in TYPES:
            return type
        tdict = dict(zip(TYPES,TYPES))
        tdict.update({
            'line': 'lc',
            'bar': 'bvs',
            'pie': 'p',
            'venn': 'v',
            'scater': 's',
            'radar': 'r',
            'meter': 'gom',
        })
        assert type in tdict, 'Invalid chart type: %s'%type
        return tdict[type]

    #####################
    # Convience Functions
    #####################     
    def getname(self):
        """
        Gets the name of the chart, if it exists
        """
        return self.get('chtt','')

    def getdata(self):
        """
        Returns the decoded dataset from chd param
        """
        #XXX: Why again? not even sure decode works well
        return Encoder(self._encoding).decode(self['chd'])

    def _parts(self):
        return ('%s=%s'%(k,smart_str(v)) for k,v in self.items() if v)

    def __str__(self):
        return self.url
    
    def __repr__(self):
        return '<GChartWrapper.%s %s>'%(self.__class__.__name__,self)
    
    @property
    def url(self):
        """
        Returns the rendered URL of the chart
        """
        self.render()        
        return self._apiurl + '&'.join(self._parts()).replace(' ','+')


    # pgbovine - disable this function
    '''
    def show(self, *args, **kwargs):
        """
        Shows the chart URL in a webbrowser

        Other arguments passed to webbrowser.open
        """
        from webbrowser import open as webopen
        return webopen(str(self), *args, **kwargs)
    '''

    def save(self, fname=None):
        """
        Download the chart from the URL into a filename as a PNG

        The filename defaults to the chart title (chtt) if any
        """
        if not fname:
            fname = self.getname()
        assert fname != None, 'You must specify a filename to save to'
        if not fname.endswith('.png'):
            fname += '.png'
        try:
            urlretrieve(self.url, fname)
        except Exception:
            raise IOError('Problem saving %s to file'%fname)
        return fname

    def img(self, **kwargs):
        """ 
        Returns an XHTML <img/> tag of the chart

        kwargs can be other img tag attributes, which are strictly enforced
        uses strict escaping on the url, necessary for proper XHTML
        """       
        safe = 'src="%s" ' % self.url.replace('&','&amp;').replace('<', '&lt;')\
            .replace('>', '&gt;').replace('"', '&quot;').replace( "'", '&#39;')
        for item in kwargs.items():
            if not item[0] in IMGATTRS:
                raise AttributeError('Invalid img tag attribute: %s'%item[0])
            safe += '%s="%s" '%item
        return '<img %s/>'%safe

    def urlopen(self):
        """
        Grabs readable PNG file pointer
        """
        req = Request(str(self))
        try:
            return urlopen(req)
        except HTTPError:
            _print('The server couldn\'t fulfill the request.')
        except URLError:
            _print('We failed to reach a server.')

    def image(self):
        """
        Returns a PngImageFile instance of the chart

        You must have PIL installed for this to work
        """
        try:
            try:
                import Image
            except ImportError:
                from PIL import Image
        except ImportError:
            raise ImportError('You must install PIL to fetch image objects')
        try:
            from cStringIO import StringIO
        except ImportError:
            from StringIO import StringIO
        return Image.open(StringIO(self.urlopen().read()))

    def write(self, fp):
        """
        Writes out PNG image data in chunks to file pointer fp

        fp must support w or wb
        """
        urlfp = self.urlopen().fp
        while 1:
            try:
                fp.write(urlfp.next())
            except StopIteration:
                return

    # pgbovine - unnecessary
    '''
    def checksum(self):
        """
        Returns the unique SHA1 hexdigest of the chart URL param parts

        good for unittesting...
        """
        self.render()
        return new_sha(''.join(sorted(self._parts()))).hexdigest()
    '''

# Now a whole mess of convenience classes
# *for those of us who dont speak API*
class QRCode(GChart):
    def __init__(self, content='', **kwargs):
        kwargs['choe'] = 'UTF-8'
        if isinstance(content, str):
            kwargs['chl'] = quote(content).replace('%0A','\n')
        else:
            kwargs['chl'] = quote(content[0]).replace('%0A','\n')
        GChart.__init__(self, 'qr', None, **kwargs)
        
class _AbstractGChart(GChart):
    o,t = {},None
    def __init__(self, dataset, **kwargs):
        kwargs.update(self.o)
        GChart.__init__(self, self.t, dataset, **kwargs)


class Meter(_AbstractGChart):   o,t = {'encoding':'text'},'gom'
class Line(_AbstractGChart):     t = 'lc' 
class LineXY(_AbstractGChart):     t = 'lxy' 
class HorizontalBarStack(_AbstractGChart):     t = 'bhs' 
class VerticalBarStack(_AbstractGChart):     t = 'bvs' 
class HorizontalBarGroup(_AbstractGChart):     t = 'bhg' 
class VerticalBarGroup(_AbstractGChart):     t = 'bvg' 
class Pie(_AbstractGChart):     t = 'p' 
class Pie3D(_AbstractGChart):     t = 'p3' 
class Venn(_AbstractGChart):     t = 'v' 
class Scatter(_AbstractGChart):     t = 's' 
class Sparkline(_AbstractGChart):     t = 'ls' 
class Radar(_AbstractGChart):     t = 'r' 
class RadarSpline(_AbstractGChart):     t = 'rs' 
class Map(_AbstractGChart):     t = 't' 
class PieC(_AbstractGChart):     t = 'pc' 

########################################
# Now for something completely different
########################################
class Text(GChart):
    def render(self): pass
    def __init__(self, *args):
        GChart.__init__(self)
        self['chst'] = 'd_text_outline'
        args = list(map(str, color_args(args, 0, 3)))
        assert args[2] in 'lrh', 'Invalid text alignment'
        assert args[4] in '_b', 'Invalid font style'
        self['chld'] = '|'.join(args).replace('\r\n','|')\
            .replace('\r','|').replace('\n','|').replace(' ','+')

class Pin(GChart):
    def render(self): pass
    def __init__(self, ptype, *args):
        GChart.__init__(self)
        assert ptype in PIN_TYPES, 'Invalid type'
        if ptype == "pin_letter":
            args = color_args(args, 1,2)
        elif ptype == 'pin_icon':
            args = list(color_args(args, 1))
            assert args[0] in PIN_ICONS, 'Invalid icon name'
        elif ptype == 'xpin_letter':
            args = list(color_args(args, 2,3,4))
            assert args[0] in PIN_SHAPES, 'Invalid pin shape'
            if not args[0].startswith('pin_'):
                args[0] = 'pin_%s'%args[0] 
        elif ptype == 'xpin_icon':
            args = list(color_args(args, 2,3))
            assert args[0] in PIN_SHAPES, 'Invalid pin shape'
            if not args[0].startswith('pin_'):
                args[0] = 'pin_%s'%args[0] 
            assert args[1] in PIN_ICONS, 'Invalid icon name'
        elif ptype == 'spin':
            args = color_args(args, 2)
        self['chst'] = 'd_map_%s'%ptype
        self['chld'] = '|'.join(map(str, args)).replace('\r\n','|')\
            .replace('\r','|').replace('\n','|').replace(' ','+')
    def shadow(self):
        image = copy(self)
        chsts = self['chst'].split('_')
        chsts[-1] = 'shadow'
        image.data['chst'] = '_'.join(chsts)
        return image

class Note(GChart):
    def render(self): pass
    def __init__(self, *args):
        GChart.__init__(self)
        assert args[0] in NOTE_TYPES,'Invalid note type'
        assert args[1] in NOTE_IMAGES,'Invalid note image'
        if args[0].find('note')>-1:
            self['chst'] =  'd_f%s'%args[0]
            args = list(color_args(args, 3))
        else:
            self['chst'] = 'd_%s'%args[0]
            assert args[2] in NOTE_WEATHERS,'Invalid weather'
        args = args[1:]
        self['chld'] = '|'.join(map(str, args)).replace('\r\n','|')\
            .replace('\r','|').replace('\n','|').replace(' ','+')

class Bubble(GChart):
    def render(self): pass
    def __init__(self, btype, *args):
        GChart.__init__(self)
        assert btype in BUBBLE_TYPES, 'Invalid type'
        if btype in ('icon_text_small','icon_text_big'):
            args = list(color_args(args, 3,4))
            assert args[0] in BUBBLE_SICONS,'Invalid icon type'
        elif btype == 'icon_texts_big':
            args = list(color_args(args, 2,3))
            assert args[0] in BUBBLE_LICONS,'Invalid icon type'
        elif btype == 'texts_big':
            args = color_args(args, 1,2)
        self['chst'] = 'd_bubble_%s'%btype
        self['chld'] = '|'.join(map(str, args)).replace('\r\n','|')\
            .replace('\r','|').replace('\n','|').replace(' ','+')
    def shadow(self):
        image = copy(self)
        image.data['chst'] = '%s_shadow'%self['chst']
        return image


# added by pgbovine
class GraphViz(GChart):
    def render(self): pass
    def __init__(self, dot_string):
        GChart.__init__(self)
        self['chl'] = dot_string
        self['cht'] = 'gv'
