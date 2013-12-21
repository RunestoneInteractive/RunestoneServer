coding = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
ecoding = coding + '-.'
codeset =  {
    'simple': {
        'coding': coding,
        'max_value':  61,
        'char': ',',
        'dchar': '',
        'none': '_',
        'value': lambda x: coding[x]
    },
    'text': {
        'coding': '',
        'max_value':  100,
        'none': '-1',
        'char': '|',
        'dchar': ',',
        'value': lambda x: '%.1f' % float(x)
    },
    'extended': {
        'coding':  ecoding,
        'max_value':  4095,
        'none':  '__',
        'dchar': '',
        'char': ',',
        'value': lambda x: '%s%s' % \
             (ecoding[int(float(x) / 64)], ecoding[int(x % 64)])
    }
}

class Encoder:
    """Data encoder that handles simple,text, and extended encodings

    Based on javascript encoding algorithm and pygooglecharts"""
    def __init__(self, encoding=None, scale=None, series=''):
        self.series = series or ''
        if encoding is None:
            encoding = 'text'
        assert(encoding in ('simple','text','extended')),\
            'Unknown encoding: %s'%encoding
        self.encoding = encoding
        self.scale = scale
        self.codeset = codeset[encoding]

    def scalevalue(self, value):
        return value # one day...
        if self.encoding != 'text' and self.scale and \
                isinstance(value, int) or isinstance(value, float):
            if type(self.scale) == type(()):
                lower,upper = self.scale
            else:
                lower,upper = 0,float(self.scale)
            value = int(round(float(value - lower) * \
                            self.codeset['max_value'] / upper))
        return min(value, self.codeset['max_value'])

    def encode(self,  *args, **kwargs):
        """Encode wrapper for a dataset with maximum value

        Datasets can be one or two dimensional
        Strings are ignored as ordinal encoding"""
        if isinstance(args[0], str):
            return self.encode([args[0]],**kwargs)
        elif isinstance(args[0], int) or isinstance(args[0], float):
            return self.encode([[args[0]]],**kwargs)
        if len(args)>1:
            dataset = args
        else:
            dataset = args[0]
        typemap = list(map(type,dataset))
        code = self.encoding[0]
        if type('') in typemap:
            data = ','.join(map(str,dataset))
        elif type([]) in typemap or type(()) in typemap:
            data = self.codeset['char'].join(map(self.encodedata, dataset))
        elif len(dataset) == 1 and hasattr(dataset[0], '__iter__'):
            data = self.encodedata(dataset[0])
        else:
            try:
                data = self.encodedata(dataset)
            except ValueError:
                data = self.encodedata(','.join(map(unicode,dataset)))
        if not '.' in data and code == 't':
            code = 'e'
        return '%s%s:%s'%(code,self.series,data)

    def encodedata(self, data):
        sub_data = []
        enc_size = len(self.codeset['coding'])
        for value in data:
            if value in (None,'None'):
                sub_data.append(self.codeset['none'])
            elif isinstance(value, str):
                sub_data.append(value)
            elif value >= -1:
                try:
                    sub_data.append(self.codeset['value'](self.scalevalue(value)))
                except:
                    raise ValueError('cannot encode value: %s'%value)
        return self.codeset['dchar'].join(sub_data)

    def decode(self, astr):
        e = astr[0]
        dec_data = []
        for data in astr[2:].split(self.codeset['char']):
            sub_data = []
            if e == 't':
                sub_data.extend(map(float, data.split(',')))
            elif e == 'e':
                flag = 0
                index = self.codeset['coding'].index
                for i in range(len(data)):
                    if not flag:
                        this,next = index(data[i]),index(data[i+1])
                        flag = 1
                        sub_data.append((64 * this) + next)
                    else: flag = 0
            elif e == 's':
                sub_data.extend(map(self.codeset['coding'].index, data))
            dec_data.append(sub_data)
        return dec_data

