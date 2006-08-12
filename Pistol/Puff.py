#!/usr/bin/env python
"""\
 Puff.py - A python universal force field implementation
"""

from math import pi,sin,cos,acos,sqrt
from Numeric import array,dot,zeros,Float
from XYZ import read
#from UFF import Data, DefaultTypes
#from Dreiding import Data, DefaultTypes

class Atom:
    def __init__(self,atno,x,y,z,type=None):
        self.atno = atno
        self.r = array((x,y,z))
        self.type = type

    def mass(self): return mass[self.atno]
    def pos(self): return self.r.tuple()
    def atuple(self): return (self.atno,self.r)
    def translate(self,pos): self.r += pos

    def distance(self,other):
        rij = self.r-other.r
        return sqrt(dot(rij,rij))

    def __str__(self):
        a,(x,y,z) = self.atuple()
        return '(%2d, (%4.2f, %4.2f, %4.2f))' % (a,x,y,z)

class HarmonicBond:
    name = 'HarmonicBond'
    coord = 2
    def __init__(self,R0=1.0,k=700.0,n=1):
        self.R0 = R0  # Equilibrium bond distance
        self.k = n*k  # Hooke's law force constant
        return

    def energy(self,atoms): # compute E/F together to save ops
        xyzi = atoms[0].r
        xyzj = atoms[1].r
        dij = xyzi-xyzj
        rij = sqrt(dot(dij,dij))
        dR = rij-self.R0
        E = 0.5*self.k*dR*dR
        dE = self.k*dR
        F = dE*dij/rij
        self.F = F
        return E
    
    def force(self,atoms):
        return [array(self.F),-array(self.F)]

class HarmonicCosineAngle: # Harmonic cosine form
    name = 'HarmonicCosineAngle'
    coord = 3
    def __init__(self,theta0=109.5, k=70.0):
        self.theta0 = theta0
        self.costheta0 = cos(theta0)
        self.k = k
        if self.theta0 < 179:
            self.is_linear = 0
            sinth = sin(self.theta0)
            self.c = self.k/sinth**2
        else:
            self.is_linear = 1
        return

    def energy(self,atoms):
        xyzi = atoms[0].r
        xyzj = atoms[1].r
        xyzk = atoms[2].r
        dij = xyzi-xyzj
        rij = sqrt(dot(dij,dij))
        djk = xyzj-xyzk
        rjk = sqrt(dot(djk,djk))
        dotijk = dot(dij,djk)
        costheta = dotijk/rij/rjk
        dcosti = djk/rij/rjk - dij*dotijk/pow(rij,3)/rjk
        dcostk = dij/rij/rjk - djk*dotijk/pow(rjk,3)/rij
        dcostj = -dcosti-dcostk

        if self.is_linear:
            E = self.k*(1 + costheta)
            dE = self.k
        else:
            dcth = costheta - self.costheta0
            E = 0.5*self.c*dcth*dcth
            dE = self.c*dcth
        F = dE*dcosti,dE*dcostj,dE*dcostk
        self.F = F
        return E

    def force(self,atoms):
        return [array(self.F),-array(self.F)]

class HarmonicAngle: # Normal Harmonic
    name = 'HarmonicAngle'
    coord = 3
    def __init__(self,theta0=109.5, k=70.0):
        self.theta0 = theta0
        self.k = k
        return

    def energy(self,atoms):
        xyzi = atoms[0].r
        xyzj = atoms[1].r
        xyzk = atoms[2].r
        dij = xyzi-xyzj
        rij = sqrt(dot(dij,dij))
        djk = xyzj-xyzk
        rjk = sqrt(dot(djk,djk))
        dotijk = dot(dij,djk)
        costheta = dotijk/rij/rjk
        sintheta = sqrt(1-costheta*costheta)
        theta = acos(costheta)
        dcosti = djk/rij/rjk - dij*dotijk/pow(rij,3)/rjk
        dcostk = dij/rij/rjk - djk*dotijk/pow(rjk,3)/rij
        dcostj = -dcosti-dcostk
        dthetai = -dcosti/sintheta
        dthetaj = -dcostj/sintheta
        dthetak = -dcostk/sintheta

        dtheta = theta-self.theta0
        E = 0.5*self.k*dtheta*dtheta
        dE = self.k*dtheta
        F = dE*dthetai,dE*dthetaj,dE*dthetak
        self.F = F
        return E

    def force(self,atoms):
        return self.F

