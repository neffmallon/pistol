
from math import exp,log,sqrt,pi
from numpy import zeros,array,dot
from numpy.linalg import eigvalsh
from Pistol.Element import mass

NA = 6.02e23 # molecules/mol

def qtot(atoms,vibes,T=300,rotsym=1,emult=1):
    """\
    q = qtot(atoms,vibes)
    Compute the total partition function given
    atoms    List of (atno,(x,y,z)) for each atom
    vibes    List of the vibrational frequencies in cm-1
    T        Temperature in Kelvin
    rotsym   Rotational symmetry number
    emult    Electronic multiplicity (degeneracy)

    Total partition function for OH:
    >>> qtot([(1,(0,0,0)),(35,(1.42,0,0))],[2650])
    1.77688605503e+34
    >>> qtot([(1,(0,0,0)),(35,(1.42,0,0))],[2650],300,1,1)
    1.77688605503e+34
    """
    return (qtrans(totmass(atoms),T)*qrot(atoms,rotsym,T)*qvibes(vibes,T)*
            emult)

def qtrans(m=1,T=300):
    """\
    qt = qtrans(m,T)     

    Compute the translational partition function given
    m    Mass in amu
    T    Temperature in Kelvin

    Units of m^-3

    >>> qtrans(mass[1])
    9.8918583708839351e+29
    >>> qtrans(mass[1],400)
    1.5229512248574643e+30
    >>> qtrans(mass[1]+mass[35])
    7.1898259556826252e+32
    >>> qtrans(mass[1]+mass[35],300)
    7.1898259556826252e+32
    """
    return 9.88e29*pow(m*T/300,1.5) # From Fowler, also Laidler
    
def qrot(atoms,rotsym=1,T=300):
    """\
    qr = qrot(atoms,rotsym)
    
    Compute the rotational partition function given
    atoms    List of (atno,(x,y,z)) for each atom
    rotsym   The rotational symmetry number for the system
    T    Temperature in Kelvin

    Dimensionless units

    >>> qrot([])
    1
    >>> qrot([(1,(0,0,0))])
    1
    >>> qrot([(1,(0,0,0)),(35,(1.42,0,0))])
    24.7138213335

    >>> qrot([(1,(0,0,0)),(35,(1.42,0,0))],1,300)
    24.7138213335

    # Need a triatomic unit test. Water?
    """
    if len(atoms) <= 1: return 1
    moments = inertia(atoms)
    if min(moments) <= 1e-8:
        # Linear molecule
        return 12.4*(T/300.0)*max(moments)/rotsym
    A,B,C = 16.85763042/moments
    return sqrt(pi/(A*B*C))*pow(T,1.5)/rotsym

def qvibes(vibes,T=300):
    """\
    qv = qvibes(vibes,T)

    Compute the vibrational partition function given
    vibes    List of the vibrational frequencies in cm-1
    T        Temperature in Kelvin

    Dimensionless units
    >>> qvibes([2650])
    1.0000029907181684
    >>> qvibes([460.,460.,2340.])
    1.2622574112462328
    >>> qvibes([460.,460.,2340.],300)
    1.2622574112462328
    """
    if len(vibes) == 0: return 1
    return prod([qvibe(v,T) for v in vibes])
    
def qvibe(v,T=300):
    """\
    qv = qvibe(v,T)
    Compute the vibrational partition function for a single vibration given
    v        The vibrational frequency in cm-1
    T        Temperature in Kelvin

    Dimensionless units
    >>> qvibe(2650)
    1.0000029907181684

    >>> qvibe(2650,300)
    1.0000029907181684
    """
    return 1/(1-exp(-hv_kT(v,T)))

def hv_kT(v,T=300):
    """\
    The energy associated with a vibration v (cm-1)

    >>> hv_kT(1)
    0.0047999999999999996
    >>> hv_kT(2650)
    12.719999999999999
    >>> hv_kT(2650,300)
    12.719999999999999
    """
    return 4.8e-3*v*T/300.0

def com(atoms):
    """\
    x,y,z = com(atoms)

    Compute the center of mass of a groups of atoms where
    atoms    List of (atno,(x,y,z)) for each atom

    Units are A,A,A

    >>> com([(1,(0,0,0))])
    array([ 0.,  0.,  0.])

    >>> com([(1,(0,0,1.5)),(1,(0,0,-1.5))])
    array([ 0.,  0.,  0.])
    """
    mtot = totmass(atoms)
    xyzcom = zeros(3,'d')
    for atno,xyz in atoms: xyzcom += mass[atno]*array(xyz,'d')
    return xyzcom/mtot
    
