# Object-oriented programming intro
# Adapted from MIT 6.01 course notes (Section 3.5)
# http://mit.edu/6.01/mercurial/spring10/www/handouts/readings.pdf

class Staff601:
    course = '6.01'
    building = 34
    room = 501

    def salutation(self):
        return self.role + ' ' + self.name

pat = Staff601()
print(pat.course)

pat.name = 'Pat'
pat.age = 60
pat.role = 'Professor'

print(pat.building)
pat.building = 32
print(pat.building)

print(pat.salutation())
print(Staff601.salutation(pat))
