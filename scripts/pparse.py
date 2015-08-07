__author__ = 'bmiller'
import re

class PTest:

    def parse_multiline_parsons(self, lines):
        current_block = []
        results = []
        for line in lines:
            if(line == '====='):
                results.append(self.convert_leading_whitespace_for_block(current_block))
                current_block = []
            else:
                current_block.append(line)
        results.append(self.convert_leading_whitespace_for_block(current_block))
        return "\n".join(results)

    def convert_leading_whitespace_for_block(self, block):
        whitespaceMatcher = re.compile("^\s*")
        initialWhitespace = whitespaceMatcher.match(block[0]).end()
        result = block[0]
        for line in block[1:]:
            result += '\\n' # not a line break...the literal characters \n
            result += line[initialWhitespace:]
        return result

tt = '''
x = 0
=====
for i in range(3):
   x = x + i
   y = 10
=====
print x
print y
'''

z = PTest()
zzz = z.parse_multiline_parsons(tt.split('\n'))
print type(zzz)
print zzz.split('\n')
print zzz