class Torsion:
    name = 'Torsion'
    coord = 4
    def __init__(self,phi0=180.0,k=1.,n=1):
        self.phi0 = phi0
        self.k = k
        self.n = n
        self.small = 0.1 # Cutoff for small angles
        return

    def energy(self,atoms):
        xyzi = atoms[0].r
        xyzj = atoms[1].r
        xyzk = atoms[2].r
        xyzl = atoms[3].r
        rij = xyzi-xyzj
        Rij = sqrt(dot(rij,rij))
        rjk = xyzj-xyzk
        Rjk = sqrt(dot(rjk,rjk))
        rkl = xyzk-xyzl
        Rkl = sqrt(dot(rkl,rkl))

        A = cross(rij,rjk)
        Alen = sqrt(dot(A,A))
        B = cross(rjk,rkl)
        Blen = sqrt(dot(B,B))

        phi = acos(dot(A,B)/Alen/Blen)
        sinphi = sin(phi)
        cosphi = cos(phi)

        if self.n > 0:
            K = self.n*self.k*sin(self.n*phi+self.phi0)
            E = self.k*(1+cos(self.n*phi+self.phi0))
        else:
            K = -2*self.k*(phi-self.phi0)
            E = self.k*(phi-self.phi0)**2

        if sinphi > self.small:
            # normal terms
            Fix = K/sinphi/Alen*(rjk[1]*(B[2]/Blen-cosphi*A[2]/Alen)-
                                 rjk[2]*(B[1]/Blen-cosphi*A[1]/Alen))
            Fiy = K/sinphi/Alen*(rjk[2]*(B[0]/Blen-cosphi*A[0]/Alen)-
                                 rjk[0]*(B[2]/Blen-cosphi*A[2]/Alen))
            Fiz = K/sinphi/Alen*(rjk[0]*(B[1]/Blen-cosphi*A[1]/Alen)-
                                 rjk[1]*(B[0]/Blen-cosphi*A[0]/Alen))

            Flx = K/sinphi/Blen*(rjk[2]*(B[1]/Blen-cosphi*A[1]/Alen)-
                                 rjk[1]*(B[2]/Blen-cosphi*A[2]/Alen))
            Fly = K/sinphi/Blen*(rjk[0]*(B[2]/Blen-cosphi*A[2]/Alen)-
                                 rjk[2]*(B[0]/Blen-cosphi*A[0]/Alen))
            Flz = K/sinphi/Blen*(rjk[1]*(B[0]/Blen-cosphi*A[0]/Alen)-
                                 rjk[0]*(B[1]/Blen-cosphi*A[1]/Alen))

            Fjx = K/sinphi*(1/Alen*(rij[2]*(B[1]/Blen-cosphi*A[1]/Alen)-
                                    rij[1]*(B[2]/Blen-cosphi*A[2]/Alen))+
                            1/Blen*(rkl[1]*(A[2]/Alen-cosphi*B[2]/Blen)-
                                    rjk[2]*(A[1]/Alen-cosphi*B[1]/Blen))) \
                  - Fix
            Fjy = K/sinphi*(1/Alen*(rij[0]*(B[2]/Blen-cosphi*A[2]/Alen)-
                                    rij[2]*(B[0]/Blen-cosphi*A[0]/Alen))+
                            1/Blen*(rkl[2]*(A[0]/Alen-cosphi*B[0]/Blen)-
                                    rjk[0]*(A[2]/Alen-cosphi*B[2]/Blen))) \
                  - Fiy
            Fjz = K/sinphi*(1/Alen*(rij[1]*(B[0]/Blen-cosphi*A[0]/Alen)-
                                    rij[0]*(B[1]/Blen-cosphi*A[1]/Alen))+
                            1/Blen*(rkl[0]*(A[1]/Alen-cosphi*B[1]/Blen)-
                                    rjk[1]*(A[0]/Alen-cosphi*B[0]/Blen))) \
                  - Fiz

            Fkx = -Flx - \
                  K/sinphi*(1/Alen*(rij[2]*(B[1]/Blen-cosphi*A[1]/Alen)-
                                    rij[1]*(B[2]/Blen-cosphi*A[2]/Alen))+
                            1/Blen*(rkl[1]*(A[2]/Alen-cosphi*B[2]/Blen)-
                                    rjk[2]*(A[1]/Alen-cosphi*B[1]/Blen)))
            Fky = -Fly - \
                  K/sinphi*(1/Alen*(rij[0]*(B[2]/Blen-cosphi*A[2]/Alen)-
                                    rij[2]*(B[0]/Blen-cosphi*A[0]/Alen))+
                            1/Blen*(rkl[2]*(A[0]/Alen-cosphi*B[0]/Blen)-
                                    rjk[0]*(A[2]/Alen-cosphi*B[2]/Blen)))
            Fkz = -Flz - \
                  K/sinphi*(1/Alen*(rij[1]*(B[0]/Blen-cosphi*A[0]/Alen)-
                                    rij[0]*(B[1]/Blen-cosphi*A[1]/Alen))+
                            1/Blen*(rkl[0]*(A[1]/Alen-cosphi*B[1]/Blen)-
                                    rjk[1]*(A[0]/Alen-cosphi*B[0]/Blen)))
        else:
            # small angle terms
            C = cross(rjk,A)
            Clen = sqrt(dot(C,C))
            Fix = K/cosphi/Clen*((rjk[1]**2+rjk[2]**2)*
                                 (B[0]/Blen-sinphi*C[0]/Clen) -
                                 rjk[0]*rjk[1]*(B[1]/Blen-sinphi*C[1]/Clen) -
                                 rjk[0]*rjk[2]*(B[2]/Blen-sinphi*C[2]/Clen))
            Fiy = K/cosphi/Clen*((rjk[2]**2+rjk[0]**2)*
                                 (B[1]/Blen-sinphi*C[1]/Clen) -
                                 rjk[1]*rjk[2]*(B[2]/Blen-sinphi*C[1]/Clen) -
                                 rjk[1]*rjk[0]*(B[0]/Blen-sinphi*C[0]/Clen))
            Fiz = K/cosphi/Clen*((rjk[0]**2+rjk[1]**2)*
                                 (B[2]/Blen-sinphi*C[2]/Clen) -
                                 rjk[2]*rjk[0]*(B[0]/Blen-sinphi*C[0]/Clen) -
                                 rjk[2]*rjk[1]*(B[1]/Blen-sinphi*C[1]/Clen))

            Flx = -K/cosphi/Blen*(rjk[2]*(C[1]/Clen-sinphi*B[1]/Blen)-
                                  rjk[1]*(C[2]/Clen-sinphi*B[2]/Blen))
            Fly = -K/cosphi/Blen*(rjk[0]*(C[2]/Clen-sinphi*B[2]/Blen)-
                                  rjk[2]*(C[0]/Clen-sinphi*B[0]/Blen))
            Flz = -K/cosphi/Blen*(rjk[1]*(C[0]/Clen-sinphi*B[0]/Blen)-
                                  rjk[0]*(C[1]/Clen-sinphi*B[1]/Blen))

            Fjx = K/cosphi*(1/Clen*(
                -(rjk[1]*rij[2]+rjk[2]*rij[2])*(B[1]/Blen-sinphi*C[0]/Clen)
                +(2*rjk[0]*rij[1]-rjk[1]*rij[0])*(B[0]/Blen-sinphi*C[1]/Clen)
                +(2*rjk[0]*rij[2]-rjk[2]*rij[0])*(B[2]/Blen-sinphi*B[2]/Clen))
                            +1/Blen*(
                rkl[1]*(C[2]/Clen-sinphi*B[2]/Blen)
                -rkl[2]*(C[0]/Clen-sinphi*B[0]/Blen))) - Fix
            Fjy = K/cosphi*(1/Clen*(
                -(rjk[1]*rij[2]+rjk[0]*rij[2])*(B[1]/Blen-sinphi*C[1]/Clen)
                +(2*rjk[1]*rij[2]-rjk[2]-rij[1])*(B[2]/Blen-sinphi*C[2]/Clen)
                +(2*rjk[1]*rij[0]-rjk[0]*rij[1])*(B[0]/Blen-sinphi*C[0]/Clen))
                            +1/Blen*(
                rkl[2]*(C[0]/Clen-sinphi*B[0]/Blen)
                -rkl[0]*(C[2]/Clen-sinphi*B[2]/Blen))) - Fiy
            Fjz = K/cosphi*(1/Clen*(
                -(rjk[1]*rij[2]+rjk[2]*rij[2])*(B[0]/Blen-sinphi*C[0]/Clen)
                +(2*rjk[0]*rij[2]-rjk[2]*rij[0])*(B[2]/Blen-sinphi*C[2]/Clen))
                            +1/Blen*(
                rkl[2]*(C[1]/Clen-sinphi*B[1]/Blen)
                -rkl[1]*(C[0]/Clen-sinphi*B[0]/Blen))) - Fiz

            Fkx = -K/cosphi*(1/Clen*(
                -(rjk[1]*rij[2]+rjk[2]*rij[2])*(B[0]/Blen-sinphi*C[0]/Clen)
                +(2*rjk[0]*rij[1]-rjk[1]*rij[0])*(B[1]/Blen-sinphi*C[1]/Clen)
                +(2*rjk[0]*rij[2]-rjk[2]*rij[0])*(B[2]/Blen-sinphi*C[2]/Clen))
                             +1/Blen*(
                rkl[1]*(C[2]/Clen-sinphi*B[2]/Blen)
                -rkl[2]*(C[0]/Clen-sinphi*B[0]/Blen))) - Flx
            Fky = -K/cosphi*(1/Clen*(
                -(rjk[1]*rij[2]+rjk[0]*rij[2])*(B[1]/Blen-sinphi*C[1]/Clen)
                +(2*rjk[1]*rij[2]-rjk[2]*rij[1])*(B[2]/Blen-sinphi*C[2]/Clen)
                +(2*rjk[1]*rij[0]-rjk[0]*rij[1])*(B[0]/Blen-sinphi*C[0]/Clen))
                             +1/Blen*(
                rkl[2]*(C[0]/Clen-sinphi*B[0]/Blen)
                -rkl[0]*(C[2]/Clen-sinphi*B[2]/Blen))) - Fly
            Fkz = -K/cosphi*(1/Clen*(
                -(rjk[0]*rij[0]+rjk[1]*rij[1])*(B[2]/Blen-sinphi*C[2]/Clen)
                +(2*rjk[2]*rij[0]-rjk[0]*rij[1])*(B[0]/Blen-sinphi*C[0]/Clen)
                +(2*rjk[2]*rij[1]-rjk[1]*rij[2])*(B[1]/Blen-sinphi*C[1]/Clen))
                             +1/Blen*(
                rkl[2]*(C[1]/Clen-sinphi*B[1]/Blen)
                -rkl[1]*(C[0]/Clen-sinphi*B[0]/Blen))) - Flz

        F = (array((Fix,Fiy,Fiz)),
             array((Fjx,Fjy,Fjz)),
             array((Fkx,Fky,Fkz)),
             array((Flx,Fly,Flz)))
        self.F = F
        return E

    def force(self,atoms):
        return self.F

