# (modified by Philip Guo to remove utf-8 dependencies and unnecessary imports)
import sys

def _print(*args):
    for arg in args:
        sys.stdout.write('%s '%arg)
    sys.stdout.write('\n')

if sys.version.startswith('3'):
    PY_VER = '3.x'
    from urllib.parse import quote_plus,parse_qsl
    from urllib.request import Request, urlopen, urlretrieve
    #from hashlib import sha1
    #new_sha = lambda s: sha1(bytes(s,'utf-8'))
else:
    PY_VER = '2.x'
    from urllib import quote_plus,urlretrieve
    from urllib2 import urlopen, Request, URLError, HTTPError
    from cgi import parse_qsl
    #try: # >= 2.5
    #    from hashlib import sha1 as new_sha
    #except ImportError: # < 2.5
    #    from sha import new as new_sha

def quote(s):
    try:
        return  quote_plus(s.encode('utf-8'),'+.,:|/?&$=')
    except:
        return  quote_plus(s,'+.,:|/?&$=')

def smart_str(s):
    try:
        s = quote(s)
    except:
        pass
    # pgbovine - never use utf-8
    #if PY_VER == '2.x':
    #    return unicode(s).encode('utf-8') # Py2K
    return str(s)#.encode('utf-8') # Py3K

APIPARAMS = ('chxtc', 'chxt', 'chxp', 'chxs', 'chxr', 'chco', 'chtm', 'chld',
    'chts', 'chtt', 'chxl', 'chd', 'chf', 'chg', 'chl', 'chm', 'chp', 'chs',
    'cht', 'chls', 'chdlp', 'chds', 'chbh', 'chdl', 'choe', 'chst', 'chma')

MARKERS = 'acdostvVhxrRbBDF'

TYPES = ('bvs', 'p3', 'qr', 'lc', 'p', 'bhg', 'pc', 's', 'r', 'rs', 'bvg', 't',
    'v', 'lxy', 'bhs', 'gom', 'ls')

IMGATTRS = ('title','alt','align','border','height','width','ismap','longdesc',
'usemap','id','class','style','lang','xml:lang','onclick','ondblclick','onmousedown',
'onmouseup','onmouseover','onmousemove','onmouseout','onkeypress','onkeydown','onkeyup')

GEO = ('africa','asia','europe','middle_east','south_america','usa','world')

TTAGSATTRS = ('label','title','color','line','grid','bar','marker','fill','legend','axes',
'encoding','scale','size','type','dataset','img','map','bar_width_spacing',
'legend_pos','output_encoding','level_data')

APIURL = 'http://chart.apis.google.com/chart?' 

