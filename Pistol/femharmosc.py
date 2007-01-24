
from numpy import array

from Pistol.fempbox import Tfem,Sfem,gheigh

def femharmosc(n=16,hL=0.5,k=1.0):
    # hL stands for half-L, since I want the potential to go between +/- L
    L = 2*hL
    T = Tfem(n,L)
    S = Sfem(n,L)
    x = array([float(L*j)/float(n)-hL for j in range(1,n)])
    V = 0.5*k*x**2
    eval,evec = gheigh(T+V,S)
    print eval
    return

if __name__ == '__main__': femharmosc()
