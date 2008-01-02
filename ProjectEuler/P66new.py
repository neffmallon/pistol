
import psyco; psyco.full()
from pprint import pprint
from math import sqrt
from sets import Set

def isint(n): return int(n) == n

N = 50000
results = {}
for i in xrange(1,N):
    x2 = i*i
    for j in xrange(1,i):
        y2 = j*j
        D = (x2-1)/float(y2)
        if isint(D):
            results[int(D)] = (i,j)

nonsquares = [i for i in xrange(1,1001) if not isint(sqrt(i))]
missing = [i for i in nonsquares if i not in results]
pprint(missing)




