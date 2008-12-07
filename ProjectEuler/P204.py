"""
A Hamming number is a positive number which has no prime factor larger
than 5. So the first few Hamming numbers are 1, 2, 3, 4, 5, 6, 8, 9,
10, 12, 15. There are 1105 Hamming numbers not exceeding 10^(8).

We will call a positive number a generalised Hamming number of type n,
if it has no prime factor larger than n. Hence the Hamming numbers are
the generalised Hamming numbers of type 5.

How many generalised Hamming numbers of type 100 are there which don't
exceed 10^(9)?
"""
from math import log
from sets import Set

def hamming_type(n=100,nmax=10**9):
    from Utils import primes
    ps = primes(n)
    hs = Set([1] + ps )
    npass = 50
    nham = 0
    print "After %d passes, there are %d hamming numbers of type %d less than %d" % (-1,len(hs),n,nmax+1)
    for i in range(npass):
        toadd = []
        for a in hs:
            for b in ps:
                if a*b < nmax:
                    toadd.append(a*b)
        for ab in toadd:
            hs.add(ab)
        print "After %d passes, there are %d hamming numbers of type %d less than %d" % (i,len(hs),n,nmax+1)
        if nham == len(hs):
            break
        nham = len(hs)

    if len(hs) < 40: 
        print list(hs)
    return

if __name__ == '__main__':
    hamming_type()
