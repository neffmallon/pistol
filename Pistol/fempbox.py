#!/usr/local/bin/python

from Pistol.DVRSinc import LinearKinetic
from numpy import zeros,diag,pi,transpose
from numpy import dot as mm
from numpy.linalg import eigh
from pylab import *

def canorth(B):
    E,V = eigh(B)
    n = len(E)
    for i in range(n):
        for j in range(n):
            V[i,j] = V[i,j]/sqrt(E[j])
    return V

def simxfrm(A,B):
    return mm(transpose(B),mm(A,B))

def geigh(A,B):
    X = canorth(B)
    E,V = eigh(simxfrm(A,X))
    return E,mm(V,A)

def epbox(n,L):
    """
    Recall that the analytic eigenvalues for a particle in a box
    are En = 0.5*n**2*pi**2/L**2
    """
    return [0.5*i*i*pi*pi/L/L for i in range(1,n+1)]

def Hdvr(n=100,L=1.,Vbig = 1e7):
    dx = L/float(n)
    T = LinearKinetic(n+1,dx)
    V = zeros(n+1,'d')
    V[0] = V[-1] = Vbig
    return T + diag(V)

def dvrpbox(n=100,L=1.,Vbig = 1e7):
    """
    Use a n+1 point DVR to solve the particle in an infinite box
    from x=0 to x=L.
    """
    H = Hdvr(n,L,Vbig)
    E,V = eigh(H)

    print E[:5]
    print epbox(5,L)

    #plot(V[:,0])
    #plot(V[:,1])
    #show()
    return

def Tfem(n=100,L=1.):
    dx = L/float(n)
    T = zeros((n-1,n-1),'d')
    for i in range(n-1):
        T[i,i] = 1.0/dx
        if i:
            T[i,i-1] = T[i-1,i] = -0.5/dx
    return T

def Sfem(n=100,L=1.):
    dx = L/float(n)
    S = zeros((n-1,n-1),'d')
    for i in range(n-1):
        S[i,i] = 2.0*dx/3.0
        if i:
            S[i,i-1] = S[i-1,i] = dx/6.0
    return S

def fempbox(n=100,L=1.):
    T = Tfem(n,L)
    S = Sfem(n,L)
    E,V = geigh(T,S)
    Edvr,Vdvr = eigh(Hdvr(n,L))
    Eexact = epbox(10,L)
    print "  #     Exact     DVR       FEM"
    for i in range(10):
        print "%4d %10.4f %10.4f %10.4f" % (i+1,Eexact[i],Edvr[i],E[i])
    # Something's wrong in the canonical orthogonalization,
    # since the eigenvalues are correct, but the eigenvectors
    # are all messed up.
    
    plot(V[:,0])
    plot(V[:,1])
    plot(Vdvr[:,0])
    plot(Vdvr[:,1])
    show()
    return

if __name__ == '__main__':
    #dvrpbox()
    fempbox()

