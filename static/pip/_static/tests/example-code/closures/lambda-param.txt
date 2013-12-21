def foo(x):
  bar(lambda y: x + y)

def bar(a):
  print(a(20))

foo(10)