class X6VDW: # Buckingham exp-6
    name = 'X6VDW'
    coord = 2
    def __init__(self,R0=2.0,D0=4.0,scale=12):
        self.R0 = R0
        self.D0 = D0
        self.scale = scale
        self.ecoef = self.D0*6/(self.scale-6)
        self.rcoef = self.D0*self.scale/(self.scale-6)
        return

    def energy(self,atoms):
        xyzi = atoms[0].r
        xyzj = atoms[0].r
        dij = xyzi-xyzj
        rij = sqrt(dot(dij,dij))
        rho = rij/self.R0
        E = self.ecoef*exp(self.scale*(1-rho)) - self.rcoef*pow(rho,-6)
        dE = -self.ecoef*exp(self.scale*(1-rho))*self.scale \
             + 6*self.rcoef*pow(rho,-7)
        drho = dij/rij/self.R0
        F = dE*drho
        self.F = F
        return E

    def force(self,atoms):
        return self.F

FFConstructors = [HarmonicBond,HarmonicCosineAngle,
                  HarmonicAngle,Torsion,X6VDW]

class EnergyExpression:
    def __init__(self,atoms):
        self.FFTypes = {}
        for func in FFConstructors:
            self.FFTypes[func.name] = func
        self.FFTypes['Bond'] = HarmonicBond
        self.FFTypes['Angle'] = HarmonicCosineAngle
        self.terms = []
        self.indices = []
        self.nat = len(atoms)
        return

    def energy(self,atoms):
        E = 0
        for term,indices in zip(self.terms,self.indices):
            termatoms = [atoms[i] for i in indices]
            E += term.energy(atoms)
        return E

    def force(self,atoms):
        F = zeros((self.nat,3))
        for term,indices in zip(self.terms,self.indices):
            termatoms = [atoms[i] for i in indices]
            forces = term.force(termatoms)
            print term.name
            print forces
            for i in range(len(indices)):
                for j in range(3):
                    print i,indices[i],j
                    F[indices[i],j] += forces[i][j]
        return F

    def add_term(self,type,indices):
        assert type in self.FFTypes
        assert len(indices) == self.FFTypes[type].coord
        # do something here to set defaults based on element types
        self.terms.append(self.FFTypes[type]())
        self.indices.append(indices)
        return
        
