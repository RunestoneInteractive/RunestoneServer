input = [("Mary", 27), ("Joe", 30), ("Ruth", 43), ("Bob", 17), ("Jenny", 22)]

youngPeople = []

for (person, age) in input:
    if age < 30:
        youngPeople.append(person)
    else:
        print("HAHA " + person + " is too old!")

print("There are " + str(len(youngPeople)) + " young people")
