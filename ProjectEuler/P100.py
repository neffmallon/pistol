
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
def disc(n): return 2*n*(n-1)+1

# These are the values of disc() that are sq ints 
# Python starts failing for larger values than this.
iroots = [1,4,21,120,697,4060,23661,137904,803761,4684660,27304197,
          # 159,140,520,  927,538,921, (5,406,092,854)
          159140520, 927538921]

# Possible solution:
# 655869060 (i=927,538,921 -> sqrt(disc) = 1,311,738,121 -> b = (sqrt(disc)-1)/2
# 2b*(b-1) = t*(t-1)
# 2b^2 - 2b -t*(t-1) = 0
# b = (disc-1)/2
def fit():
    from numpy import array,exp
    from scipy.optimize import leastsq
    yvals = array(iroots)
    xvals = array(range(1,len(iroots)+1))
    def feval(x,p): return p[0]*exp(x)+p[1]
    def residuals(p,y,x): return y-feval(x,p)
    p0 = array((1.,1.))
    print residuals(p0,yvals,xvals)
    plsq = leastsq(residuals,p0,args=(iroots,xvals))
    a,b = plsq[0]
    print plsq[0]
    print [a*exp(x)+b for x in xvals]
    return

def disc_roots():
    for i in xrange(10**8,10**9):
        if issqint(disc(i)):
            print i
def main():
    #disc_roots()
    for i in range(1,len(iroots)): print i,iroots[i]/float(iroots[i-1])    

if __name__ == '__main__': main()

        
