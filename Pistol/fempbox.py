#!/usr/local/bin/python

from Pistol.DVRSinc import LinearKinetic
from numpy import zeros,diag,pi,transpose,sqrt,sin,array
from numpy import dot as mm
from numpy.linalg import eigh
from pylab import *

def canorth(B):
    E,V = eigh(B)
    n = len(E)
    for i in range(n):
        V[:,i] /= sqrt(E[i])
    return V

def simxfrm(A,B): return mm(transpose(B),mm(A,B))
def simxfrmt(A,B): return mm(B,mm(A,transpose(B)))

def geigh(A,B):
    X = canorth(B)
    E,V = eigh(simxfrm(A,X))
    return E,mm(X,V)

def Exact(nstate,npoint,L):
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

def fempbox(n=16,L=1.):
    ncalc = 8
    T = Tfem(n,L)
    S = Sfem(n,L)
    x = array([float(L*j)/float(n) for j in range(1,n)])
    E,V = geigh(T,S)
    xx,Ex,Vx = Exact(ncalc,200,L)
    print "  #     Exact     FEM"
    for i in range(ncalc):
        print "%4d %10.4f %10.4f" % (i+1,Ex[i],E[i])

    # phasefactors
    phase1 = int(V[1,1]/abs(V[1,1])*abs(Vx[1,1])/Vx[1,1])
    # Plot out the data
    plot(x,abs(V[:,0]),'bo',label="1 FEM/%d" % n)
    plot(xx,abs(Vx[:,0]),label="1 Exact")
    plot(x,phase1*V[:,1],'go',label="2 FEM/%d" % n)
    plot(xx,Vx[:,1],label="2 Exact")
    title("Particle in a box wave functions")
    xlabel("x")
    legend(loc="lower left")
    #savefig("fembox-wfns.eps")
    show()
    return

if __name__ == '__main__':
    fempbox()

