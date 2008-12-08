"""
Utility functions that have been useful in Project Euler
"""

from math import sqrt
from sets import Set
from MillerRabin import isprime
from operator import mul

def timeit(command,*args,**kwargs):
    from time import time
    ntimes = kwargs.get('ntimes',20)
    start = time()
    for i in range(ntimes): retval = command(*args)
    end = time()
    print "timeit(%s): %f seconds" % (command.__name__,(end-start)/ntimes)
    return retval

def get_wordgen(fname="/usr/share/dict/words"):
    return (line.strip() for line in open(fname))

def get_wordlist(fname): return list(get_wordgen(fname))
def get_wordset(fname): return Set(get_wordgen(fname))

def prod(l): return reduce(mul,l)

def gcd(a,b):
    while b:
        a, b = b, a%b
    return a

def gcd3(a,b,c): return gcd(gcd(a,b),c)

def prime_factors(n,ps):
    factors = []
    for p in ps:
        if p > n: break
        if n % p == 0:
            factors.append(p)
    return factors

def proper_divisors(n):
    d = [1]
    limit = int(sqrt(n))
    for i in xrange(2,limit+1):
        if n%i == 0: 
            d.append(i)
            if n/i != i: d.append(n/i)
    d.sort()
    return d

def ndivisors(n,VERBOSE=False):
    "just count the divisors of n"
    s = 0
    lim = int(sqrt(n)+1)
    for i in xrange(1,lim):
        if n%i == 0:
            if i == n/i:
                s += 1
            else:
                s+=2
    return s

def divisors(n):
    "Also include n"
    return proper_divisors(n) + [n]

def lcm(a,b):
    return a*b/gcd(a,b)

def fibonacci():
    yield 0
    yield 1
    n1,n2 = 0,1
    while 1:
        n1,n2 = n2,n1+n2
        yield n2
    return

def factorial(n):
    if n == 0:
        return 1
    return n*factorial(n-1)

def ndigits(n): return len(num_to_digits(n))
def num_to_digits(n): return map(int,str(n))
def digits_to_num(d): return int("".join(map(str,d)))

def unique(l,sort=False):
    vals = {}
    for li in l:
        vals[li] = 1
    results = vals.keys()
    if sort:
        results.sort()
    return results

def isprime_sieve_factory(nmax=1000000):
    pset = Set(primes(nmax))
    def isprime(n):
        assert n<nmax, "%d too large for prime test" % n
        return n in pset
    return isprime

def primes(n):
    """\
    From python cookbook
    returns a list of prime numbers from 2 to < n

    >>> primes(2)
    [2]
    >>> primes(10)
    [2, 3, 5, 7]
    """
    if n==2: return [2]
    elif n<2: return []
    s=range(3,n+1,2)
    mroot = n ** 0.5
    half=(n+1)/2-1
    i=0
    m=3
    while m <= mroot:
        if s[i]:
            j=(m*m-3)/2
            s[j]=0
            while j<half:
                s[j]=0
                j+=m
        i=i+1
        m=2*i+3
    return [2]+[x for x in s if x]

def sortcopy(l):
    from copy import copy
    l2 = copy(l)
    l2.sort()
    return l2

def isperm(a,b):
    as = str(a)
    bs = str(b)
    return len(as) == len(bs) and Set(as) == Set(bs)

def permute(iterable) :
     if len(iterable) == 1 : yield iterable
     else :
         next = permute(iterable[1:])
         for i in next :
             if isinstance(iterable[0], basestring) :
                 elt = iterable.__class__(iterable[0])
             else : elt = iterable.__class__((iterable[0],))
             for j, k in enumerate(i) : yield i[0:j] + elt + i[j:]
             yield i + elt

def farey(v, lim):
    """
    Named after James Farey, an English surveyor.
    No error checking on args -- lim = max denominator,
    results are (numerator, denominator), (1,0) is infinity
    """
    if v < 0:
        n,d = farey(-v, lim)
        return -n,d
    z = lim-lim	# get 0 of right type for denominator
    lower, upper = (z,z+1), (z+1,z)
    while 1:
        mediant = (lower[0] + upper[0]), (lower[1]+upper[1])
        if v * mediant[1] > mediant[0]:
            if lim < mediant[1]: return upper
            lower = mediant
        elif v * mediant[1] == mediant[0]:
            if lim >= mediant[1]: return mediant
            if lower[1] < upper[1]: return lower
            return upper
        else:
            if lim < mediant[1]: return lower
            upper = mediant


def xcombos(items,n,unique=True):
    if n == 0: yield []
    else:
        for i in xrange(len(items)):
            if unique:
                for cc in xcombos(items[i+1:],n-1,unique):
                    yield [items[i]]+cc
            else:
                for cc in xcombos(items[:i]+items[i+1:],n-1,unique):
                    yield [items[i]]+cc
    return

