# 'nonlocal' keyword is only in Python 3
def outer():
    x = 1
    def inner():
        nonlocal x
        x = 2
        y = x
        print("inner:", x, y)
    inner()
    print("outer:", x)

outer()
