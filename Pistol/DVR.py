# Taken almost verbatim from the web page at
# http://k2.chem.uh.edu/quantum/Supplement/QDVR/index.html

from math import sin,pi,exp,sqrt
from pylab import plot,show,axis
from numpy import zeros,transpose,diag
from numpy import dot as matmul
from numpy.linalg import eigh

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
    h = m = 1.
    pts,T,KEfbr,w = tcheby(npts,xmin,xmax)
    Vdvr = [V(xi) for xi in pts]
    plot(pts,Vdvr)
    KEfbr = diag(KEfbr)*(h*h/2/m)
    KEdvr = fb2dv(KEfbr,T)
    Vdvr = diag(Vdvr)
    Hdvr =  KEdvr+Vdvr
    return pts,Hdvr

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
    a = kwargs.get('a',1.)
    def V(x): return D*pow(1-exp(-a*(x-X0)),2)-D
    return V

def double_well_factory(**kwargs):
    a = kwargs.get('a',-5.)
    b = kwargs.get('b',1.)
    def V(x): return a*x**2 + b*x**4
    return V

def plotter(x,V,E,U,**kwargs):
    doshow = kwargs.get('doshow',True)
    nplot = kwargs.get('nplot',5)
    ymin = kwargs.get('ymin',-5)
    ymax = kwargs.get('ymax',5)
    plot(x,[V(xi) for xi in x])
    for i in range(nplot):
        if i == 0:
            plot(x,abs(U[:,i])+E[i])
        else:
            plot(x,U[:,i]+E[i])
    axis(ymax=ymax,ymin=ymin)
    if doshow: show()
    return

def morse_test():
    Vmorse = morse_factory(D=3.,a=0.5)
    pts,Hmorse = Hdvr(100,-3.,32.,Vmorse)
    E,U = eigh(Hmorse)
    print E[:5]
    plotter(pts,Vmorse,E,U,ymin=-3,ymax=2)
    return

def double_well_test():
    Vdw = double_well_factory()
    pts,Hdw = Hdvr(100,-3.5,3.5,Vdw)
    E,U = eigh(Hdw)
    plotter(pts,Vdw,E,U,ymin=-7,ymax=3)
    return

if __name__ == '__main__': double_well_test()
    