def cross(a,b): return array((a[1]*b[2]-a[2]*b[1],
                              a[2]*b[0]-a[0]*b[2],
                              a[0]*b[1]-a[1]*b[0]))

def gen_bondpartners(atoms):
    bondpartners = []
    for atom in atoms: bondpartners.append([])

    for i in range(len(atoms)):
        atomi = atoms[i]

        ri0 = atomi.R0

        for j in range(i):
            atomj = atoms[j]
            rj0 = atomj.R0
            
            rij = atomi.distance(atomj)

            if rij < 1.2*(ri0+rj0):
                bondpartners[i].append(j)
                bondpartners[j].append(i)
    return bondpartners

def gen_bondlist(bondpartners):
    nat = len(bondpartners)
    bondlist = []
    for i in range(nat):
        for j in bondpartners[i]:
            if j < i: continue
            bondlist.append((i,j))
    return bondlist

def gen_anglelist(bondpartners):
    nat = len(bondpartners)
    anglelist = []

    for i in range(nat):

        npart = len(bondpartners[i])
        if npart < 2: continue
        for index1 in range(npart):
            for index2 in range(index1):
                anglelist.append((i,bondpartners[i][index1],
                                  bondpartners[i][index2]))
    return anglelist

def gen_torsionlist(bondpartners):
    nat = len(bondpartners)
    torsionlist = []

    for j in range(nat):
        for k in bondpartners[j]:
            if k < j: continue

            # We now have a unique bond pair j,k
            for i in bondpartners[j]:
                if i == k: continue
                for l in bondpartners[k]:
                    if l == j: continue
                    torsionlist.append((i,j,k,l))
    return torsionlist

