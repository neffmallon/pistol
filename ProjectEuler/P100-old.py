#!/usr/bin/env python
from math import sqrt

def disc(n): return 2*n*(n-1)+1
def isint(n): return int(n) == n
def issqint(n): return isint(sqrt(n))

iroots = [1,4,21,120,697,4060,23661,137904,803761,4684660,27304197,
          159140520, 927538921,5406093004,31509019101,
          183648021600,1070379110485]

# 159,140,520,   927,538,921,  5,406,093,004,   31,509,019,101
# 183,648,021,600, 1,070,379,110,494

# I think that 756,872,327,473 and 1,070,379,110,494 should be suitable
# pairs

def next_start(): return iroots[-1]*iroots[-1]/iroots[-2]

def next_root(istart):
    for i in range(-100,1000000):
        ii = istart + i
        print i
        if issqint(disc(ii)):
            print ii
            print sqrt(disc(ii))
            print istart,i
            break
    return

def main():
    #for i in range(1,len(iroots)):
    #    ratio = iroots[i]/float(iroots[i-1])
    #    print ratio
    ratio = 5.82842712467
    istart = int(ratio*iroots[-1])
    print "Starting from...",istart
    next_root(istart)

if __name__ == '__main__': main()