COLOR_MAP = {
    'aliceblue': 'F0F8FF',
    'antiquewhite': 'FAEBD7',
    'aqua': '00FFFF',
    'aquamarine': '7FFFD4',
    'azure': 'F0FFFF',
    'beige': 'F5F5DC',
    'bisque': 'FFE4C4',
    'black': '000000',
    'blanchedalmond': 'FFEBCD',
    'blue': '0000FF',
    'blueviolet': '8A2BE2',
    'brown': 'A52A2A',
    'burlywood': 'DEB887',
    'cadetblue': '5F9EA0',
    'chartreuse': '7FFF00',
    'chocolate': 'D2691E',
    'coral': 'FF7F50',
    'cornflowerblue': '6495ED',
    'cornsilk': 'FFF8DC',
    'crimson': 'DC143C',
    'cyan': '00FFFF',
    'darkblue': '00008B',
    'darkcyan': '008B8B',
    'darkgoldenrod': 'B8860B',
    'darkgray': 'A9A9A9',
    'darkgreen': '006400',
    'darkkhaki': 'BDB76B',
    'darkmagenta': '8B008B',
    'darkolivegreen': '556B2F',
    'darkorange': 'FF8C00',
    'darkorchid': '9932CC',
    'darkred': '8B0000',
    'darksalmon': 'E9967A',
    'darkseagreen': '8FBC8F',
    'darkslateblue': '483D8B',
    'darkslategray': '2F4F4F',
    'darkturquoise': '00CED1',
    'darkviolet': '9400D3',
    'deeppink': 'FF1493',
    'deepskyblue': '00BFFF',
    'dimgray': '696969',
    'dodgerblue': '1E90FF',
    'firebrick': 'B22222',
    'floralwhite': 'FFFAF0',
    'forestgreen': '228B22',
    'fuchsia': 'FF00FF',
    'gainsboro': 'DCDCDC',
    'ghostwhite': 'F8F8FF',
    'gold': 'FFD700',
    'goldenrod': 'DAA520',
    'gray': '808080',
    'green': '008000',
    'greenyellow': 'ADFF2F',
    'honeydew': 'F0FFF0',
    'hotpink': 'FF69B4',
    'indianred ': 'CD5C5C',
    'indigo  ': '4B0082',
    'ivory': 'FFFFF0',
    'khaki': 'F0E68C',
    'lavender': 'E6E6FA',
    'lavenderblush': 'FFF0F5',
    'lawngreen': '7CFC00',
    'lemonchiffon': 'FFFACD',
    'lightblue': 'ADD8E6',
    'lightcoral': 'F08080',
    'lightcyan': 'E0FFFF',
    'lightgoldenrodyellow': 'FAFAD2',
    'lightgrey': 'D3D3D3',
    'lightgreen': '90EE90',
    'lightpink': 'FFB6C1',
    'lightsalmon': 'FFA07A',
    'lightseagreen': '20B2AA',
    'lightskyblue': '87CEFA',
    'lightslategray': '778899',
    'lightsteelblue': 'B0C4DE',
    'lightyellow': 'FFFFE0',
    'lime': '00FF00',
    'limegreen': '32CD32',
    'linen': 'FAF0E6',
    'magenta': 'FF00FF',
    'maroon': '800000',
    'mediumaquamarine': '66CDAA',
    'mediumblue': '0000CD',
    'mediumorchid': 'BA55D3',
    'mediumpurple': '9370D8',
    'mediumseagreen': '3CB371',
    'mediumslateblue': '7B68EE',
    'mediumspringgreen': '00FA9A',
    'mediumturquoise': '48D1CC',
    'mediumvioletred': 'C71585',
    'midnightblue': '191970',
    'mintcream': 'F5FFFA',
    'mistyrose': 'FFE4E1',
    'moccasin': 'FFE4B5',
    'navajowhite': 'FFDEAD',
    'navy': '000080',
    'oldlace': 'FDF5E6',
    'olive': '808000',
    'olivedrab': '6B8E23',
    'orange': 'FFA500',
    'orangered': 'FF4500',
    'orchid': 'DA70D6',
    'palegoldenrod': 'EEE8AA',
    'palegreen': '98FB98',
    'paleturquoise': 'AFEEEE',
    'palevioletred': 'D87093',
    'papayawhip': 'FFEFD5',
    'peachpuff': 'FFDAB9',
    'peru': 'CD853F',
    'pink': 'FFC0CB',
    'plum': 'DDA0DD',
    'powderblue': 'B0E0E6',
    'purple': '800080',
    'red': 'FF0000',
    'rosybrown': 'BC8F8F',
    'royalblue': '4169E1',
    'saddlebrown': '8B4513',
    'salmon': 'FA8072',
    'sandybrown': 'F4A460',
    'seagreen': '2E8B57',
    'seashell': 'FFF5EE',
    'sienna': 'A0522D',
    'silver': 'C0C0C0',
    'skyblue': '87CEEB',
    'slateblue': '6A5ACD',
    'slategray': '708090',
    'snow': 'FFFAFA',
    'springgreen': '00FF7F',
    'steelblue': '4682B4',
    'tan': 'D2B48C',
    'teal': '008080',
    'thistle': 'D8BFD8',
    'tomato': 'FF6347',
    'turquoise': '40E0D0',
    'violet': 'EE82EE',
    'wheat': 'F5DEB3',
    'white': 'FFFFFF',
    'whitesmoke': 'F5F5F5',
    'yellow': 'FFFF00',
    'yellowgreen': '9ACD32'
}
PIN_TYPES = ('pin_letter','pin_icon','xpin_letter','xpin_icon','spin')
PIN_ICONS = ('home', 'home', 'WC', 'WCfemale', 'WCmale', 'accomm', 'airport',
    'baby', 'bar', 'bicycle', 'bus', 'cafe', 'camping', 'car', 'caution', 'cinema',
    'computer', 'corporate', 'dollar', 'euro', 'fire', 'flag', 'floral', 'helicopter',
    'home', 'info', 'landslide', 'legal', 'location', 'locomotive', 'medical',
    'mobile', 'motorcycle', 'music', 'parking', 'pet', 'petrol', 'phone', 'picnic',
    'postal', 'pound', 'repair', 'restaurant', 'sail', 'school', 'scissors', 'ship',
    'shoppingbag', 'shoppingcart', 'ski', 'snack', 'snow', 'sport', 'swim', 'taxi',
    'train', 'truck', 'wheelchair', 'yen')
PIN_SHAPES = ('pin','star','sleft','sright')
NOTE_TYPES = ('note_title','note','weather')
NOTE_IMAGES = ('arrow_d', 'balloon', 'pinned_c', 'sticky_y', 'taped_y', 'thought')
NOTE_WEATHERS = ('clear-night-moon', 'cloudy-heavy', 'cloudy-sunny', 'cloudy',
    'rain', 'rainy-sunny', 'snow', 'snowflake', 'snowy-sunny', 'sunny-cloudy',
    'sunny', 'thermometer-cold', 'thermometer-hot', 'thunder', 'windy')
BUBBLE_TYPES = ('icon_text_small','icon_text_big','icon_texts_big','texts_big')
BUBBLE_SICONS = ('WC', 'WCfemale', 'WCmale', 'accomm', 'airport', 'baby', 'bar',
    'bicycle', 'bus', 'cafe', 'camping', 'car', 'caution', 'cinema', 'computer',
    'corporate', 'dollar', 'euro', 'fire', 'flag', 'floral', 'helicopter', 'home',
    'info', 'landslide', 'legal', 'location', 'locomotive', 'medical', 'mobile',
    'motorcycle', 'music', 'parking', 'pet', 'petrol', 'phone', 'picnic', 'postal',
    'pound', 'repair', 'restaurant', 'sail', 'school', 'scissors', 'ship', 'shoppingbag',
    'shoppingcart', 'ski', 'snack', 'snow', 'sport', 'swim', 'taxi', 'train',
    'truck', 'wheelchair', 'yen')
BUBBLE_LICONS = ('beer', 'bike', 'car', 'house', 'petrol', 'ski', 'snack')
LEGEND_POSITIONS = ('b','t','r','l','bv','tv')
