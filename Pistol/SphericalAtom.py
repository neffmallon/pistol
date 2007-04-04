#!/usr/bin/env python
"""\
SphericalAtom.py - Construct radial wave functions corresponding to
  spherical atoms of different atomic numbers.
"""

from Pistol.DVRSinc import RadialKinetic,CoulombFactory
from Pistol.Element import symbol
from pylab import *
from numpy import zeros,array,pi
from numpy.linalg import eigh

# Default occupations for the various shells, based on the number of
# electrons. There are all kinds of neat stuff we can do with this
# later, such as using fractional occupations that give the best
# reproduction of the chemistry.
defaultAtoms = [
    None,
    [1.0],
    [2.0], # He
    [2.0,1.0],
    [2.0,2.0],
    [2.0,2.0,1.0],
    [2.0,2.0,2.0],
    [2.0,2.0,3.0],
    [2.0,2.0,4.0],
    [2.0,2.0,5.0],
    [2.0,2.0,6.0],  # Ne
    [2.0,2.0,6.0,1.0],
    [2.0,2.0,6.0,2.0],
    [2.0,2.0,6.0,2.0,1.0],
    [2.0,2.0,6.0,2.0,2.0],
    [2.0,2.0,6.0,2.0,3.0],
    [2.0,2.0,6.0,2.0,4.0],
    [2.0,2.0,6.0,2.0,5.0],
    [2.0,2.0,6.0,2.0,6.0], # Ar
    [2.0,2.0,6.0,2.0,6.0,1.0],
    [2.0,2.0,6.0,2.0,6.0,2.0],
    [2.0,2.0,6.0,2.0,6.0,2.0,1.0],
    [2.0,2.0,6.0,2.0,6.0,2.0,2.0],
    [2.0,2.0,6.0,2.0,6.0,2.0,3.0],
    [2.0,2.0,6.0,2.0,6.0,2.0,4.0],
    [2.0,2.0,6.0,2.0,6.0,2.0,5.0],
    [2.0,2.0,6.0,2.0,6.0,2.0,6.0],
    [2.0,2.0,6.0,2.0,6.0,2.0,7.0],
    [2.0,2.0,6.0,2.0,6.0,2.0,8.0],
    [2.0,2.0,6.0,2.0,6.0,2.0,9.0],
    [2.0,2.0,6.0,2.0,6.0,2.0,10.0], # Zn
    ]

# This is the periodic table ordering, which is not necessarily correct
shell_order = [ (1,0), (2,0), (2, 1),           # 1s, 2s, 2p
                (3, 0), (3, 1),                 # 3s, 3p
                (4, 0), (3, 2), (4, 1),         # 4s, 3d, 4p
                (5,0), (4, 2), (5, 1),          # 5s, 4d, 5p
                (6,0), (4, 3), (5, 2), (6, 1),  # 6s, 4f, 5d, 6p
                (7,0), (5, 3), (6, 2), (7, 1)]  # 7s, 5f, 6d, 7p

# Number of electrons in a shell of a given angular momentum (l)
fmax = [2.0, 6.0, 10.0, 14.0]

def get_lmax(e_per_shell,**opts):
    """\
    Given a list of shell occupations in e_per_shell, generate the
    highest occupied l value:

    >>> get_lmax(defaultAtoms[1]) # Hydrogen
    0
    >>> get_lmax(defaultAtoms[3]) # Lithium
    0
    >>> get_lmax(defaultAtoms[6]) # Carbon
    1
    >>> get_lmax([2,2,0,0]) # Be, with extra zero occupations
    0
    """
    lmax = 0
    for i,fval in enumerate(e_per_shell):
        nval,lval = shell_order[i]
        if fval > 0: lmax = max(lmax,lval)
    return lmax

def fs_per_l(l,e_per_shell):
    """\
    Given a list of shell occupations in e_per_shell, return a
    list of the occupations of a given l value:

    >>> fs_per_l(1,[1.0])
    []
    >>> fs_per_l(0,[1.0])
    [1.0]

    Must handle empty shells correctly:
    >>> fs_per_l(0,[0.0])
    []

    Carbon
    >>> fs_per_l(0,defaultAtoms[6])
    [2.0, 2.0]

    In carbon there are 2 electrons in the lowest p orbitals, thus
    we return [2.0], rather than [0.0, 2.0] (since there's no such
    thing as a 1p orbital:
    >>> fs_per_l(1,defaultAtoms[6])
    [2.0]

    Potassium
    >>> fs_per_l(0,defaultAtoms[19])
    [2.0, 2.0, 2.0, 1.0]
    >>> fs_per_l(1,defaultAtoms[19])
    [6.0, 6.0]
    >>> fs_per_l(2,defaultAtoms[19])
    []
    """
    fvals = []
    for i,fval in enumerate(e_per_shell):
        nval,lval = shell_order[i]
        if lval == l and fval > 0:
            fvals.append(fval)
    return fvals

def SphericalAtom(Z,**kwargs):
    """\

    SphericalAtom -- Construct radial wave functions for spherical atoms

    [psis] = SphericalAtom(Z,ePerShell,**kwargs)

    Given a nuclear charge an a (possibly fractional) number of
    electrons per shell, return radial wave functions for
    relevant shells.

    Z         integer   The nuclear charge
    ePerShell [double]  The number of electrons per shell

    The following parameters can be passed in as keyword arguments:
    Rmax      double    The maximum radius (default=10.0)
    N         integer   The number of grid points (default=100)
    Charge    integer   The integral charge on the system (default=0)

    """
    Rmax = kwargs.get('Rmax',10.0)
    N = kwargs.get('N',100)
    Charge = kwargs.get('Charge',0.0)
    Nel = int(Z-Charge)

    # e_per_shell is given as a list of tuples: [(N,L,eLM)]. Currently it
    # is computed based on the number of electrons, but I will later
    # give the option to pass this information in
    e_per_shell = defaultAtoms[Nel]

    dr = Rmax/float(N)
    R = array([float(i+1)*dr for i in range(N)])
    T = RadialKinetic(N,dr)

    lmax = get_lmax(e_per_shell)
    Vl = [CoulombFactory(Z,lval) for lval in range(lmax)]
    rho = zeros(N,'d')

    # solve for the one-electron solutions
    for l in range(lmax+1):
        V = CoulombFactory(Z,l)
        H = RadialKinetic(N,dr)
        for j in range(N): H[j,j] += V(R[j])
        
        # Solve the one-electron system
        eval,evec = eigh(H)
        for i in range(3):
            print i,l,Z,eval[i],-0.5*pow(Z/(i+1.),2)

        # Update the density with this component
        for i,fi in enumerate(fs_per_l(l,e_per_shell)):
            occ = 2*fi/fmax[l] 
            rho += occ*evec[:,i]**2
    return rho

def test():
    import doctest
    doctest.testmod()

def main():
    rho = SphericalAtom(1)
    N = len(rho)
    dr = 10.0/float(N)
    R = array([float(i+1)*dr for i in range(N)])

    #for nel in range(1,7):
    for nel in [3]:
        rho = 4*pi*SphericalAtom(nel)
        plot(R,rho,label=symbol[nel])
    legend()
    axis(xmax=5.1)
    xlabel("R/bohr")
    ylabel("rho")
    title("Electron density of different atoms")
    show()
    
if __name__ == '__main__':  main()
