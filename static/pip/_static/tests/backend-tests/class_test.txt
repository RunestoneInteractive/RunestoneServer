class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return "(%d, %d)" % (self.x, self.y)

p = Point(1, 2)
print(p)
p2 = Point(3, -4)
print(p2)

