#!/usr/bin/env python
"""\
SphericalAtom.py - Construct radial wave functions corresponding to
  spherical atoms of different atomic numbers.
"""

from Pistol.DVRSinc import RadialKinetic,CoulombFactory

# Default occupations for the various shells, based on the number of
# electrons. There are all kinds of neat stuff we can do with this
# later, such as using fractional occupations that give the best
# reproduction of the chemistry.
defaultAtoms = [
    None,
    [(1,0,1.0)],                                           #H  
    [(1,0,2.0)],                                           #He 
    [(1,0,2.0),(2,0,1.0)],                                 #Li 
    [(1,0,2.0),(2,0,2.0)],                                 #Be 
    [(1,0,2.0),(2,0,2.0),(2,1,1.0)],                       #B  
    [(1,0,2.0),(2,0,2.0),(2,1,2.0)],                       #C  
    [(1,0,2.0),(2,0,2.0),(2,1,3.0)],                       #N  
    [(1,0,2.0),(2,0,2.0),(2,1,4.0)],                       #O  
    [(1,0,2.0),(2,0,2.0),(2,1,5.0)],                       #F  
    [(1,0,2.0),(2,0,2.0),(2,1,6.0)],                       #Ne 
    [(1,0,2.0),(2,0,2.0),(2,1,6.0),(3,0,1.0)],             #Na 
    [(1,0,2.0),(2,0,2.0),(2,1,6.0),(3,0,2.0)],             #Mg 
    [(1,0,2.0),(2,0,2.0),(2,1,6.0),(3,0,2.0),(3,1,1.0)],   #Al 
    [(1,0,2.0),(2,0,2.0),(2,1,6.0),(3,0,2.0),(3,1,2.0)],   #Si 
    [(1,0,2.0),(2,0,2.0),(2,1,6.0),(3,0,2.0),(3,1,3.0)],   #P  
    [(1,0,2.0),(2,0,2.0),(2,1,6.0),(3,0,2.0),(3,1,4.0)],   #S  
    [(1,0,2.0),(2,0,2.0),(2,1,6.0),(3,0,2.0),(3,1,5.0)],   #Cl 
    [(1,0,2.0),(2,0,2.0),(2,1,6.0),(3,0,2.0),(3,1,6.0)],   #Ar
    ]

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

    # ePerShell is given as a list of tuples: [(N,L,eLM)]. Currently it
    # is computed based on the number of electrons, but I will later
    # give the option to pass this in
    ePerShell = defaultAtoms[Nel]

    dr = Rmax/float(N)
    R = [float(i+1)*dr for i in range(N)]
    T = RadialKinetic(N,dr)

    # solve for the one-electron solutions
    for nval,lval,f in ePerShell:
        Vl[(nval,lval)] = CoulombFactory(Z,lval)

        # Solve the one-electron system

        # Update the density with this component

    # Start the SCF iterations
    for iter in range(MaxIter):
        # Solve the Poisson problem to get the potential

        # Get the XC functional on the radial grid

        # Solve for each component of the wave function and update the density
        for nval,lval,f in ePerShell:
            Vl[(nval,lval)] = CoulombFactory(Z,lval)

            # Solve

            # update the density

        # Compute the total energy and test for convergence.
    return


        

    


    
    
    
