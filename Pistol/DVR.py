"""\
Use a simple Discrete Variable Representation method to solve
one-dimensional potentials.

The program here is taken almost verbatim from Eric Bittner's web page at:
http://k2.chem.uh.edu/quantum/Supplement/QDVR/index.html

A good general introduction to DVR methods is
Light and Carrington, Adv. Chem. Phys. 114, 263 (2000)
"""

from math import sin,pi,exp,sqrt
from pylab import plot,show,axis
from numpy import zeros,transpose,diag
from numpy import dot as matmul
from numpy.linalg import eigh

def tcheby(npts,xmin,xmax):
    """\
    pts,T,KE,w = tcheby(npts,xmin,xmax)

    Returns the quadrature points, the transformation matrix, the
    kinetic energy operator, and the quadrature weights corresponding
    to a Chebyshev-based discrete variable representation.

    npts    The number of points in the quadrature
    xmin    The minimum value of x for the quadrature
    xmax    The maximum value of x for the quadrature
    """
    delta = xmax-xmin
    pts = [xmin+i*delta/(npts+1.) for i in range(1,npts+1)]
    KEfbr = [(i*pi/delta)**2 for i in range(1,npts+1)]
    w = [delta/(npts+1.) for i in range(1,npts+1)]
    T = zeros((npts,npts),'d')
    for i in range(1,npts+1):
        for j in range(1,npts+1):
            T[i-1,j-1] = sqrt(2/(npts+1.))*sin(i*j*pi/(npts+1.))
    return pts, T,KEfbr, w


def dv2fb(DVR,T):
    """Transform a matrix from the discrete variable representation
    to the finite basis representation"""
    return matmul(T,matmul(DVR,transpose(T)))
def fb2dv(FBR,T):
    """Transform a matrix from the finite basis representation to the
    discrete variable representation."""
    return matmul(transpose(T),matmul(FBR,T))

def Hdvr(npts,xmin,xmax,V):
    """\
    pts,H = Hdvr(npts,xmin,xmax,V)

    Generate a DVR Hamiltonian for the potential V (one-d function)
    and return the Hamiltonian and the quadrature points.

    npts      The number of points to be used in the quadrature
    xmin      The minimum value of the dependent variable
    xmax      The maximum value of the dependent variable
    V         A one-dimensional function of x
    """
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
# A factory is a function that makes a function. 
def square_well_factory(**kwargs):
    """
    V = square_well_factory(**kwargs)

    returns a function of a single variable:

    V0 = V(0)

    Key word arguments:

    V0    The well-depth of the potential. Default=1
    A     The width of the potential well. Default=1

    Thus, the potential looks like this:

         (-A,V0)              (A,V0)                                   
    ------------       +       ----------------
               |               |
               |               |
               |               |
               |               |
        (-A,0) |-------+-------|(A,0)
                     (0,0)
    
    """
    V0 = kwargs.get('V0',1.)
    A = kwargs.get('A',1.)
    def V(x):
        if abs(x) < A: return 0
        return V0
    return V

def double_square_well_factory(**kwargs):
    """
    V = double_square_well_factory(**kwargs)

    Returns a one-dimensional potential function that represents
    a double-square-well potential

    Options
    V0      The depth of the well. Default=1
    A       The inner boundary of the well. Default=1
    B       The outer boundary of the well. Default=1
    
         (-B,V0)       (-A,V0)   (A,V0)      (B,V0)
    ----------            ---------            ---------- 
             |            |       |            |
             |            |       |            |
             |            |       |            |
             |            |       |            |
             |____________|   +   |____________|
                            (0,0)
    """
    V0 = kwargs.get('V0',1.)
    A = kwargs.get('A',1.)
    B = kwargs.get('B',2.)
    def V(x):
        if A < abs(x) < B: return 0
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
    doshow = kwargs.get('doshow',False)
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

def radial_test():
    def Vrad(r): return -1

if __name__ == '__main__': double_well_test()
    
