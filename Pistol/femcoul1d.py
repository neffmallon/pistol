#!/usr/bin/env python

from numpy import array,diag,sqrt,zeros,log
from numpy.linalg import eigh
from Pistol.DVRSinc import LinearKinetic
from Pistol.fempbox import Tfem,Sfem,geigh
from pylab import plot,show

def loga(x,small=1e-40):
    "This is a safe log(abs(x)), so that when x is small, it's still okay"
    ax = abs(x)
    if ax<small: ax = small
    return log(ax)

def dvr(n=1000,**kwargs):
    xmax = kwargs.get('xmax',5.0)
    xmin = kwargs.get('xmin',-xmax)
    dx = (xmax-xmin)/float(n-1)
    X = array([xmin + i*dx for i in range(n)])
    T = LinearKinetic(n,dx)
    def Coul(x): return -1/abs(x)
    V = diag([Coul(x) for x in X])
    H = T+V
    E,U = eigh(H)
    normfact = 1/sqrt(dx)
    U = U*normfact
    return X,E,U

#def sign(x): return int(x/abs(x))
def sign(x):
    if x >= 0: return 1
    return -1

def main(n=10,**kwargs):
    xmax = kwargs.get('xmax',2.0)
    xmin = kwargs.get('xmin',-xmax)
    small = kwargs.get('small',1e-10)
    L = xmax-xmin
    dx = L/float(n)
    Xdvr,Edvr,Udvr = dvr(xmax=xmax,xmin=xmin)
    X = [xmin+i*dx for i in range(1,n)]
    T = Tfem(n,L)
    S = Sfem(n,L)
    V = zeros((n-1,n-1),'d')
    for i in range(n-1):
        xi = X[i]
        ax = abs(xi)
        V[i,i] = 1
        if xi > dx:
            V[i,i] = 
        if abs(xi) > tol:
            V[i,i] += 4*
        V[i,i] = -2*ax/dx \
                 + pow((dx-ax)/dx,2)*(loga(xi)-loga(xi-dx)) \
                 + pow((dx+ax)/dx,2)*(loga(xi+dx)-loga(xi))
        #if i < n-2:
        #    V[i,i+1] = V[i+1,i] = (2*ax+dx)/(2*dx) + ax*(dx+ax)/(dx*dx) *\
        #               (loga(xi+dx)-loga(xi))
    E,U = geigh(T+V,S)
    print E[:4]
    print Edvr[:4]
    print X
    plot(Xdvr,abs(Udvr[:,0]),'b-')
    plot(X,abs(U[:,0]),'bo')
    show()
    

if __name__ == '__main__': main()

