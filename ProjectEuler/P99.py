
from math import log

maxval = 0
imax = 0

for i,line in enumerate(open("base_exp.txt")):
    a,b = map(int,line.split(","))
    val = b*log(a)
    print a,b,val
    if val > maxval:
        maxval = val
        imax = i
print imax+1
