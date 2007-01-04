#!/usr/bin/env python
"""SincDVR.py - Radial and Linear kinetic energies matrices via the
Discrete Variable Representation (DVR) from olbert/Miller J. Chem.
Phys 96, 1982 (1992), Appendix A."""

from pylab import *
from numpy import array,zeros,diag,pi
from numpy.linalg import eigh

def LinearKinetic(n,dx):
    """Linear Sinc DVR for the kinetic energy from (-inf,inf) from
    Colbert/Miller J. Chem. Phys 96, 1982 (1992), Appendix A.1."""
    T = zeros((n,n),'d')
    F = 0.5/(dx*dx) # Prefactor
    for i in range(n):
        # i != j
        for j in range(i):
            T[i,j] = F*pow(-1,i-j)*2/pow(i-j,2)
            T[j,i] = T[i,j]
        # i = j
        T[i,i] = F*pi*pi/3.
    return T

def RadialKinetic(n,dr):
    """Radial Sinc Discrete Variable Representation of the kinetic
    energy operator from Colbert/Miller's paper J. Chem. Phys 96, 1982
    (1992), Appendix A.2."""
    T = zeros((n,n),'d')
    F = 0.5/(dr*dr) # Prefactor
    for i in range(n):
        # j != i:
        for j in range(i):
            T[i,j] = F*pow(-1,i-j)*(2.0/pow(float(i-j),2) - 
                                    2.0/pow(float(i+j+2),2))
            T[j,i] = T[i,j]
        # j=i:
        T[i,i] = F*(pi*pi/3.0 - 0.5/pow(float(i+1),2))
    return T

def CoulombFactory(Z=1.0,L=0.0):
    def V(r):
        return -Z/r + 0.5*L*(L+1.0)/(r*r)
    return V

def HarmonicOscillatorFactory(k=1.0):
    def V(x):
        return 0.5*k*x*x
    return V

def HarmonicOscillator(**kwargs):
    n = kwargs.get('n',50)
    xmax = kwargs.get('xmax',6.0)
    doplot = kwargs.get('doplot',True)
    
    dx = 2*xmax/float(n)
    X = array([i*dx-xmax for i in range(n)])
    H = LinearKinetic(n,dx)
    V = HarmonicOscillatorFactory()
    H += diag([V(x) for x in X])

    E,V = eigh(H)
    print E
    if doplot:
        plot(X,V[:,0])
        plot(X,V[:,1])
        plot(X,V[:,2])
        show()
    return            

def Hydrogen():
    n = 100
    Rmax = 10.0
    dr = Rmax/float(n)
    R = [float(i+1)*dr for i in range(n)]
    V = CoulombFactory()
    H = RadialKinetic(n,dr) + diag([V(r) for r in R])
    eval,evec = eigh(H)
    print eval
    r = array([(i+1)*dr for i in range(n)])
    plot(r,abs(evec[:,0]))
    plot(r,evec[:,1])
    show()
    return

def Test():
    Hydrogen()
    #HarmonicOscillator()

if __name__ == '__main__': Test()

    
    
