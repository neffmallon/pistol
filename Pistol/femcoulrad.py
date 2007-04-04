#!/usr/bin/env python

from numpy import array,diag,sqrt,zeros,log,exp
from numpy.linalg import eigh
from Pistol.DVRSinc import RadialKinetic
from Pistol.fempbox import Tfem,Sfem,geigh
from pylab import plot,show

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

def CoulombFactory(Z=1.0,L=0.0):
    def V(r):
        return -Z/r + 0.5*L*(L+1.0)/(r*r)
    return V

def ExactH(n,L,Z=1.0):
    """\
    Exact Hydrogen-like radial wave functions
    """
    n = int(n)
    L = int(L)
    Z = float(Z)
    assert n>L
    assert n>0
    assert L >= 0
    alpha = 2*Z/float(n)
    prefac = sqrt(pow(alpha,3)*fact(n-L-1)/(2*n*fact(n+L)))
    Lnl = Laguerre(n-L-1,2*L+1)
    def F(r):
        ar = alpha*r
        return prefac*exp(-0.5*ar)*pow(ar,L)*Lnl(ar)
    return -0.5*Z/pow(n,2),F

def DVR(R,n,L,Z=1.0):
    n = int(n)
    L = int(L)
    Z = float(Z)
    assert n>L
    assert n>0
    assert L >= 0
    R = array(R)
    dr = R[0]
    npts = len(R)
    V = CoulombFactory(Z,L)
    H = RadialKinetic(npts,dr)  + diag([V(r) for r in R])
    E,U = eigh(H)
    return E[n-1],U[:,n-1]/sqrt(R**2*dr)

def main(n=30,**kwargs):
    L = kwargs.get('L',5.0)
    Z = kwargs.get('Z',1.0)
    tol = kwargs.get('tol',1e-5)
    dx = L/float(n)
    X = [i*dx for i in range(1,n)]
    T = Tfem(n,L)
    S = Sfem(n,L)
    V = zeros((n-1,n-1),'d')
    for i in range(n-1):
        xi = X[i]
        V[i,i] = Z + Z*pow((xi+dx)/dx,2)*log(xi+dx)
        if abs(xi) > tol:
            V[i,i] += 4*Z*xi*log(xi)/dx
        if abs(xi-dx) > tol:
            V[i,i] += Z*pow((xi-dx)/dx,2)*log(xi-dx)
    E,U = geigh(T+V,S)
    plot(X,U[:,0])
    # Exact solutions, for comparison
    E10,Psi10 = ExactH(1,0)
    plot(X,[Psi10(x) for x in X],'b-')
    print E[0],E10

    # DVR solutions, for comparison
    #E10dvr,Psi10dvr = DVR(X,1,0)
    #plot(X,Psi10dvr,'bo')
    show()
    

if __name__ == '__main__': main()

