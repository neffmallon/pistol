"""
The number 3797 has an interesting property. Being prime itself, it is
possible to continuously remove digits from left to right, and remain
prime at each stage: 3797, 797, 97, and 7. Similarly we can work from
right to left: 3797, 379, 37, and 3.

Find the sum of the only eleven primes that are both truncatable from
left to right and right to left.
"""
from copy import copy

def num_to_digits(n): return map(int,str(n))
def digits_to_num(d): return int("".join(map(str,d)))

def truncate_series(n):
    digits = num_to_digits(n)
    series = []
    forward = copy(digits)
    reverse = copy(digits)
    for i in range(len(digits)-1):
        forward.pop()
        reverse.pop(0)
        series.append(digits_to_num(forward))
        series.append(digits_to_num(reverse))
        #series.append(copy(forward))
        #series.append(copy(reverse))
    return series

def primes(n):
    # From python cookbook
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

#print digits_to_num(num_to_digits(3797))
#print truncate_series(3797)
nmax = 900000
ps = primes(nmax)
from sets import Set
pset = Set(ps)

tprimes = []
for p in ps[4:]:
    candidates = truncate_series(p)
    result = True
    for c in candidates:
        if c not in pset:
            result = False
            break
    if result:
        tprimes.append(p)
print len(tprimes),sum(tprimes),tprimes



    
