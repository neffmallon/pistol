"""
Considering 4-digit primes containing repeated digits it is clear that
they cannot all be the same: 1111 is divisible by 11, 2222 is
divisible by 22, and so on. But there are nine 4-digit primes
containing three ones:

1117, 1151, 1171, 1181, 1511, 1811, 2111, 4111, 8111

We shall say that M(n, d) represents the maximum number of repeated
digits for an n-digit prime where d is the repeated digit, N(n, d)
represents the number of such primes, and S(n, d) represents the sum
of these primes.

So M(4, 1) = 3 is the maximum number of repeated digits for a 4-digit
prime where one is the repeated digit, there are N(4, 1) = 9 such
primes, and the sum of these primes is S(4, 1) = 22275. It turns out
that for d = 0, it is only possible to have M(4, 0) = 2 repeated
digits, but there are N(4, 0) = 13 such cases.

In the same way we obtain the following results for 4-digit primes.
Digit, d 	M(4, d) 	N(4, d) 	S(4, d)
0 	2 	13 	67061
1 	3 	9 	22275
2 	3 	1 	2221
3 	3 	12 	46214
4 	3 	2 	8888
5 	3 	1 	5557
6 	3 	1 	6661
7 	3 	9 	57863
8 	3 	1 	8887
9 	3 	7 	48073

For d = 0 to 9, the sum of all S(4, d) is 273700.

Find the sum of all S(10, d).
"""

from doctest import testmod
from math import sqrt
from Utils import primes,isprime,timeit
from re import findall

def nprimes(n):
    "Primes with n-digits"
    return [p for p in primes(10**n) if p > 10**(n-1)]

def nprimes2(n):
    # Much slower than nprimes()
    return [i for i in xrange(10**(n-1)+1,10**n,2) if isprime(i)]

def nprimes3(n):
    # Slower than nprimes()
    limit = int(sqrt(10**n))
    psmall = primes(limit)
    ps = []
    for i in xrange(10**(n-1)+1,10**n,2):
        for p in psmall:
            if i % p == 0: break
        else:
            ps.append(i)
    return ps

def gmpy_primes(start,end):
    import gmpy
    i = start
    while True:
        #i = int(gmpy.next_prime(i))
        i = gmpy.next_prime(i)
        if i > end: break
        yield i
    return

def nprimes4(n):
    # Slightly slower than nprimes()
    return list(gmpy_primes(10**(n-1),10**n))

def noccur(word,c):
    """
    Return the number of times the character c occurs in word
    >>> noccur('abc','a')
    1
    >>> noccur('aab','a')
    2
    """
    return word.count(c)
    #return sum(1 for w in word if w==c)
    #return len(findall(c,word)) # Argh! slower !?

def maxoccur(l,d):
    """\
    For words in l, return the maximum number of times the digit
    d occurs in any one word.
    >>> maxoccur(['abc','aab'],'a')
    2
    """
    return max(noccur(word,d) for word in l)

def occurlist(l,d,n):
    return [w for w in l if noccur(w,d) == n]

def sum111(xdigit):
    psx = nprimes(xdigit)
    spsx = map(str,psx)
    vs = []
    for d in '0123456789':
        mxd = maxoccur(spsx,d)
        ol = occurlist(spsx,d,mxd)
        sxd = sum(map(int,ol))
        #print d,mxd,len(ol),sxd
        vs.append(sxd)
    #print "Final sum for %d digits = %d" % (xdigit,sum(vs))
    return sum(vs)

def search111(xdigit):
    mxd = [0]*10
    digits = range(10)
    dlist = [[] for i in digits]
    for p in gmpy_primes(10**(xdigit-1),10**xdigit):
    #for p in nprimes(xdigit):
        for d in digits:
            nd = noccur(str(p),str(d))
            if nd > mxd[d]:
                mxd[d] = nd
                dlist[d] = [p]
            elif nd == mxd[d]:
                dlist[d].append(p)
    for i in range(10):
        print i,mxd[i],len(dlist[i]),sum(dlist[i])
    print sum(sum(dlist[i]) for i in range(10))
    return sum(sum(dlist[i]) for i in xrange(10))

def timeprimes(nmax):
    from time import time
    t0 = time()
    l1 = nprimes(nmax)
    t1 = time()
    print t1-t0
    #l2 = nprimes2(nmax)
    t2 = time()
    #print t2-t1
    l3 = nprimes3(nmax)
    t3 = time()
    print t3-t2
    l4 = nprimes4(nmax)
    t4 = time()
    print t4-t3
    print l1 == l3 == l4
    return

def timesol(nmax):
    from time import time
    t0 = time()
    l1 = sum111(nmax)
    t1 = time()
    print t1-t0
    l2 = search111(nmax)
    t2 = time()
    print t2-t1
    print l1 == l2
    return

def profmain():
    import cProfile,pstats
    cProfile.run('search111(8)','prof')
    prof = pstats.Stats('prof')
    prof.strip_dirs().sort_stats('time').print_stats(15)
    return

def gen_n_nm1(n,k,forceprimes=False):
    """\
    Generate all of the n-digit numbers, with n-1 k's.
    If forceprimes is True, only generate primes
    """
    from gmpy import is_prime
    for p in range(n):
        for d in '0123456789':
            if int(d) == k: continue
            num = [str(k)]*n
            num[p] = d
            if num[0] == '0': continue
            num = int("".join(num))
            if forceprimes and not is_prime(num): continue            
            yield num
    return

def gen_n_nm2(n,k,forceprimes=False):
    """\
    Generate all of the n-digit numbers, with n-2 k's.
    If forceprimes is True, only generate primes.
    """
    from gmpy import is_prime
    for p1 in range(n):
        for p2 in range(p1):
            if p1 == p2: continue
            for d1 in '0123456789':
                if int(d1) == k: continue
                for d2 in '0123456789':
                    if int(d2) == k: continue
                    num = [str(k)]*n
                    num[p1] = d1
                    num[p2] = d2
                    if num[0] == '0': continue
                    num = int("".join(num))
                    if forceprimes and not is_prime(num): continue            
                    yield num
    return

def direct111(n):
    #l0 = gen_n_nm2(10,0,True)
    #l1 = gen_n_nm1(10,1,True)
    #l2 = gen_n_nm2(10,2,True)
    #l3 = gen_n_nm1(10,3,True)
    #l4 = gen_n_nm1(10,4,True)
    #l5 = gen_n_nm1(10,5,True)
    #l6 = gen_n_nm1(10,6,True)
    #l7 = gen_n_nm1(10,7,True)
    #l8 = gen_n_nm2(10,8,True)
    #l9 = gen_n_nm1(10,9,True)
    #lall = l0,l1,l2,l3,l4,l5,l6,l7,l8,l9
    l = []
    allsum = 0
    for i in range(10):
        li = list(gen_n_nm1(n,i,True))
        if len(li) == 0:
            li = list(gen_n_nm2(n,i,True))
        assert len(li) > 0
        l.append(li)
        print li,len(li),sum(li)
        allsum += sum(li)
    print allsum

def main():
    testmod()
    #profmain()
    #timeprimes(7)
    direct111(10)

if __name__ == '__main__': main()
