# Philip's 10-minute intro to Python

# numbers!
age = 26
pi = 3.14159

# strings!
s = 'Rutherford Birchard Hayes'
tokens = s.split()
firstName = tokens[0]
middleName = tokens[1]
lastName = tokens[2]
s2 = firstName + ' ' + middleName + ' ' + lastName

# 'if' statement - indentation matters!
if (s == s2):
    print('yes!!!')
else:
    print('nooooooo')

# list (mutable sequence)
beatles = ['John', 'Paul', 'George']
beatles.append('Ringo')

# 'for' loop - indentation matters!
for b in beatles:
    print('Hello ' + b)

# tuple (immutable sequence)
ages = (18, 21, 28, 21, 22, 18, 19, 34, 9)

# set (no order, no duplicates)
uniqueAges = set(ages)
uniqueAges.add(18) # already in set, no effect
uniqueAges.remove(21)

# no guaranteed order when iterating over a set
for thisAge in uniqueAges:
    print(thisAge)

# testing set membership
if 18 in uniqueAges:
    print('There is an 18-year-old present!')

# sorting
beatles.sort() # in-place
orderedUniqueAges = sorted(uniqueAges) # new list

# dict - mapping unique keys to values
netWorth = {}
netWorth['Donald Trump'] = 3000000000
netWorth['Bill Gates'] = 58000000000
netWorth['Tom Cruise'] = 40000000
netWorth['Joe Postdoc'] = 20000

# iterating over key-value pairs:
for (person, worth) in netWorth.items():
    if worth < 1000000:
        print('haha ' + person + ' is not a millionaire')

# testing dict membership
if 'Tom Cruise' in netWorth:
    print('show me the money!')
