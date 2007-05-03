#!/usr/bin/env python
"""Sinc.py - Radial and Linear kinetic energies matrices via the
Discrete Variable Representation (DVR) from Colbert/Miller J. Chem.
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

def SquareWellTest():
    from PotentialFactories import SquareWellFactory
    from Exact import ExactSquareWell
    n = 128
    xmax = 0.6
    dx = 2*xmax/float(n-1)
    X = array([i*dx-xmax for i in range(n)])
    H = LinearKinetic(n,dx)
    V = SquareWellFactory(L=0.5,Depth=1e8)
    H += diag([V(x) for x in X])

    Xx,Ex,Vx = ExactSquareWell(2,100,1.0)
    E,V = eigh(H)

    # The wave functions that DVR outputs are different than the exact solution,
    #  and one needs to multiply by 1/sqrt(dx) to convert the DVR output to
    #  the exact value.
    normfact = 1/sqrt(dx)
    plot(X,normfact*abs(V[:,0]),'bo',label="dvr")
    plot(Xx-0.5,abs(Vx[:,0]),'b-',label="exact") # shift the solutions
    plot(X,normfact*V[:,1],'go',label="dvr")
    plot(Xx-0.5,Vx[:,1],'g-',label="exact") 
    legend()
    #plot(X,V[:,1])
    #plot(X,V[:,2])
    show()
    return            
    
def HarmonicOscillatorTest(**kwargs):
    from PotentialFactories import HarmonicOscillatorFactory
    n = kwargs.get('n',50)
    xmax = kwargs.get('xmax',6.0)
    doplot = kwargs.get('doplot',True)
    
    dx = 2*xmax/float(n)
    X = array([i*dx-xmax for i in range(n)])
    H = LinearKinetic(n,dx)
    V = HarmonicOscillatorFactory()
    H += diag([V(x) for x in X])

    # The wave functions that DVR outputs are different than the exact solution,
    #  and one needs to multiply by 1/sqrt(dx) to convert the DVR output to
    #  the exact value.
    normfact = 1/sqrt(dx)

    E,V = eigh(H)
    print E
    if doplot:
        plot(X,normfact*V[:,0])
        plot(X,normfact*V[:,1])
        plot(X,normfact*V[:,2])
        show()
    return

def sign(x): return int(x/abs(x))

def HydrogenTest():
    from PotentialFactories import CoulombFactory
    from Exact import ExactH
    Z = 1.0
    L = 0
    n = 50
    Rmax = 20.0
    dr = Rmax/float(n)
    R = [float(i+1)*dr for i in range(n)]
    V = CoulombFactory()
    H = RadialKinetic(n,dr) + diag([V(r) for r in R]) 
    eval,evec = eigh(H)
    print eval
    # The wave functions that DVR outputs are different than the exact solution,
    #  and one needs to multiply by 1/sqrt(r**2*dr) to convert the DVR output to
    #  the exact value.
    F1 = ExactH(1,L,Z)
    F1dvr = [abs(evec[i,0])/sqrt(r*r*dr) for i,r in enumerate(R)]
    plot(R,F1dvr,'bo',label='1s DVR')
    plot(R,[F1(r) for r in R],'b-',label='1s exact')

    F2 = ExactH(2,L,Z)
    F2dvr = array([evec[i,1]/sqrt(r*r*dr)  for i,r in enumerate(R)])
    phase = sign(F2(R[1]))/sign(F2dvr[1])
    plot(R,phase*F2dvr,'go',label='2s DVR')
    plot(R,[F2(r) for r in R],'g-',label='2s exact')
    legend()
    show()
    return

def Test():
    #SquareWellTest()
    HydrogenTest()
    #HarmonicOscillatorTest()

if __name__ == '__main__': Test()

    
    
