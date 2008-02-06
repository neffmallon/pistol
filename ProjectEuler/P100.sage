#!/usr/bin/env sage

def disc(n): return 2*n*(n-1)+1
def isint(n): return int(n) == n
def issqint(n): return isint(sqrt(n))

iroots = [1,4,21,120,697,4060,23661,137904,803761,4684660,27304197,
          159140520, 927538921,5406093004,31509019101]

def next_start(): return int(n(iroots[-1]*iroots[-1]/iroots[-2]))

def next_root(istart):
    for i in range(1000000):
        print i
        ii = istart + i
        if issqint(disc(ii)):
            print ii
            break
    return

