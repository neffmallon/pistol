"""
The primes 3, 7, 109, and 673, are quite remarkable. By taking any two
primes and concatenating them in any order the result will always be
prime. For example, taking 7 and 109, both 7109 and 1097 are prime.
The sum of these four primes, 792, represents the lowest sum for a set
of four primes with this property.

Find the lowest sum for a set of five primes for which any two primes
concatenate to produce another prime.
"""

from Utils import primes
from sets import Set

def concatints(a,b): return int(str(a)+str(b))

nmax = 10000
ps = primes(nmax)
nprimes = len(ps)
pset = Set(ps)
bpset = Set(primes(nmax*nmax))

primepairs = Set()
for i in xrange(nprimes):
    pi = ps[i]
    for j in range(i):
        pj = ps[j]
        if concatints(pi,pj) in bpset and\
           concatints(pj,pi) in bpset:
            if pi > pj:
                pi,pj = pj,pi
            primepairs.add((pi,pj))
print primepairs

primetrios = Set()
for pi,pj in primepairs:
    for k in xrange(nprimes):
        pk = ps[k]
        if pk == pi or pk == pj: continue
        if concatints(pi,pk) in bpset and\
           concatints(pk,pi) in bpset and\
           concatints(pj,pk) in bpset and\
           concatints(pk,pj) in bpset:
            l = [pi,pj,pk]
            l.sort()
            primetrios.add(tuple(l))
print primetrios

primequartets = Set()
for pi,pj,pk in primetrios:
    for l in xrange(nprimes):
        pl = ps[l]
        if pl == pi or pl == pj or pl == pk: continue
        if concatints(pi,pl) in bpset and\
           concatints(pl,pi) in bpset and\
           concatints(pj,pl) in bpset and\
           concatints(pl,pj) in bpset and\
           concatints(pk,pl) in bpset and\
           concatints(pl,pk) in bpset:
            l = [pi,pj,pk,pl]
            l.sort()
            primequartets.add(tuple(l))
print primequartets

primequintets = Set()
for pi,pj,pk,pl in primequartets:
    for m in xrange(nprimes):
        pm = ps[m]
        if pm == pi or pm == pj or pm == pk or pm == pl: continue
        if concatints(pi,pm) in bpset and\
           concatints(pm,pi) in bpset and\
           concatints(pj,pm) in bpset and\
           concatints(pm,pj) in bpset and\
           concatints(pk,pm) in bpset and\
           concatints(pm,pk) in bpset and\
           concatints(pl,pm) in bpset and\
           concatints(pm,pl) in bpset:
            l = [pi,pj,pk,pl,pm]
            l.sort()
            primequintets.add(tuple(l))
print primequintets
