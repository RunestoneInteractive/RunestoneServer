input = 'John,Doe,1984,4,1,male'

tokens = input.split(',')
firstName = tokens[0]
lastName = tokens[1]
birthdate = (int(tokens[2]), int(tokens[3]), int(tokens[4]))
isMale = (tokens[5] == 'male')

print('Hi ' + firstName + ' ' + lastName)
