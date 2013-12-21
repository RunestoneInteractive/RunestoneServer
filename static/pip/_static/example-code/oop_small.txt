class A:
    x = 1
    y = 'hello'

class B:
    z = 'bye'

class C(A,B):
    def salutation(self):
        return '%d %s %s' % (self.x, self.y, self.z)

inst = C()
print(inst.salutation())
inst.x = 100
print(inst.salutation())
