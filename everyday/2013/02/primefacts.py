__author__ = 'bmiller'

import math
import time

def get_next_prime_factor(n):
    if n % 2 == 0:
        return 2

    for x in xrange(3,n//2,2):
        if n % x == 0:
            return x

    return n


def get_prime_factors(n):
    factors = []

    while n > 1:
        factor = get_next_prime_factor(n)
        factors.append(factor)
        n = n // factor

    return factors

print get_prime_factors(14421)

#start = time.time()
#print get_prime_factors(68718952447)
#end = time.time()
#print end-start

#print get_prime_factors(1125899839733759)
def get_prime_factors(num,fact):
    if fact > num:
        return []
    if num % fact == 0:
        return [fact] + get_prime_factors(num // fact, 2)
    return get_prime_factors(num, fact+1)

#print get_prime_factors(1073676287,2)


def primegen(n):
    yield 2

    primes = []
    for m in range(3,n,2):
        if all(m%p for p in primes):
            primes.append(m)
            yield m

primelist = primegen(100)
print list(primelist)

def firstn(n):
    num = 0
    while num < n:
        yield num
        num = num + 1

x = firstn(10)
print(x)