def contfrac(f,nterms=10):
    f,rem = divmod(f,1)
    frac = [int(f)]
    for i in xrange(nterms-1):
        if rem == 0: break
        f,rem = divmod(1/rem,1)
        frac.append(int(f))
    return frac

def cf_to_frac(l):
    # would be nice to have a rational version of this
    n = len(l)
    f = l[n-1]
    for i in xrange(n-2,-1,-1):
        f = l[i] + 1/float(f)
    return f

def sqrtcf(n):
    orig = n
    denom = 1
    addterm = 0
    cflist = []
    while True:
        m = int(pow(n,0.5)) # <-- replace with function call
        cflist.append(m)
        if len(cflist)>1 and denom == 1:
            break                   
        addterm = -(addterm - m*denom)
        denom = (orig - addterm**2)/denom
        n = ((pow(orig,0.5) + addterm)/denom)**2
    return cflist

class Rational:
    def __init__(self,N,D=1):
        self.N = N
        self.D = D
        self.reduce()
        return

    def reduce(self):
        f = gcd(self.N,self.D) 
        if f != 1:
            self.N /= f
            self.D /= f
        return

    def float(self): return self.N/float(self.D)
    def int(self): return int(self.float())

    def mult(self,other):
        return Rational(self.N*other.N,self.D*other.D)

    def add(self,other):
        return Rational(self.N*other.D + self.D*other.N,self.D*other.D)

    def inverse(self):
        return Rational(self.D,self.N)

    def __repr__(self):
        return "%d/%d" % (self.N,self.D)

    def isint(self): return self.D == 1

def cf_to_rf(l):
    n = len(l)
    r = Rational(l[n-1])
    for i in xrange(n-2,-1,-1):
        r = Rational(l[i]).add(r.inverse())
    return r


def isqrt(n):
    xn = 1
    xn1 = (xn + n/xn)/2
    while abs(xn1 - xn) > 1:
        xn = xn1
        xn1 = (xn + n/xn)/2
    while xn1*xn1 > n:
        xn1 -= 1
    return xn1

def issquare(n): return isqrt(n)**2 == n

def isint(f): return f == int(f)
def is_int_frac(a,b): return (a%b==0)

def next_partition(p):
    "Taken from the perl monks recipe 621859, which I don't understand"
    from copy import copy
    p2 = copy(p)

    # Collect all the trailing 1s
    x = 0
    while p2 and p2[-1] == 1:
        x += p2.pop()
    if not p2: return []

    # Collect 1 from the rightmost remaining element
    p2[-1] -= 1
    x += 1

    while x > p2[-1]:
        p2.append(p2[-1])
        x -= p2[-1]
    p2.append(x)
    return p2

def partition_upper_bound(k):
    """Ramanujan's upper bound for number of partitions of k"""
    from math import sqrt,exp,pi
    return int(exp(pi*sqrt(2.0*k/3.0))/(4.0*k*sqrt(3.0)))

def count_partitions(i):
    p = [i]
    n = 1
    while 1:
        p = next_partition(p)
        if not p: break
        n += 1
    return n

def incr_partitions(p1s):
    """Given the partitions of p(n-1), generate the partitions of p(n).
    This generates the partitions in the reverse of the order I like,
    but it isn't that big of a deal.
    """
    ps = []
    for p in p1s:
        ps.append([1]+p)
        if p and (len(p) == 1 or p[1] > p[0]):
            ps.append([p[0]+1]+p[1:])
    return ps

def spiral():
    """\
    >>> list(islice(spiral(),1))
    [(0, 0)]
    >>> list(islice(spiral(),2))
    [(0, 0), (1, 0)]
    >>> list(islice(spiral(),4))
    [(0, 0), (1, 0), (1, -1), (0, -1)]
    >>> list(islice(spiral(),9))
    [(0, 0), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1)]
    """
    #RIGHT, UP, LEFT, DOWN = range(4)
    UP, RIGHT, DOWN, LEFT = range(4)
    
    dx = dy = 0
    count = 1
    remain = 2
    distance = 1
    direction = RIGHT

    icount = 0
    while 1:
        yield dx,dy
        remain -= 1
        if remain == 0:  # Need to change direction
            if direction == UP:
                distance += 1
                direction = LEFT
            elif direction == DOWN:
                distance += 1
                direction -= 1
            else:
                direction -= 1
            remain = distance
        if direction == LEFT:
            dx -= 1
        elif direction == RIGHT:
            dx += 1
        elif direction == UP:
            dy -= 1
        elif direction == DOWN:
            dy += 1
    # end

def spiral_matrix(n):
    "Make a numpy integer matrix from the pts array"
    from itertools import islice
    from numpy import zeros
    p = zeros((n,n),'i')
    sp = list(islice(spiral(),n*n))
    hn,rem = divmod(n,2)
    ipt = 0
    for y,x in sp:
        x = -x
        ipt += 1
        p[x+hn,y+hn] = ipt
    return p

