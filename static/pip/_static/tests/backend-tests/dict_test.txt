x = {1 : 2}
x[('tup', 'le')] = set([1, 2, 3])

def foo():
  local_x = {1 : 2}
  local_y = {}
  local_y[('tup', 'le')] = set([1, 2, 3])
  print("hello", list(local_y.values()))

foo()
