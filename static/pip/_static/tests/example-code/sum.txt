# Higher-order functions
# Adapted from MIT 6.01 course notes (Section A.2.2)
# http://mit.edu/6.01/mercurial/spring10/www/handouts/readings.pdf

def summation(low, high, f, next):
    s = 0
    x = low
    while x <= high:
        s = s + f(x)
        x = next(x)
    return s

def sumsquares(low, high):
    return summation(low, high, lambda x: x**2, lambda x: x+1)

print(sumsquares(1, 10))
