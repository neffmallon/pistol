"""\
Use a simple Discrete Variable Representation method to solve
one-dimensional potentials.

A good general introduction to DVR methods is
Light and Carrington, Adv. Chem. Phys. 114, 263 (2000)
"""

from pylab import plot,show,axis
from numpy import zeros,transpose,diag,array,dot,sin,pi,exp,sqrt
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

    The program here is taken almost verbatim from Eric Bittner's web
    page at: http://k2.chem.uh.edu/quantum/Supplement/QDVR/index.html

    """
    delta = xmax-xmin
    pts = [xmin+i*delta/(npts+1.) for i in range(1,npts+1)]
    KEfbr = [(i*pi/delta)**2 for i in range(1,npts+1)]
    w = [delta/(npts+1.) for i in range(1,npts+1)]
    T = zeros((npts,npts),'d')
    for i in range(1,npts+1):
        for j in range(1,npts+1):
            T[i-1,j-1] = sqrt(2/(npts+1.))*sin(i*j*pi/(npts+1.))
    return array(pts), T,KEfbr, w

def simx(A,B,trans='N'):
    """\
    C = simx(A,B,trans)
    Perform the similarity transformation C = B'*A*B (trans='N') or
    C = B*A*B' (trans='T').
    """
    if trans.lower().startswith('t'):
        return dot(B,dot(A,transpose(B)))
    return dot(transpose(B),dot(A,B))
    
def dv2fb(DVR,T):
    """Transform a matrix from the discrete variable representation
    to the finite basis representation"""
    return simx(DVR,T,'T')

def fb2dv(FBR,T):
    """Transform a matrix from the finite basis representation to the
    discrete variable representation."""
    return simx(FBR,T,'N')

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
    #plot(pts,Vdvr)
    KEfbr = diag(KEfbr)*(0.5*h*h/m)
    KEdvr = fb2dv(KEfbr,T)
    Vdvr = diag(Vdvr)
    Hdvr =  KEdvr+Vdvr
    return pts,Hdvr

def square_well_test():
    from PotentialFactories import SquareWellFactory
    from Exact import ExactSquareWell
    xmax = 0.6
    xmin = -xmax
    npts = 100
    Vw = SquareWellFactory(L=0.5,Depth=1e8)
    pts,Hw = Hdvr(npts,xmin,xmax,Vw)
    E,U = eigh(Hw)
    dx = (xmax-xmin)/float(npts)
    renorm = 1/sqrt(dx)
    Xx,Ex,Vx = ExactSquareWell(2,100,1.0)
    plot(pts,renorm*abs(U[:,0]),'bo')
    plot(pts,-renorm*U[:,1],'go')
    plot(Xx-0.5,Vx[:,0],'b-')
    plot(Xx-0.5,Vx[:,1],'g-')
    show()
    return

def radial_test():
    from Exact import ExactH
    from PotentialFactories import CoulombFactory
    V = CoulombFactory()
    npts=100
    xmax = 20.
    xmin = 0.
    pts,Hrad = Hdvr(npts,xmin,xmax,V)
    E,U = eigh(Hrad)
    dx = (xmax-xmin)/float(npts)
    plot(pts,abs(U[:,0])/sqrt(pts*pts*dx),'bo')
    F = ExactH(1,0.0,1.0)
    plot(pts,[F(r) for r in pts],'b-')
    plot(pts,-U[:,1]/sqrt(pts*pts*dx),'go')
    F = ExactH(2,0.0,1.0)
    plot(pts,[F(r) for r in pts],'g-')
    show()

def HarmonicOscillatorTest(**kwargs):
    from PotentialFactories import HarmonicOscillatorFactory
    n = kwargs.get('n',50)
    xmax = kwargs.get('xmax',6.0)
    doplot = kwargs.get('doplot',True)
    
    V = HarmonicOscillatorFactory()
    pts,H = Hdvr(n,-xmax,xmax,V)

    # The wave functions that DVR outputs are different than the exact solution,
    #  and one needs to multiply by 1/sqrt(dx) to convert the DVR output to
    #  the exact value.
    dx = 2*xmax/float(n)
    normfact = 1/sqrt(dx)

    E,U = eigh(H)
    print E[:10]
    if doplot:
        plot(pts,normfact*U[:,0])
        plot(pts,normfact*U[:,1])
        plot(pts,normfact*U[:,2])
        show()
    return

if __name__ == '__main__':
    #square_well_test()
    #radial_test()
    HarmonicOscillatorTest()
    
