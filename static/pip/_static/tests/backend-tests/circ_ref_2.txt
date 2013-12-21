# true indirect circular reference

x = [1, 2]
y = [3, 4, x]
x.append(y)

