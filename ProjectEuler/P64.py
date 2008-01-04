from math import sqrt
from decimal import Decimal,getcontext

def isint(f): return f==int(f)

def contfrac(f,nterms=10):
    "slightly diff version, that computes period"
    f,rem = divmod(f,1)
    frac = [int(f)]
    period = None
    seen = []
    for i in range(nterms-1):
        if rem == 0:
            period = 0
            break
        f,rem = divmod(1/rem,1)
        key = int(10000*rem)
        if key in seen:
            period = i-seen.index(key)
            break
        frac.append(int(f))
        seen.append(key)
    return frac,period

prec = 10
getcontext().prec=prec
nmax = 1000
nodd = 0
unfound = []
for i in range(1,nmax+1):
    di = Decimal(i)
    sqrti = sqrt(i)
    if isint(sqrt(i)): continue
    cf,period = contfrac(sqrt(i),prec)
    if not period:
        unfound.append(i)
    elif period %2 == 1:
        nodd += 1
print nodd
print len(unfound),unfound
unfound2 = []
getcontext().prec=100
for i in unfound:
    di = Decimal(i)
    sqrti = sqrt(i)
    if isint(sqrt(i)): continue
    cf,period = contfrac(sqrt(i),prec)
    if not period:
        unfound.append(i)
    elif period %2 == 1:
        nodd += 1
print nodd
print len(unfound2),unfound2

    

