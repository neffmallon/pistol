
from numpy import array,identity
from pylab import *
from Pistol.fempbox import Tfem,Sfem,geigh

def Exact(npoint=100,hL=6.0,k=1.0):
    # Taken from Fluegge, problem 30.
    nstate=6
    L = 2*hL
    dx = L/float(npoint)
    X = array([-hL+dx*i for i in range(npoint)])
    E = array([0.5,1.5,2.5,3.5,4.5,5.5])
    V = zeros((npoint,nstate),'d')
    
    lam = k # m*k/hbar
    prefac = pow(lam/pi,0.25)
    C0 = prefac
    C1 = prefac*sqrt(2.0*lam)
    C2 = prefac/sqrt(2.0)
    C3 = prefac*sqrt(3.0*lam)
    C4 = prefac*sqrt(3.0/8.0)
    C5 = prefac*sqrt(15.0*lam/4.)

    for i in range(npoint):
        x = X[i]
        x2 = x*x
        x3 = x2*x
        x4 = x2*x2
        x5 = x3*x2
        expax = exp(-0.5*lam*x2)
        V[i,0] = C0*expax
        V[i,1] = C1*x*expax
        V[i,2] = C2*(1-2*lam*x2)*expax
        V[i,3] = C3*(x-2.0*lam*x3/3.)*expax
        V[i,4] = C4*(1-4*lam*x2+4*lam*lam*x4/3.)*expax
        V[i,5] = C5*(x-4*lam*x3/3.+4*lam*lam*x5/15.)*expax

    return X,E,V

def sign(x): return int(x/abs(x))

def femharmosc(n=128,hL=6.0,k=1.0):
    doplot = False
    # hL stands for half-L, since I want the potential to go between +/- L/2
    L = 2*hL
    dx = L/float(n)
    X = [-hL+dx*i for i in range(1,n)]
    T = Tfem(n,L)
    S = Sfem(n,L)
    V = zeros((n-1,n-1),'d')
    for i in range(n-1):
        xi = X[i]
        V[i,i] = 0.5*k*(dx**3/15.  + 2*dx*xi**2/3.)
        if i < n-2:
            V[i,i+1] = V[i+1,i] = 0.5*k*(dx**3/20. + dx**2*xi/6.  + dx*xi**2/6.)
    eval,evec = geigh(T+V,S)
    print eval[:6]
    if doplot:
        Xx,Ex,Vx = Exact(100,hL)
        print eval[:min(5,n)]
        phase0 = sign(evec[5,0])/sign(Vx[5,0])
        plot(X,phase0*evec[:,0],'bo',label="0 FEM/32")
        plot(Xx,Vx[:,0],'b-',label="0 Exact")
        phase1 = sign(evec[5,1])/sign(Vx[5,1])
        plot(X,phase1*evec[:,1],'go',label="1 FEM/32")
        plot(Xx,Vx[:,1],'g-',label="1 Exact")
        title("Harmonic oscillator wave functions")
        xlabel("x")
        legend()
        savefig("/Users/rmuller/Documents/tex/fem-pbox/fem-harmosc.eps")
        show()
    return

if __name__ == '__main__': femharmosc()
