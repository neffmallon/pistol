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
    #n2 = sqrt(disc)
    n2 = isqrt(disc)
    return (n1+n2)/(2*a),(n1-n2)/(2*a)

def brute():
    t =1000000000000L
    m = 1000000
    for i in xrange(m):
        nt = t+i
        nb1,nb2 = quadratic(2,-2,-nt*(nt-1))
        nb = int(nb1)
        if isint(nb1):
            print nt,nb,2*nb*(nb-1)==nt*(nt-1)
    return

def brute2():
    t =1000000000000L
    b = 1000000000
    m = 1000000
    for i in xrange(2*b):
        nt = t+i
        nb1,nb2 = quadratic(2,-2,-nt*(nt-1))
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

def clever2():
    from pylab import *
    thou = 1000
    mill = 1000000
    bill = 1000000000
    trill = 1000000000000L
    nmax = thou
    # We want to find the solutions where 2*k^2-1 is a perfect square
    ks = []
    for k in range(2,mill):
        s = sqrt(2*k*k-1)
        i = long(s)
        if i == s and i%2==1:
            nt = (1 + i)/2
            nb = (1 + sqrt(1+2*nt*(nt-1)))/2
            print k,nt,nb,2.*nb*(nb-1)/(nt*(nt-1))
            ks.append(i)
    plot(ks)
    show()
    

def clever():
    t =1000000000000L
    b = 1000000000
    m = 1000000
    for i in xrange(2*b):
        nt = t+i
        q = 2*nt*nt - 2*nt + 1
        qrt = long(sqrt(q))
        sqs = []
        win = 1
        #print "Seeking sqrt of ",q
        #print "Approximate sqrt = ",qrt,qrt*qrt
        for i in range(-win,win+1):
            qrti = qrt + i
            qrti2 = qrti*qrti
            if q == qrti2:
                "Solution found: nt = ",nt
                "sqrt(2nt^2-2nt+1) = ",qrti
                break
            elif qrti2 > q:
                break
            #print "!= ",qrti2
clever()
