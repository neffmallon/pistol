"""\
A positive integer n is called squarefree, if no square of a prime
divides n, thus 1, 2, 3, 5, 6, 7, 10, 11 are squarefree, but not 4, 8,
9, 12.

How many squarefree numbers are there below 2**50?
"""
from doctest import testmod
from math import sqrt
from sets import Set
from Utils import primes

# Some ideas of scale:
#print len(primes(2**25)) #  There are 2,063,689 below 2**25
#print 2**50              #  = 1,125,899,906,842,624

def factors(n):
    """
    Return the factors of n
    >>> factors(2)
    [1, 2]
    >>> factors(4)
    [1, 2, 4]
    """
    fs = []
    for i in range(1,n+1):
        if n%i == 0:
            fs.append(i)
    return fs

def is_sqfree(n):
    fs = Set(factors(n))
    for p in primes(n):
        if p*p in fs: return False
    return True

def sqfree_slow(n):
    return [i for i in range(1,n) if is_sqfree(i)]

def sieve_sqfree(n):
    """
    Return a list of squarefree numbers below n.
    Squarefree numbers are defined as those without square prime factors.
    >>> sieve_sqfree(12)
    [1, 2, 3, 5, 6, 7, 10, 11]

    Checked against sqfree_slow(n) up to n=8192
    """
    candidates = range(n)
    sqprimes = [i*i for i in primes(int(sqrt(n)))]
    for p2 in sqprimes:
        fmax = n/p2 + 1
        for f in range(1,fmax):
            if f*p2 < n:
                candidates[f*p2] = 0
    return [c for c in candidates if c]

if __name__ == '__main__':
    testmod()
    #for i in range(1,13):
    #    print "%3d %8d %8d %8d" % (i,2**i,len(sieve_sqfree(2**i)),
    #                               len(sqfree_slow(2**i)))
    def psf(n):
        ssf = sieve_sqfree(2**n)
        print len(ssf),ssf
    psf(3)
    psf(4)

# Number of squarefree numbers below 2**n
#        n     2**n   Nsqf(n)
#        1        2        1
#        2        4        3
#        3        8        6
#        4       16       11
#        5       32       20
#        6       64       39
#        7      128       78
#        8      256      157
#        9      512      314
#       10     1024      624
#       11     2048     1245
#       12     4096     2491
#       13     8192     4982
#       14    16384     9962
#       15    32768    19920
#       16    65536    39844
#       17   131072    79688
#       18   262144   159360
#       19   524288   318725
#       20  1048576   637461
#       21  2097152  1274918
#       22  4194304  2549834
# It seems that every time you go up a power of 2, you double the number
# of squarefree numbers, less the new number that you introduce. However,
# between 2**7 and 2**8, Nsqf(2**8) = 2*Nsqf(2**7)+1. I have now idea
# how this is possible.
