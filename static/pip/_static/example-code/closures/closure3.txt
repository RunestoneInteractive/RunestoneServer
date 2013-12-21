def foo(x):
    def bar(y):
        def baz(z):
            return len(x) + len(y) + len(z)
        return baz
    return bar([4,5,6,7])

l = [1,2,3]
x = foo(l)
x([8,9,10,11,12])
