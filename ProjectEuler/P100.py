import psyco; psyco.full()

from math import sqrt
from sets import Set
from Utils import primes,gcd

def avg(a,b): return (a+b)/2.
def isqrt(n,maxiter=100,f=1):
    for i in range(maxiter):
        f = avg(f,n/f)
    return f

def isint(n): return int(n) == n

def isintsq(n): return isint(sqrt(n))

def isoddsquare(n,abc,tol=1e-9):
    return abs(sqrt(f(n,abc))%2-1) < tol

def f(n,(a,b,c)): return a*n*n+b*n+c

    
nmax = 1001000
ps = primes(nmax)
pset = Set(ps)

def getfactors(n):
   """Return list containing prime factors of a number."""
   if isprime(n) or n==1:
       return [n]
   for i in ps:
       if not n%i: # if goes evenly
           n = n/i
           return [i] + getfactors(n)
   return []

def isprime(n): return n in pset

def quadratic(a,b,c):
    n1 = -b
    disc = b*b-4*a*c
    if disc < 0: return None,None
    n2 = sqrt(disc)
    return (n1+n2)/(2.0*a),(n1-n2)/(2.0*a)

def brute():
    t =1000000000000L
    for i in xrange(20000):
        nt = t+i
        nb1,nb2 = quadratic(1,-1,-nt*(nt-1)/2)
        if isint(nb1):
            print nt,nb1

def brute2():
    t =1000000000000L
    b = 1000000000
    m = 1000000
    for i in xrange(b,2*b):
        nt = t+i
        nb1,nb2 = quadratic(1,-1,-nt*(nt-1)/2)
        inb1 = long(nb1)
        win = 1
        for nb in range(inb1-win,inb1+win+1):
            n = 2*nb*(nb-1)
            d = nt*(nt-1)
            if n==d:
                print nb,nt,n,d
                break
        if i % m == 0: print i
    return

brute2()


