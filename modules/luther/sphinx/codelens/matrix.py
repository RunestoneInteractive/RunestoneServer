#  m a t r i x . p y
#
#  Support for 2d matrix that renders to an HTML table
#
#  Chris Meyers. 09/25/2013
#

dftTableAttr = 'cellspacing="0" cellpadding="10"'

class Matrix :
    def __init__ (self, nrows=1, ncols=1, data=None,
                  dftFormat="", dftStyle="", title="",
                  tableAttr=dftTableAttr, tableHeaders=None,
                  Expand=True) :
        self.nrows = nrows
        self.ncols = ncols
        self.values = {}
        self.expanded = Expand
        if Expand :
            # get attributes only on the main Matrix
            self.dftFormat    = dftFormat
            self.dftStyle     = dftStyle
            self.title        = title
            self.tableAttr    = tableAttr
            self.tableHeaders = tableHeaders
            self.format = Matrix(nrows, ncols, Expand=False)
            self.style  = Matrix(nrows, ncols, Expand=False)
        if data :
            if type(data) == type({}) : data=dictToLol(data)
            if type(data) == type([]) :
                self.populate(data)

    def __getitem__(self, coords) :
        row, col = coords
        return self.values.get((row,col))

    def __setitem__(self, coords, value) :
        row, col = coords
        self.values[(row,col)] = value
        self.nrows = max(self.nrows,row+1)
        self.ncols = max(self.ncols,col+1)
        if self.expanded :
            self.format.nrows = self.nrows
            self.format.ncols = self.ncols
            self.style.nrows  = self.nrows
            self.style.ncols  = self.ncols
        return value

#===========================================

    def setrowVals(self, row, values) :
        "set each column to a seperate value"
        col = 0
        for col in range(len(values)) :
            self.__setitem__((row,col),values[col])
            col += 1

    def setrowVal(self, row, value) :
        "set all columns to the same value"
        col = 0
        while col < self.ncols :
            self.__setitem__((row,col),value)
            col += 1

    def getrow (self, row) :
        vals = []
        for c in range(self.ncols) :
            vals.append(self.__getitem__( (row,c) ))
        return vals

#===========================================

    def setcolVals(self, col, values) :
        "set each row to a seperate value"
        row = 0
        for row in range(len(values)) :
            self.__setitem__((row,col),values[row])
            row += 1

    def setcolVal(self, col, value) :
        "set all rowumns to the same value"
        row = 0
        while row < self.nrows :
            self.__setitem__((row,col),value)
            row += 1

    def getcol (self, col) :
        vals = []
        for r in range(self.nrows) :
            vals.append(self.__getitem__( (r,col) ))
        return vals

#===========================================

    def populate(self, lists) :
        "Fill self from a list of lists"
        nRows = len(lists)
        nCols = max([len(l) for l in lists])
        for row in range(len(lists)) :
            vals = lists[row]
            if type(vals) != list : vals = [vals] # make sing col
            self.setrowVals(row, vals)

    def renderHtml(self,wrap=None) :
        lins = ["","<table %s>" % self.tableAttr]
        if self.title : lins[0] = "<div>%s</div>" % self.title
        headers = self.tableHeaders
        if headers :
            lins.append("<tr><th>"+"</th><th>".join(map(str,headers))+
                        "</th></tr>")
        for row in range(self.nrows) :
            rowLin = ["  <tr>"]
            vals = self.getrow(row)
            if self.format : formats = self.format.getrow(row)
            else           : formats = ['']*self.ncols
            if self.style  : styles  = self.style.getrow(row)
            else           : styles  = ['']*self.ncols
            for c in range(self.ncols) :
                val = vals[c]; style=styles[c]; format=formats[c]
                if val == None : val = ""
                if not format : format = self.dftFormat
                if format :
                    if type(format)==type("") : val = format % val
                    else                      : val = format(val)
                if not style : style = self.dftStyle
                if style : cell = '<td style="%s">%s</td>' % (style,val)
                else     : cell = '<td>%s</td>' % val
                if wrap and c>0 and c%wrap==0 : cell="</tr><tr>"+cell
                rowLin.append(cell)
            rowLin.append("</tr>")
            lins.append("".join(rowLin))
        lins.append("</table>")
        return "\n".join(lins)

    def __str__ (self) :
        return "Matrix-%dx%d" % (self.nrows,self.ncols)

#===========================================

typeSeq = (type([]), type((1,2)))

def dictToLol(dic) :
    "Convert dict to a list of lists"
    keys = dic.keys(); keys.sort()
    lists = []
    for key in keys :
        val = dic[key]
        if type(val) not in typeSeq : val = [val]
        lists.append([key]+list(val))
    return lists

