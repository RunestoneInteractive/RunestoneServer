def foo(y):
    def bar(x):
        return x + y
    return bar

b = foo(1)
b(2)
