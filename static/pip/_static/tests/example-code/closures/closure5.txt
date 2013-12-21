def f(x):
    def g(y, z):
        if z == 0:
            return y
        return g(x+y+z, z-1)
    return lambda: g(0, x)

foo = f(3)
bar = f(4)
baz = foo() + bar()
