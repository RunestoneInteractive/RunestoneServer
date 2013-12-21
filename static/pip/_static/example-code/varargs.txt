# Demonstrate *args and **kwargs
def f1(a, b, *rest):
    pass

f1(1, 2)
f1(1, 2, 3, 4, 5, 6, 7)

def f2(a, b, **kwrest):
    pass

f2(1, 2, name='Bob', age=38)

def f3(a, b, *rest, **kwrest):
    pass

f3(1, 2, 3, 4, name='Bob', age=38)