def prod(list):
    """\
    Compute the product of the elements in list

    >>> prod([])
    1
    >>> prod([0])
    0
    >>> prod([1,2])
    2
    >>> prod([1.0,2.0])
    2.0
    """
    p = 1
    for l in list: p*=l
    return p

def totmass(atoms):
    """\
    Compute the total mass of a molecule in [(atno,(x,y,z))] format.

    The total mass of HBr:
    >>> totmass([(1,(0,0,0)),(35,(1.42,0,0))])
    80.904799999999994
    
    The total mass of OH
    >>> totmass([(8,(0.0000,0.0000,0.1077)),(1,(0.0000,0.0000,-0.8618))])
    16.9998
    """
    return sum([mass[atno] for atno,xyz in atoms])

def inertia(atoms):
    """\
    moi = inertia(atoms)

    Compute the moment of inertia for a groups of atoms where
    atoms    List of (atno,(x,y,z)) for each atom

    Units are amu * A^2

    Compute the moment of inertia of HBr. This matches the value from
    the Laidler textbook.
    >>> inertia([(1,(0,0,0)),(35,(1.42,0,0))])
    array([ 0.        ,  1.99305011,  1.99305011])

    Compute the moment of inertia of OH. This matches the value from
    Truong's TheRate program (although he uses au's for distance).
    >>> inertia([(8,(0.0000,0.0000,0.1077)),(1,(0.0000,0.0000,-0.8618))])
    array([ 0.        ,  0.88530303,  0.88530303])

    >>> inertia([(8,(0,0,0)),(1,(0,0,1)),(1,(0,1,0))])
    array([ 0.88951475,  1.0008    ,  1.89031475])
    """
    I = zeros((3,3),'d')
    xyzcom = com(atoms)
    moi = 0
    for atno,xyz in atoms:
        m = mass[atno]
        xyz = array(xyz,'d')
        xyz -= xyzcom
        x,y,z = xyz
        I[0,0] += m*(y*y+z*z)
        I[1,1] += m*(x*x+z*z)
        I[2,2] += m*(y*y+x*x)
        I[0,1] -= m*x*y
        I[1,0] = I[0,1]
        I[0,2] -= m*x*z
        I[2,0] = I[0,2]
        I[1,2] -= m*y*z
        I[2,1] = I[1,2]
    moments = eigvalsh(I)
    #print "Moments of Inertia (amu*A2) ",moments
    #print "Moments of Inertia (au) ",moments/0.52918**2
    #print "Rotational constants (cm-1) ",16.85763042/moments
    return moments

def rate_bi(A_atoms,A_vibes,A_rotsym,A_emult,
         B_atoms,B_vibes,B_rotsym,B_emult,
         AB_atoms,AB_vibes,AB_rotsym,AB_emult,
         T=300):
    """\
    k = rate_bi()
    Compute the rate of the A+B = AB* -> Prod reaction

    Input atoms, vibrational frequencies, rotational symmetry numbers
    and electronic degeneracy (multiplicity) for each state A, B, AB*

    The factor of 10^6 is to convert from m^3/(mol s) to cm^3/(mol s),
    which is what GRI reports parameters in.

    Example: Rate of H + HBr = H2 + Br example from Laidler
    (my parameters differ slightly)
    >>> h = [(1,(0,0,0))]
    >>> vh = []
    >>> hbr = [(1,(0,0,0)),(35,(1.42,0,0))]
    >>> vhbr = [2650]
    >>> hhbr = [(1,(0,0,0)),(1,(1.50,0,0)),(35,(2.92,0,0))]
    >>> vhhbr = [460.,460.,2340.]
    >>> rate_bi(h,vh,1,2,hbr,vhbr,1,1,hhbr,vhhbr,1,2,300)
    2.53252370816e+13
    """
    qtot_A = qtot(A_atoms,A_vibes,T,A_rotsym,A_emult)
    qtot_B = qtot(B_atoms,B_vibes,T,B_rotsym,B_emult)
    qtot_AB = qtot(AB_atoms,AB_vibes,T,AB_rotsym,AB_emult)
    qratio = qtot_AB/(qtot_A*qtot_B)
    return 62.5e11*NA*qratio*1e6

def rate_uni(A_atoms,A_vibes,A_rotsym,A_emult,
             As_atoms,As_vibes,As_rotsym,As_emult,
             T=300):
    """\
    k = rate_uni()
    Compute the rate of the A = A* -> Prod reaction

    Input atoms, vibrational frequencies, rotational symmetry numbers
    and electronic degeneracy (multiplicity) for each state A, A*

    """
    qtot_A = qtot(A_atoms,A_vibes,T,A_rotsym,A_emult)
    qtot_As = qtot(As_atoms,As_vibes,T,As_rotsym,As_emult)
    qratio = qtot_As/qtot_A
    return 62.5e11*qratio

