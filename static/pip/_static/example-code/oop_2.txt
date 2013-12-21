# The __init__ 'constructor' - object-oriented programming intro
# Adapted from MIT 6.01 course notes (Section 3.5)
# http://mit.edu/6.01/mercurial/spring10/www/handouts/readings.pdf

class Staff601:
    course = '6.01'
    building = 34
    room = 501

    def __init__(self, name, role, years, salary):
      self.name = name
      self.role = role
      self.age = years
      self.salary = salary

    def salutation(self):
        return self.role + ' ' + self.name

pat = Staff601('Pat', 'Professor', 60, 100000)
print(pat.salutation())

