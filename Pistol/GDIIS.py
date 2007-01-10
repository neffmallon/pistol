#!/usr/bin/env python
"""\
 Implementation of Pulay's GDIIS geometry optimizer. Can be used to
 optimize both unit cells and geometries.

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""
from numpy import dot, ravel,zeros,Float,transpose,sum,array,reshape
from numpy.oldnumeric.linear_algebra import solve_linear_equations
from math import sqrt

# This is the averager that D.D. Johnson attributes to Anderson.
# PRB 38, 12807 (1988).

class SD:
    def __init__(self,step=0.1):
        self.step = step
        self.energy_old = None
        self.less = 0.5
        self.more = 1.2

    def newgeo(self,atoms,F,energy):
        if self.energy_old:
            if energy < self.energy_old: self.step *= self.more
            else: self.step *= self.less
        geo = []
        a = self.step
        for i in range(len(atoms)):
            atno,(x,y,z) = atoms[i]
            fx,fy,fz = F[i]
            geo.append((atno,(x+a*fx,y+a*fy,z+a*fz)))
        self.energy_old = energy
        return geo                
        
class AndersonAverager:
    def __init__(self,alpha=0.5):
        self.alpha = alpha
        self.atoms_old = None
        self.F_old = None
        return

    def newgeo(self,atoms,F):
        if self.atoms_old:
            beta = self.get_beta(atoms,F)
            print "beta = ",beta
            geo = self.and_update(atoms,F,beta)
        else:
            geo = self.simple_update(atoms,F)
            
        self.atoms_old = atoms
        self.F_old = F
        return geo

    def simple_update(self,atoms,F):
        newatoms = []
        a = self.alpha
        for i in range(len(atoms)):
            atno,(x,y,z) = atoms[i]
            fx,fy,fz = F[i]
            newatoms.append((atno,(x+a*fx,y+a*fy,z+a*fz)))
        return newatoms

    def get_beta(self,atoms,F):
        f_fm = 0   
        fm_fm = 0  
        for i in range(len(atoms)):
            fx,fy,fz = F[i]
            fxo,fyo,fzo = self.F_old[i]
            f_fm += fx*(fx-fxo) + fy*(fy-fyo) + fz*(fz-fzo)
            fm_fm += (fx-fxo)*(fx-fxo) + (fy-fyo)*(fy-fyo) + (fz-fzo)*(fz-fzo)
        return f_fm/fm_fm

    def and_update(self,atoms,F,b):
        newgeo = []
        a = self.alpha
        for i in range(len(atoms)):
            fx,fy,fz = F[i]
            fxo,fyo,fzo = self.F_old[i]
            atno,(xo,yo,zo) = self.atoms_old[i]
            atno,(x,y,z) = atoms[i]
            
            xnew = x*(1-b) + xo*b + a*(1-b)*fx + a*b*fxo
            ynew = y*(1-b) + yo*b + a*(1-b)*fy + a*b*fyo
            znew = z*(1-b) + zo*b + a*(1-b)*fz + a*b*fzo
            newgeo.append((atno,(xnew,ynew,znew)))
        return newgeo
    
class GDIIS:
    def __init__(self,errcut=0.1,sdstep=0.1):
        self.errcut = errcut
        self.sdstep = sdstep
        self.errors = []
        self.geos = []
        self.started = 0
        return

    def newgeo(self,geo,forces):
        err = -ravel(array(forces))
        maxerr = max(abs(err))
        print "Maxerror = ",maxerr
        if maxerr < self.errcut and not self.started:
            self.started = 1
            print "GDIIS started"

        newgeo = []
        nat = len(geo)
        nit = len(self.errors)
        if self.started:
            self.errors.append(err)
            self.geos.append(geo)

        if self.started and nit > 1:
            #print "Nit = ",nit
            a = zeros((nit+1,nit+1),Float)
            b = zeros(nit+1,Float)
            for i in range(nit):
                for j in range(nit):
                    a[i,j] = dot(self.errors[i],
                                 self.errors[j])
            for i in range(nit):
                a[nit,i] = a[i,nit] = -1.
            b[nit] = -1.
            c = solve_linear_equations(a,b)
            newf = zeros(len(self.errors[0]),Float)
            for i in range(nit): newf += c[i]*self.errors[i]
            newf = reshape(newf,(nat,3))
            for i in range(nat):
                atno = 0
                x = y = z = 0
                fx = fy = fz = 0
                for j in range(nit):
                    atno,(xj,yj,zj) = self.geos[j][i]
                    x += c[j]*xj
                    y += c[j]*yj
                    z += c[j]*zj
                newgeo.append((atno,(x,y,z)))
            for i in range(nat):
                atno,(xi,yi,zi) = newgeo[i]
                fxi,fyi,fzi = newf[i]
                newgeo[i] = atno,(xi-fxi,yi-fyi,zi-fzi)
        else:
            for i in range(nat):
                atno,(x,y,z) = geo[i]
                fx,fy,fz = forces[i]
                x += self.sdstep*fx
                y += self.sdstep*fy
                z += self.sdstep*fz
                newgeo.append((atno,(x,y,z)))
        return newgeo

def dist_angle(xyz1,xyz2,xyz3):
    from math import acos,pi
    r1 = array(xyz1)
    r2 = array(xyz2)
    r3 = array(xyz3)
    dr12 = r1-r2
    dr13 = r1-r3
    r12 = sqrt(dot(dr12,dr12))
    r13 = sqrt(dot(dr13,dr13))
    a123 = acos(dot(dr12,dr13)/r12/r13)*180/pi
    return r12,r13,a123

def sq_test():
    """Use Seqquest to test the GDIIS optimization"""
    from SeqQuest import get_energy_forces
    from Constants import Ang2Bohr

    #optimizer = GDIIS(1,0.05)
    optimizer = SD(0.1)

    h2o = [(8,(0,0,0)),(1,(1.,0,0)),(1,(0,1,0))]
    # Convert Angstroms to bohr
    for i in range(len(h2o)):
        atno,(x,y,z) = h2o[i]
        h2o[i] = atno,(Ang2Bohr(x),Ang2Bohr(y),Ang2Bohr(z))

    gconv = 0.004
    for i in range(50):
        energy,forces = get_energy_forces('quest.in',h2o,
                                          [[20,0,0],[0,20,0],[0,0,20]],
                                          0,(40,40,40))
        err = max(abs(ravel(forces)))
        if err < gconv:
            print "Geometry converged to ",gconv," Ry/bohr"
            break
        print "G iteration ",i+1,err
        for i in range(len(h2o)):
            atno,(x,y,z) = h2o[i]
            fx,fy,fz = forces[i]
            print "%2d %10.4f %10.4f %10.4f %10.4f %10.4f %10.4f " %\
                  (atno,x,y,z,fx,fy,fz)
        r12,r13,a123 = dist_angle(h2o[0][1],h2o[1][1],h2o[2][1])
        print r12,r13,a123
        h2o = optimizer.newgeo(h2o,forces,energy)
    return                                          
    
def mindo_test():
    """Test the geometry optimization using MINDO forces"""
    from PyQuante.Molecule import Molecule
    from PyQuante.MINDO3 import get_energy_forces
    h2o = Molecule('H2O',atomlist=[(8,(0,0,0)),(1,(1.,0,0)),(1,(0,1.,0))])
    optimizer = GDIIS(60,0.0001)

    for i in range(25):
        energy,forces = get_energy_forces(h2o)
        forces *= -1
        for i in range(len(h2o)):
            atno,(x,y,z) = h2o[i].atuple()
            fx,fy,fz = forces[i]
            print "%2d %10.4f %10.4f %10.4f %10.4f %10.4f %10.4f " %\
                  (atno,x,y,z,fx,fy,fz)
        newgeo = optimizer.newgeo(h2o.atuples(),forces)
        h2o.update_from_atuples(newgeo)
    #end for
if __name__ == '__main__':
    sq_test()

# Results:
# This structure takes 9 steps in SQ to converge using Broyden to
#  max(F) < 0.04 Ry/bohr;Here's the 0.04 geo:
#  1            1            0.0935753031    0.0935774464    0.0001572386
#  2            2            1.9083838032   -0.0074900156   -0.0003071949
#  3            2           -0.0074912203    1.9083902682   -0.0003096187
#  r12 = r13 = 1.8176
#  a123 = 96.4 deg
#  took 29 steps to converge < 0.004 Ry/bohr: 1.817,1.817,112.23 deg. 
#
# GDIIS takes 6 iterations to converge to the same limit, and
#  gets roughly the same geometry. It has  a very hard time getting much
#  below this. It also doesn't appear stable when trying to go too much lower.
#
# Anderson took 13 steps to converge to 0.04: 1.858, 106.939
#  (this may actually be a more accurate geometry -- the PES seems convoluted).
#          took 17 to converge to 0.004: 1.832, 101.05
#
# Steepest Descent took 12 steps to 0.04: 1.848/96.22
#     took 23 steps to 0.004: 1.828/101.998
