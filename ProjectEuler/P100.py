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
    def disc(n): return 2*n*(n-1)+1
    t = 10**12
    for i in count():
        nt = t+i
        if issqint(disc(nt)):
            d = int(sqrt(disc(nt)))
            nb = (d+1)/2
            print nt,disc(nt),nb,2*nb*(nb-1)==nt*(nt-1)
    return

if __name__ == '__main__': main()

        
