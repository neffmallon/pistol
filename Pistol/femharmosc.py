
from numpy import array,identity
from pylab import *
from Pistol.fempbox import Tfem,Sfem,geigh


def femharmosc(n=20,hL=0.5,k=1.0):
    # hL stands for half-L, since I want the potential to go between +/- L
    L = 2*hL
    dx = L/float(n)
    T = Tfem(n,L)
    S = Sfem(n,L)
    V = identity(n-1,'d')*k*dx**3/30. # yuck!
    eval,evec = geigh(T+V,S)
    print eval[:min(10,n)]
    #plot(evec[:,0])
    #show()
    return

if __name__ == '__main__': femharmosc()
