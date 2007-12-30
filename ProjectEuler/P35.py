"""
The number, 197, is called a circular prime because all rotations of
the digits: 197, 971, and 719, are themselves prime.

There are thirteen such primes below 100: 2, 3, 5, 7, 11, 13, 17, 31,
37, 71, 73, 79, and 97.

How many circular primes are there below one million?
"""

import psyco; psyco.full()

from sets import Set

def gen_primes(n):
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

def num_to_digits(n): return map(int,str(n))

def circ_perms(n):
    perms = [n]
    digs = num_to_digits(n)
    ndigs = len(digs)
    for i in range(ndigs-1):
        fd = digs.pop(0)
        digs.append(fd)
        perms.append(int("".join(map(str,digs))))
    return perms

primes = gen_primes(1000000)
primeset = Set(primes)

cplist = []
for p in primes:
    perms = circ_perms(p)
    logs = [pi in primeset for pi in perms]
    is_circ_prime = False not in logs
    if is_circ_prime:
        cplist.append(p)
print len(cplist),cplist

