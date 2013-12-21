class A(object):
  bla = "A"
  def __init__(self):
    self.blb = "B"

  def x(self):
    self.bla = self.blb

a = A()

a.x()

print(a.bla)
print(A.bla)

