from math import sqrt
from itertools import count

def quadratic(a,b,c):
    n1 = -b
    disc = b*b-4*a*c
    if disc < 0: return None,None
    n2 = sqrt(disc)
    return (n1+n2)/(2*a),(n1-n2)/(2*a)

def isint(n): return int(n) == n
def issqint(n): return isint(sqrt(n))

def main():
    #def disc(n): return 2*n*(n-1)+1
    rt2 = sqrt(2)
    trillion = 10**12
    for i in count():
        nt = i+trillion
        nb = int(round(nt/rt2))
        if 2*nb*(nb-1) == nt*(nt-1):
            print nt,nb
    return

if __name__ == '__main__': main()

        
