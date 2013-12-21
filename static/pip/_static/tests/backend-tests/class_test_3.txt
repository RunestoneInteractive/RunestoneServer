class Staff601:
    course = '6.01'
    building = 34
    room = 501

pat = Staff601()
print(pat.course)

pat.name = 'Pat'
pat.age = 60
pat.role = 'Professor'

print(pat.building)
pat.building = 32
print(pat.building)

