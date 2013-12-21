# Tutorial code from Prof. Peter Wentworth
# Rhodes University, South Africa (http://www.ru.ac.za/)

# Demonstrate recursion that throws an exception
# at its base case, and the tracing of try ... finally.
#
# How many "survived!" messages will be printed???

def f(n):
    try:
        x = 10 / n
        print("x is " + str(x))
        f(n-1)
        print("survived!")
    finally:
        print("Bye from f where n = " + str(n))

f(4)