def test_therate():
    oh = [(8,(0.0000,0.0000,0.1077)),(1,(0.0000,0.0000,-0.8618))]
    voh = [3821]
    qtr = qtrans(totmass(oh))
    qr = qrot(oh)
    qv = qvibes(voh)
    qr = qrot(oh)
    qv = qvibes(voh)
    qt = qtot(oh,voh,1,2)
    print "OH"
    print "trans ",qtr,log(qtr)
    print "rot   ",qr,log(qr)
    print "vibe  ",qv,log(qv)
    print "tot   ",qt,log(qt)

    c2h6 = [
        (6,    (-0.7594,    0.0000,    0.0000)),
        (6,    ( 0.7594,    0.0000,    0.0000)),
        (1,    (-1.1593,   -1.0014,   -0.1876)),
        (1,    (-1.1593,    0.3382,    0.9610)),
        (1,    (-1.1593,    0.6632,   -0.7734)),
        (1,    ( 1.1593,    1.0014,    0.1876)),
        (1,    ( 1.1593,   -0.6632,    0.7734)),
        (1,    ( 1.1593,   -0.3382,   -0.9610))]
    vc2h6 =  [326,   846,   846,  1050,  1252,  1252,  1437,
              1468,  1527,  1527,  1530,  1530, 
              3117,  3122,  3178,  3179,  3203,  3203  ]
    qtr = qtrans(totmass(c2h6))
    qr = qrot(c2h6)
    qv = qvibes(vc2h6)
    qt = qtot(c2h6,vc2h6,1,1)
    print "C2H6"
    print "trans ",qtr,log(qtr)
    print "rot   ",qr,log(qr)
    print "vibe  ",qv,log(qv)
    print "tot   ",qt,log(qt)

    c2h6oh = [
        (6,    ( 0.0000,    0.0000,    0.0000)),
        (6,    ( 0.0000,    0.0000,    1.5050)),
        (1,    ( 1.0252,    0.0000,   -0.3901)),
        (1,    (-0.5054,   -0.8837,   -0.3993)),
        (1,    (-0.5061,    0.8837,   -0.3975)),
        (1,    (-1.1786,    0.0219,    1.8861)),
        (1,    ( 0.4362,   -0.8931,    1.9577)),
        (1,    ( 0.4140,    0.9024,    1.9602)),
        (8,    (-2.3911,   -0.1765,    2.1877)),
        (1,    (-2.3378,   -1.1299,    2.3229))
        ]
    vc2h6oh = [56,   126,   185,   420,   651,   826,   858,   959,
               1059,  1167,  1261,  1299, 1441,  1481,  1501,  1513,
               1520,  3111,  3159,  3183,  3204,  3238,  3881]

    qtr = qtrans(totmass(c2h6oh))
    qr = qrot(c2h6oh)
    qv = qvibes(vc2h6oh)
    qt = qtot(c2h6oh,vc2h6oh,1,2)
    print "C2H6-OH"
    print "trans ",qtr,log(qtr)
    print "rot   ",qr,log(qr)
    print "vibe  ",qv,log(qv)
    print "tot   ",qt,log(qt)

    print "Rate: %10.4e" % rate_bi(oh,voh,1,2,c2h6,vc2h6,1,1,
                                c2h6oh,vc2h6oh,1,2,300)

def jagout_scanner(fname):
    """\
    Scan a Jaguar output file and get the relevant information for kinetics calculations,
    including:
    - geometry
    - frequencies
    - rotational symmetry number
    - spin multiplicity
    - total energy
    - zero point energy
    """
    from Pistol.Jaguar import read_output_as_dict
    props = read_output_as_dict(fname)
    geo = props.get('structure')
    if not geo:
        raise Exception("Structure not obtained from Jaguar file")
    freqs = props.get('freqs',[])
    rotsym = props.get('rotsym',1)
    emult = props.get('multiplicity',1)
    energy = props.get('energy')
    zpe = props.get('zpe',0)
    #print "Properties obtained from Jaguar output"
    #print "structure"
    #for atno,(x,y,z) in geo:
    #    print "%d   %10.4f %10.4f %10.4f" % (atno,x,y,z)
    #print "multiplicity = ",emult
    #print "frequencies = ",freqs
    #print "zpe = ",zpe
    #print "rotsym = ",rotsym
    #print "energy = ",energy
    return geo,freqs,rotsym,emult,energy,zpe

