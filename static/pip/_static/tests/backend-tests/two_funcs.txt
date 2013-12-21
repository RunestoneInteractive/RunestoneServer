def add(a, b, c):
  d = a + b
  return c + d

def double_add(a, b, c):
  x = add(a, b, c)
  y = add(a, b, c)
  return x + y

x = 5
y = 10
z = x * y
print(add(x, y, z))
print(double_add(x, y, z))
