def foo(y):
    def bar(x):
        return x + y
    return bar

def foo_deux(y):
    def bar_deux(x):
        return x + y
    return bar_deux

b = foo(1)
b_deux = foo_deux(1000)

b(2)    
b_deux(2000)
