# not a true circular reference

a = [10, 20, 30]
b = a
c = [10, 20, 30]
d = (a, b, c)

