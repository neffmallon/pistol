#!/usr/bin/env python
"""\
Exact.py Exact solutions for test case comparisons.

"""

from numpy import array,zeros,sin,sqrt,pi,exp
from pylab import plot,show

def ExactSquareWell(nstate,npoint,L):
    """\
    Return an n-point discretization of the first nstate solutions
    of the exact particle-in-a-box energies and wave function.
    """
    x = array([float(L*j)/float(npoint-1) for j in range(npoint)])
    E = zeros(nstate,'d')
    V = zeros((npoint,nstate),'d')
    norm = sqrt(2./float(L))
    for n in range(1,nstate+1):
        E[n-1] = 0.5*n**2*pi**2/L**2
        V[:,n-1] = norm*sin(n*pi*x/L)
    return x,E,V

def fact(n):
    cache = [1,1,2,6,24,120,720,5040,40320,362880]
    if n < len(cache): return cache[n]
    return n*fact(n-1)

def Laguerre(n,k):
    """\
    The Associated Laguerre Polynomials, from Arfken p 841
    """
    assert k >= 0
    def L(r):
        val = 0
        for m in range(n+1):
            val += pow(-1,m)*fact(n+k)*pow(r,m)/(fact(n-m)*fact(k+m)*fact(m))
        return val
    return L

def ExactH(n,L,Z=1.0):
    """\
    Exact Hydrogen-like radial wave functions
    """
    n = int(n)
    L = int(L)
    Z = float(Z)
    assert n>L
    alpha = 2*Z/float(n)
    prefac = sqrt(pow(alpha,3)*fact(n-L-1)/(2*n*fact(n+L)))
    Lnl = Laguerre(n-L-1,2*L+1)
    def F(r):
        ar = alpha*r
        return prefac*exp(-0.5*ar)*pow(ar,L)*Lnl(ar)
    return F

def LaguerreTest():
    n = 100
    Rmax = 10.0
    dr = Rmax/float(n)
    R = [float(i+1)*dr for i in range(n)]
    L01 = Laguerre(0,1)
    plot(R,[L01(r) for r in R])
    L11 = Laguerre(1,1)
    plot(R,[L11(r) for r in R])
    L21 = Laguerre(2,1)
    plot(R,[L21(r) for r in R])
    show()
    return

if __name__ == '__main__': LaguerreTest()
