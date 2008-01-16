from math import sqrt
from Utils import sqrtcf

def issquare(n): return isint(sqrt(n))
def isint(f): return f==int(f)

nmax = 10000
nodd = 0
for N in range(2,nmax+1):
    if issquare(N): continue
    cf = sqrtcf(N)
    period = len(cf)-1
    if period%2 == 1: nodd += 1
print "%d fractions <= %d have an odd period" % (nodd,nmax)
