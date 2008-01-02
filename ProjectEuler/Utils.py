#def gcd(a,b):
#    if b==0: return a
#    return gcd(b, a%b)

# This is faster:
def gcd(a,b):
    while b:
        a, b = b, a%b
    return a

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
