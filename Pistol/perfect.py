#!/usr/bin/env python
"Play with perfect numbers and primes"

from time import time
from operator import add
from random import randrange

def square(a): return a*a

def smallest_divisor(n):
    for i in range(2,n+1):
        if square(i) > n: return n
        if n%i==0: return i
    return n

def expmod(b,e,m):
    "Returns b^e mod m"
    if e==0: return 1
    if iseven(e): return (square(expmod(b,e/2,m)) % m)
    return (b*expmod(b,e-1,m) % m)

def isprime(n): return smallest_divisor(n)==n

def fermattest(n):
    a = randrange(2,n)
    return expmod(a,n,n)==a

def probprime(n,times=100):
    "Probabalistic test for primes"
    for i in range(times):
        if fermattest(n)==0: return 0
    return 1

# The known Mersenne primes are (p, for 2^p-1)
marsennes = [
    2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 127, 521, 607, 1279, 2203, 2281,
    3217, 4253, 4423, 9689, 9941, 11213, 19937, 21701, 23209, 44497,
    86243, 110503, 132049, 216091, 756839, 859433, 1257787, 1398269,
    2976221, 3021377, 6972593, 13466917, 20996011]

def lucas(p):
    "Test whether 2^p-1 is a Mersenne prime"
    s = 4
    val = pow(2,p)-1
    for i in range(3,p+1): s = (s*s-2)%val
    return not s

def lucas_gmp(p):
    "Test whether 2^p-1 is a Mersenne prime"
    from gmpy import mpz
    s = mpz('4')
    val = pow(2,p)-1
    for i in range(3,p+1): s = (s*s-2)%val
    return not s

def sum(l): return reduce(add,l + [0])  # [0] handles empty list
def isfactor(i,n): return (n%i == 0)
def findperfects(l): return [i for i in l if isperfect(i)]
def factors(n): return [i for i in range(1,n) if isfactor(i,n)]
def isperfect(n): return sum(factors(n)) == n
def iseven(n): return (n%2==0)
def findprimes(l): return [i for i in l if isprime(i)]
# This is the most direct way of computing the perfects:
def formperf(n):
    return [pow(2,i-1)*(pow(2,i)-1) for i in range(2,n) if isprime(pow(2,i)-1)]

def isprimelist(n):
    "faster than findprimes(n) for finding all primes < n"
    isprime = [1]*(n+1)
    isprime[0] = isprime[1] = 0
    for i in range(2,n):
        for j in range(2,n):
            if i*j > n: break
            isprime[i*j] = 0
    return isprime

def sieve(n): # Sieve of Eratosthenes
    isprime = isprimelist(n)
    return [i for i in range(2,n+1) if isprime[i]]

def primedens(n):
    "the number of primes less than a number"
    isprime = isprimelist(n)
    return [sum(isprime[:i]) for i in range(2,n)]

def plotprimedens(n):
    pd = primedens(n)
    steps = range(len(pd))
    from biggles import FramedPlot, Curve
    g = FramedPlot()
    g.add(Curve(steps,pd))
    g.show()
    return


# This was the original version, but I have depricated it since the Sussman
#  Abelson version is so much faster
def isprime_slo(n): return len(factors(n)) == 1

# Some random routines written for fun, mostly from Sussman/Abelson
def ipow(b,n):
    # integer power routine, from Sussman/Abelson. Almost as fast as
    #  the C-version in Python. Scales log n
    if n == 0: return 1
    elif iseven(n): return square(ipow(b,n/2))
    return b*ipow(b,n-1)

def close_enough(a,b,tol=1e-9): return abs(a-b)<tol
def mysqrt(n,guess=1.,tol=1e-9):
    if close_enough(n,square(guess),tol): return guess
    return mysqrt(n,0.5*(guess+n/guess))

if __name__ == '__main__':
    #print isperfect(6)
    #print isperfect(7)
    #print isperfect(28)
    #print findperfects(range(1,500))
    #print findprimes(range(1,500))
    #print factors(496)
    #print sieve(500)
    #print primedens(1000)
    #plotprimedens(10000)
    from gmpy import mpz
    i=marsennes[20] ; print mpz('2')**i-1,lucas_gmp(i)