def gen_inversionlist(bondpartners):
    nat = len(bondpartners)
    inversionlist = []

    for i in range(nat):
        if len(bondpartners[i]) == 3:
            # Test for excluded atom types
            inversionlist.append((i,bondpartners[i][0],
                                  bondpartners[i][1], bondpartners[i][2]))
    return inversionlist

def gen_nblist(atoms,bondpartners):
    nat = len(atoms)
    nblist = []

    for i in range(nat):
        for j in range(i):
            rij = atoms[i].distance(atoms[j])
            if rij > 9: continue
            if j in bondpartners[i]: continue
            is13 = 0
            for k in bondpartners[i]:
                if j in bondpartners[k]: is13 = 1
            if is13: continue
            nblist.append((i,j))
    return nblist

def test_big(filename):
    print "Testing UFF machinery for %s" % filename
    xyzs = read(filename)[-1] # Default to last geo
    atoms = []
    for atno,(x,y,z) in xyzs: atoms.append(Atom(atno,x,y,z))
    bondpartners = gen_bondpartners(atoms)
    print " bondpartners"
    for bp in bondpartners: print bp

    bonds = gen_bondlist(bondpartners)
    print " # bonds = ", len(bonds)
    for a,b in bonds: print a,b

    angles = gen_anglelist(bondpartners)
    print " # angles = ",len(angles) 
    for a,b,c in angles: print a,b,c

    tors = gen_torsionlist(bondpartners)
    print " # torsions = ", len(tors)
    for a,b,c,d in tors: print a,b,c,d

    invs = gen_inversionlist(bondpartners)
    print " # inversions = ", len(invs)
    for a,b,c,d in invs: print a,b,c,d

    nbs = gen_nblist(atoms,bondpartners)
    print " # nonbonds = ", len(nbs)
    for a,b in nbs: print a,b

