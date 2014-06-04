# Example module for Online Python Tutor
# Philip Guo
# 2013-08-03

# To get the Online Python Tutor backend to import this custom module,
# add its filename ('htmlexample_module') to the CUSTOM_MODULE_IMPORTS
# tuple in pg_logger.py

# To see an example of this module at work, write the following code in
# http://pythontutor.com/visualize.html
'''
from htmlexample_module import ColorTable

t = ColorTable(3, 4)

t.set_color(0, 0, 'red')
t.render_HTML()

t.set_color(1, 1, 'green')
t.render_HTML()

t.set_color(2, 2, 'blue')
t.render_HTML()

for i in range(3):
    for j in range(4):
        t.set_color(i, j, 'gray')
        t.render_HTML()
'''


# defines a simple table where you can set colors for individual rows and columns
class ColorTable:
    def __init__(self, num_rows, num_columns):
        self.num_rows = num_rows
        self.num_columns = num_columns

        # create a 2D matrix of empty strings
        self.table = []
        for i in range(self.num_rows):
            new_lst = ['' for e in range(self.num_columns)]
            self.table.append(new_lst)


    # color must be a legal HTML color string
    def set_color(self, row, column, color):
        assert 0 <= row < self.num_rows
        assert 0 <= column < self.num_columns
        self.table[row][column] = color


    # call this function whenever you want to render this table in HTML
    def render_HTML(self):
        # incrementally build up an HTML table string
        html_string = '<table>'

        for i in range(self.num_rows):
            html_string += '<tr>'
            for j in range(self.num_columns):
                color = self.table[i][j]
                if not color:
                    color = "white"
                html_string += '''<td style="width: 30px; height: 30px; border: 1px solid black;
                                  background-color: %s;"></td>''' % color
            html_string += '</tr>'

        html_string += '</table>'

        # then call the magic setHTML function
        setHTML(html_string)

