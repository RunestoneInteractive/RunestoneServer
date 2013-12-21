# Inheritance - object-oriented programming intro
# Adapted from MIT 6.01 course notes (Section 3.5)
# http://mit.edu/6.01/mercurial/spring10/www/handouts/readings.pdf

class Staff601:
    course = '6.01'
    building = 34
    room = 501

    def giveRaise(self, percentage):
        self.salary = self.salary + self.salary * percentage

class Prof601(Staff601):
    salary = 100000

    def __init__(self, name, age):
        self.name = name
        self.giveRaise((age - 18) * 0.03)

    def salutation(self):
        return self.role + ' ' + self.name

pat = Prof601('Pat', 60)

