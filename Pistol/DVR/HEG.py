#!/usr/bin/env python
"""
Solve 1-D potentials via the method of Harris, Engerholm, and Gwinn.
See JCP 43, 1515 (1965).

Status: works for eigenvalues for Harmonic and morse potentials.
Does not work for wave functions. Doing something wrong with the transforms.
"""

from math import sqrt,pi,exp,sin

from numpy import zeros,arange,transpose,diag,array2string
from numpy import dot as matmul
from numpy.linalg import eigh
from pylab import plot,clf,axis,show

def HEG(n,V):
    X = zeros((n,n),'d')
    for i in range(n):
        if i > 0:
            X[i,i-1] = X[i-1,i] = sqrt(i)/sqrt(2)
    # Eq 1 from HEG
    lam,T = eigh(X)
    print lam

    # Form the potential matrix
    # Eq 2 from HEG
    Vx = [V(li) for li in lam]
    Vho = matmul(T,matmul(diag(Vx),transpose(T)))

    KEho = zeros((n,n),'d')
    for i in range(n):
        KEho[i,i] = 0.25*(2*i+1)
        if i > 1:
            KEho[i,i-2] = KEho[i-2,i] = -0.25*sqrt(i-1)*sqrt(i)
    Hho = KEho+Vho
    Hx = matmul(transpose(T),matmul(Hho,T))
    E,U = eigh(Hho)

    # The eigenvectors are in terms of the HO eigenvectors, so
    # we have to multiply by X before returning
    return lam,E,matmul(transpose(T),U)

def HEG2(n,V):
    """\
    Does the diagonalization in the discrete variable representation
    """
    X = zeros((n,n),'d')
    for i in range(n):
        if i > 0:
            X[i,i-1] = X[i-1,i] = sqrt(i)/sqrt(2)
    # Eq 1 from HEG
    lam,T = eigh(X)

    KEho = zeros((n,n),'d')
    for i in range(n):
        KEho[i,i] = 0.25*(2*i+1)
        if i > 1:
            KEho[i,i-2] = KEho[i-2,i] = -0.25*sqrt(i-1)*sqrt(i)

    KEx = matmul(transpose(T),matmul(KEho,T))
    #KEx = matmul(T,matmul(KEho,transpose(T)))

    # Form the potential matrix
    # Eq 2 from HEG
    Vx = diag([V(li) for li in lam])

    Hx = KEx + Vx
    print "x\n",lam[:5]
    #from scipy.special.orthogonal import h_roots
    #print h_roots(n)
    
    matprint(KEx,label="T")
    matprint(Vx,label="V")
    matprint(Hx,label="H")
    
    E,U = eigh(Hx)
    return lam,E,U

def Tfd(n,dx):
    "Form a finite-difference kinetic energy operator"
    a = 1./dx/dx
    H = zeros((n,n),'d')
    for i in range(n):
        H[i,i] = a
        if i > 0:
            H[i,i-1] = H[i-1,i] = -0.5*a
    return H

def Hfd(n,xmin,xmax,V):
    delta = 1e-8
    dx = (xmax-xmin)/float(n-1.)
    x = arange(xmin,xmax+delta,dx)

    T = Tfd(n,dx)  # Form the KE operator
    Vfd = diag([V(xi) for xi in x])
    H = T+Vfd
    
    E,U = eigh(H)
    print "x\n",x[:5]
    matprint(T,label="T")
    matprint(Vfd,label="V")
    matprint(H,label="H")
    return x,E,U

def tcheby(npts,xmin,xmax):
    delta = xmax-xmin
    pts = [xmin+i*delta/(npts+1.) for i in range(1,npts+1)]
    KEfbr = [(i*pi/delta)**2 for i in range(1,npts+1)]
    w = [delta/(npts+1.) for i in range(1,npts+1)]
    T = zeros((npts,npts),'d')
    for i in range(1,npts+1):
        for j in range(1,npts+1):
            T[i-1,j-1] = sqrt(2/(npts+1.))*sin(i*j*pi/(npts+1.))
    return pts, T,KEfbr, delta

def dv2fb(DVR,T): return matmul(T,matmul(DVR,transpose(T)))
def fb2dv(FBR,T): return matmul(transpose(T),matmul(FBR,T))

def Hdvr(npts,xmin,xmax,V):
    m = 1.
    h = 1.
    pts,T,KEfbr,w = tcheby(npts,xmin,xmax)
    Vdvr = [V(xi) for xi in pts]
    plot(pts,Vdvr)
    KEfbr = diag(KEfbr)*(h*h/2/m)
    KEdvr = fb2dv(KEfbr,T)
    Vdvr = diag(Vdvr)
    Hdvr =  KEdvr+Vdvr
    print "x\n",pts[:5]
    matprint(KEdvr,label="T")
    matprint(Vdvr,label="V")
    matprint(Hdvr,label="H")
    E,U = eigh(Hdvr)
    return pts,E,U

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
    from PotentialFactories import SquareWellFactory
    from Exact import ExactSquareWell
    npts = 30
    V = SquareWellFactory(L=5.0,Depth=1e8)

    x,E,U = HEG2(npts,V)
    plot(x,U[:,0])
    show()
    print E[:5]


if __name__ == '__main__': main()