def posfreqs(freqs,dotest=True,**kwargs):
    """\
    Returns the positive frequencies only. Optionally also tests
    whether there is exactly one negative frequency.
    """
    freq_cutoff = kwargs.get('freq_cutoff',0)
    if dotest:
        nf = [freq for freq in freqs if freq < freq_cutoff]
        assert len(nf) == 1
    return [freq for freq in freqs if freq > freq_cutoff]

def fileroot(fname):
    import os.path
    head,tail = os.path.split(fname)
    root,ext = os.path.splitext(tail)
    return root

def jaguar_kinetics_bi(Aout,Bout,ABout,**kwargs):
    A,A_freqs,A_rotsym,A_mult,A_energy,A_zpe = jagout_scanner(Aout)
    Aname = fileroot(Aout)
    B,B_freqs,B_rotsym,B_mult,B_energy,B_zpe = jagout_scanner(Bout)
    Bname = fileroot(Bout)
    AB,AB_freqs,AB_rotsym,AB_mult,AB_energy,AB_zpe = jagout_scanner(ABout)
    ABname = fileroot(ABout)
    AB_pfreqs = posfreqs(AB_freqs,**kwargs)
    print "Rate for %s + %s = %s" % (Aname,Bname,ABname)
    dE = 627.51*(AB_energy-A_energy-B_energy)
    dZPE = AB_zpe-A_zpe-B_zpe
    print "Inherent barrier (kcal/mol) = ",dE,dZPE
    print "T(K)  k(cm^3/mol-s)"
    for T in range(300,2001,100):
        k = rate_bi(A,A_freqs,A_rotsym,A_mult,
                 B,B_freqs,B_rotsym,B_mult,
                 AB,AB_pfreqs,AB_rotsym,AB_mult,T)
        print "%5d %10.4e" % (T,k)

def jaguar_kinetics_uni(Aout,Asout,**kwargs):
    A,A_freqs,A_rotsym,A_mult,A_energy,A_zpe = jagout_scanner(Aout)
    Aname = fileroot(Aout)
    As,As_freqs,As_rotsym,As_mult,As_energy,As_zpe = jagout_scanner(Asout)
    Asname = fileroot(Asout)
    As_pfreqs = posfreqs(As_freqs,**kwargs)
    print "Rate for %s => %s" % (Aname,Asname)
    dE = 627.51*(As_energy-A_energy)
    dZPE = As_zpe-A_zpe
    print "Inherent barrier (kcal/mol) = ",dE,dZPE
    print "T(K)  k(/s)"
    for T in range(300,2001,100):
        k = rate_uni(A,A_freqs,A_rotsym,A_mult,
                     As,As_pfreqs,As_rotsym,As_mult,T)
        print "%5d %10.4e" % (T,k)
    return

def test2():
    oh = [(8,(0.0000,0.0000,0.1077)),(1,(0.0000,0.0000,-0.8618))]
    c2h6oh = [
        (6,    ( 0.0000,    0.0000,    0.0000)),
        (6,    ( 0.0000,    0.0000,    1.5050)),
        (1,    ( 1.0252,    0.0000,   -0.3901)),
        (1,    (-0.5054,   -0.8837,   -0.3993)),
        (1,    (-0.5061,    0.8837,   -0.3975)),
        (1,    (-1.1786,    0.0219,    1.8861)),
        (1,    ( 0.4362,   -0.8931,    1.9577)),
        (1,    ( 0.4140,    0.9024,    1.9602)),
        (8,    (-2.3911,   -0.1765,    2.1877)),
        (1,    (-2.3378,   -1.1299,    2.3229))
        ]

    c2h4 =[
        (6,  (-0.0000000154,      0.0000000098,  -0.0152424944 )),
        (6,  (-0.0000000547,     -0.0000000155,   1.3152424900 )),
        (1,  ( 0.9238695505,     -0.0000004712,  -0.5874149610 )),
        (1,  (-0.9238690969,      0.0000004982,  -0.5874159171 )),
        (1,  ( 0.9238694305,      0.0000005048,   1.8874149243 )),
        (1,  (-0.9238690499,     -0.0000004645,   1.8874160067 ))]

    print inertia(oh)
    print inertia(c2h6)
    print inertia(c2h6oh)
    print inertia(c2h4)

def doctests():
    import doctest
    doctest.testmod()
    
def main():
    doctests() # Always run the doctests
    #test_therate()
    #test_hbr()
    jaguar_kinetics_bi("/home/rmuller/Desktop/oh.out",
                       "/home/rmuller/Desktop/h2.out",
                       "/home/rmuller/Desktop/h2-oh.out")

if __name__ == '__main__':
    main()
