def f(x):
    def g(y):
        return x + y
    return g

g1 = f(1)
g2 = f(2)
g1(3) + g2(4)
