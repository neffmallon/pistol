#!/usr/bin/env python
"""
Solve 1-D potentials via the method of Harris, Engerholm, and Gwinn.
See JCP 43, 1515 (1965).
"""

from math import sqrt,pi,exp

use_numpy = True
if use_numpy:
    from numpy import zeros,arange,matrixmultiply,transpose,diag,array2string
    from numpy.linalg import eigh
else:
    from Numeric import zeros,arange,matrixmultiply,transpose,array2string
    from LinearAlgebra import Heigenvectors as eigh


def diag(v):
    n = len(v)
    A = zeros((n,n),'d')
    for i in range(n): A[i,i] = v[i]
    return A

def HEG(n,V):
    X = zeros((n,n),'d')
    for i in range(n):
        if i:
            X[i,i-1] = X[i-1,i] = sqrt(i)/sqrt(2)
    # Eq 1 from HEG
    lam,T = eigh(X)

    Vx = [V(li) for li in lam]
    # Eq 2 from HEG
    #Vho = zeros((n,n),'d')
    #Vho = matrixmultiply(T,matrixmultiply(diag(Vx),transpose(T)))
    Vho = simxt(diag(Vx),T)
    Tho = zeros((n,n),'d')
    for i in range(n):
        Tho[i,i] = 0.25*(2*i+1)
        if i > 1:
            Tho[i,i-2] = Tho[i-2,i] = -0.25*sqrt(i-1)*sqrt(i)
    Hho = Tho+Vho
    matprint(Tho,label="T")
    matprint(Vho,label="V")
    matprint(Hho,label="H")
    
    E,U = eigh(Hho)
    # The eigenvectors are in terms of the HO eigenvectors, so
    # we have to multiply by X before returning
    return lam,E,matrixmultiply(T,U)

def simx(A,T): return matrixmultiply(transpose(T),matrixmultiply(A,T))
def simxt(A,T): return matrixmultiply(T,matrixmultiply(A,transpose(T)))

def Tfd(n,dx):
    "Form a finite-difference kinetic energy operator"
    a = 1./dx/dx
    H = zeros((n,n),'d')
    for i in range(n):
        H[i,i] = a
        if i > 0:
            H[i,i-1] = H[i-1,i] = -0.5*a
    return H

def Hfd(x,V):
    n = len(x)
    dx = x[1]-x[0]
    H = Tfd(n,dx)  # Form the KE operator

    # Add in the potential
    for i in range(n):
        H[i,i] += V(x[i])

    E,U = eigh(H)
    return E,U

# Factory functions to build different potentials:
def square_well_factory(**kwargs):
    V0 = kwargs.get('V0',1.)
    A = kwargs.get('A',1.)
    def V(x):
        if abs(x) < A: return 0
        return V0
    return V

def harmosc_factory(**kwargs):
    k = kwargs.get('k',1.)
    def V(x): return 0.5*k*x*x
    return V

def morse_factory(**kwargs):
    X0 = kwargs.get('X0',0)
    D = kwargs.get('D',1.)
    alpha = kwargs.get('alpha',1.)
    def V(x): return D*pow(1-exp(-alpha*(x-X0)),2)
    return V        

# General plotting function
def plot_results(x,V,U,**kwargs):
    from pylab import plot,clf,axis,show

    clear = kwargs.get('clear',True)
    ymin = kwargs.get('ymin',-0.5)
    ymax = kwargs.get('ymax',3)
    norb = kwargs.get('norb',2)

    if clear: clf()
    plot(x,[V(xi) for xi in x])
    for i in range(norb):
        if use_numpy:
            plot(x,U[:,i])
        else:
            plot(x,U[i,:])
    axis(ymin=ymin,ymax=ymax)
    show()
    return

def matprint(A,**kwargs):
    imin = kwargs.get('imin',0)
    imax = kwargs.get('imax',4)
    jmin = kwargs.get('jmin',imin)
    jmax = kwargs.get('jmax',imax)
    label = kwargs.get('label',None)
    suppress_small = kwargs.get('suppress_small',True)
    if label: print "Matrix ",label
    print array2string(A[imin:imax,jmin:jmax],suppress_small=suppress_small)
    return

def main():
    delta = 1e-8
    n = 100
    xmax = 1.1
    xmin = -xmax
    dx = (xmax-xmin)/float(n-1.)
    x = arange(xmin,xmax+delta,dx)
    Vbox = square_well_factory(V0=100.)
    Vho = harmosc_factory(k=1)
    Vmorse = morse_factory(D=1.,alpha=1.)
    V = Vho
    E,U = Hfd(x,V)
    #plot_results(x,V,U)
    print E[:min(5,n)]/E[0]
    print E[0],E[0]*8/pi/pi, " The latter should be 1"
    x,E,U = HEG(n,V)
    plot_results(x,V,U,clear=False)
    print E[:min(5,n)]/E[0]
    print E[0],E[0]*8/pi/pi, " The latter should be 1"


if __name__ == '__main__': main()