def test_bond():
    import biggles
    atom1 = Atom(1,0.,0.,0.)
    atom2 = Atom(1,1.,0.,0.)
    bond = HarmonicBond(atom1,atom2,1.0)
    Es = []
    Rs = [0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5]
    for R in Rs:
        atom2.r = array((R,0.,0.))
        E,F = bond.EF()
        Es.append(E)
        print R,E,F
    p = biggles.FramedPlot()
    p.add(biggles.Curve(Rs,Es))
    p.title = 'Energy of HarmonicBond'
    p.xlabel = 'x'
    p.ylabel='Energy'
    p.show()
    return

def test_angle():
    import biggles
    atomi = Atom(1,0.,0.,0.)
    atomj = Atom(8,1.,0.,0.)
    atomk = Atom(8,0.,1.,0.)
    
    angle = HarmonicAngle(atomi,atomj,atomk,120.0*pi/180.)
    angle2 = HarmonicCosineAngle(atomi,atomj,atomk,120.0*pi/180.)
    as = range(10,180)
    Es = []
    E2s = []
    for a in as:
        th = a*pi/180.
        x = cos(th)
        y = sin(th)
        atomk.r = array((x,y,0))
        E,F = angle.EF()
        E2,F2 = angle2.EF()
        Es.append(E)
        E2s.append(E2)
    p = biggles.FramedPlot()
    p.title = "Harmonic (blue) vs HarmonicCosine (red) terms"
    p.xlabel = "Angle (degrees)"
    p.ylabel = "E (kcal/mol)"
    p.add(biggles.Curve(as,Es,color='blue'))
    p.add(biggles.Curve(as,E2s,color='red'))
    #p.write_img(400,300,"angle.png")
    p.show()
    return

def test_torsion():
    import biggles
    atomi = Atom(1,0.,1.,0.)
    atomj = Atom(8,0.,0.,0.)
    atomk = Atom(8,1.,0.,0.)
    atoml = Atom(1,1.,1.,0.)
    tors = Torsion(atomi,atomj,atomk,atoml,pi,100,6)

    Es = []
    Fs = []
    angs = []
    for phi in range(180):
        y = cos(phi*pi/180.)
        z = sin(phi*pi/180.)
        atoml.r = array((1.,y,z))

        E,F = tors.EF()
        Ftot = 0
        for fxyz in F:
            Ftot += sqrt(dot(fxyz,fxyz))
        angs.append(phi)
        Es.append(E)
        Fs.append(Ftot/10)
    p = biggles.FramedPlot()
    p.title = "Torsional Energy (Red) and Force (Blue)"
    p.xlabel = "Angle (degrees)"
    p.add(biggles.Curve(angs,Es,color='red'))
    p.add(biggles.Curve(angs,Fs,color='blue'))
    p.show()
    return

def test_min_h2o(**kwargs):
    MaxIters = kwargs.get('maxiters',1)
    
    atoms = [ Atom(8,0.,0.,0.),
              Atom(1,1.,0.,0.),
              Atom(1,0.,1.,0.)]

    ee = EnergyExpression(atoms)
    ee.add_term('Bond',[0,1])
    ee.add_term('Bond',[0,2])
    ee.add_term('Angle',[1,0,2])

    for i in range(MaxIters):
        E = ee.energy(atoms)
        print "Energy = ",E
        F = ee.force(atoms)
        print "Force = ",F
        return

if __name__ == '__main__':
    #test_bond()
    #test_angle()
    #test_torsion()
    test_min_h2o()
