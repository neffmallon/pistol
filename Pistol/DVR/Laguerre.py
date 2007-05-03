#!/usr/bin/env python
"""
DVR/Laguerre.py - DVR based on Laguerre polynomials.
"""

from numpy import zeros,sqrt,array,diag
from numpy.linalg import eigh
from scipy.special.orthogonal import la_roots

def Laguerre_S(i,j,x):
    Sij = 0
    N = len(x)
    xi = x[i]
    xj = x[j]
    for k in range(N):
        if k == i or k == j: continue
        xk = x[k]
        Sij += sqrt(xi*xj)/(xk*(xk-xi)*(xk-xj))
    return Sij

def RadialKinetic0(N,L):
    # Baye + Heenen eq 3.17
    a = 2*L+2
    x,w = la_roots(N,a)
    x = x.real
    T = zeros((N,N),'d')
    for i in range(N):
        xi = x[i]
        Sii = Laguerre_S(i,i,x)
        T[i,i] = 0.25*pow((a+1.)/xi,2)+Sii
        for j in range(i):
            xj = x[j]
            Sij = Laguerre_S(i,j,x)
            T[i,j] = T[j,i] = pow(-1,i-j)*(0.5*(a+1.)*(xi+xj)/pow(xi*xj,1.5)+Sij)
    return x,0.5*T

def RadialKinetic1(N,L):
    # Baye + Heenen eq 3.27
    a = L+0.5
    x,w = la_roots(N,a)
    x = sqrt(x.real)
    T = zeros((N,N),'d')
    for i in range(N):
        xi = x[i]
        xi2 = xi*xi
        T[i,i] = (2./3.)*(a+2.0*N+1.0+(a*a-1)/xi2 - 0.5*xi2)
        for j in range(i):
            xj = x[j]
            xj2 = xj*xj
            T[i,j] = T[j,i] = pow(-1,i-j)*8*xi*xj/(xi2-xj2)
    return x,0.5*T

def RadialKinetic(N,L):
    # Szalay Table III: Does not contain the AM term
    a = 2L+2 # ? L+1,2L+1???
    x,w = la_roots(N,a)
    x = x.real
    T = zeros((N,N),'d')
    for i in range(N):
        xi = x[i]
        T[i,i] = 1./12. - (2.0*N+1.0)/(6.0*xi) + 2.0/(3.0*xi*xi)
        for j in range(i):
            xj = x[j]
            T[i,j] = T[j,i] = sqrt(xj/xi)*(-3.0*xi+xj)/(xi*pow(xi-xj,2))
    return x,0.5*T

def Sincresults(n,V):
    from Sinc import RadialKinetic
    Rmax = 20.0
    dr = Rmax/float(n)
    R = [float(i+1)*dr for i in range(n)]
    H = RadialKinetic(n,dr) + diag([V(r) for r in R]) 
    E,U = eigh(H)
    return R,E,U

def Htest(N=50):
    x,T = RadialKinetic1(N,0)
    def V(x,Z=1.0): return -Z/x # Coulomb
    #def V(x): return x
    Vx = array([V(xi) for xi in x])
    E,U = eigh(T+diag(Vx))
    xdvr,Edvr,Udvr = Sincresults(N,V)
    print E[:4]
    print Edvr[:4]
    return


        
if __name__ == '__main__': Htest()
