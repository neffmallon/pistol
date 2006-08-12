#!/usr/bin/env python
"""\
NAME
    CMM.py - Implementation of the cell multipole method

NOTES
    This module has functions to compute total charge, dipole, quadrupole
    and octapole moments. It appears, though, that the octapole moments
    fall off so quickly (1/r^4) that they are better off excluded.

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

from time import time
from math import sqrt,pow
from Numeric import zeros,Float,array,dot
from Multipoles import distance,l2,full_potential,fit_charge,fit_dipole,\
     fit_quadrupole, fit_octapole, charge_potential, dipole_potential,\
     quadrupole_potential, octapole_potential

class CMM:
    "Goddard's Cell Multipole Method"
    def __init__(self,nbins,points=[],cutoff=30.):
        self.nx,self.ny,self.nz = nbins
        self.bins = []
        self.cutoff = cutoff
        if points:
            self.add_points(points)
        else:
            self.points = []
        return

    def pot(self,xyz):
        vxyz = 0
        for bin in self.bins:
            xyzb = bin.center()
            rbin = distance(xyz,xyzb)
            if rbin < self.cutoff:
                vxyz += bin.full_potential(xyz)
            else:
                vxyz += bin.mp_potential(xyz)
        return vxyz

    def __call__(self,xyz): return self.pot(xyz)

    def add_points(self,points):
        self.points = points
        self.set_bbox()
        self.setup_bins()
        self.distribute_points()
        self.pack_bins()
        return

    def pack_bins(self):
        for bin in self.bins: bin.pack()
        return

    def set_bbox(self):
        BIG = 10000
        D = 1e-8
        xmax = ymax = zmax = -BIG
        xmin = ymin = zmin = BIG
        for qi,(xi,yi,zi) in self.points:
            xmax = max(xi,xmax)
            ymax = max(yi,ymax)
            zmax = max(zi,zmax)
            xmin = min(xi,xmin)
            ymin = min(yi,ymin)
            zmin = min(zi,zmin)
        self.xmin = xmin-D
        self.xmax = xmax+D
        self.ymin = ymin-D
        self.ymax = ymax+D
        self.zmin = zmin-D
        self.zmax = zmax+D
        self.dx = self.xmax-self.xmin
        self.dy = self.ymax-self.ymin
        self.dz = self.zmax-self.zmin
        return

    def bin_index(self,xyz):
        i = int(self.nx*(xyz[0]-self.xmin)/self.dx)
        j = int(self.ny*(xyz[1]-self.ymin)/self.dy)
        k = int(self.nz*(xyz[2]-self.zmin)/self.dz)
        return k+j*self.nz+i*self.nz*self.ny
        
    def setup_bins(self):
        for i in range(self.nx):
            xminbin = self.xmin + i*self.dx/self.nx
            xmaxbin = self.xmin + (i+1)*self.dx/self.nx
            for j in range(self.ny):
                yminbin = self.ymin + j*self.dy/self.ny
                ymaxbin = self.ymin + (j+1)*self.dy/self.ny
                for k in range(self.nz):
                    zminbin = self.zmin + k*self.dz/self.nz
                    zmaxbin = self.zmin + (k+1)*self.dz/self.nz
                    bin = Bin((xminbin,xmaxbin,yminbin,
                               ymaxbin,zminbin,zmaxbin))
                    self.bins.append(bin)
        return

    def distribute_points(self):
        for point in self.points:
            index = self.bin_index(point[1])
            self.bins[index].add_point(point)
        return
    
class Bin:
    def __init__(self,bbox):
        self._xmin = bbox[0]
        self._xmax = bbox[1]
        self._ymin = bbox[2]
        self._ymax = bbox[3]
        self._zmin = bbox[4]
        self._zmax = bbox[5]
        self._points = []
        self._center = array((0.5*(self._xmax+self._xmin),
                              0.5*(self._ymax+self._ymin),
                              0.5*(self._zmax+self._zmin)))
        self.do_oct = 0 # include octapole moments
        return

    def pack(self):
        self._q = fit_charge(self._points)
        self._dip = fit_dipole(self._center,self._points)
        self._quad = fit_quadrupole(self._center,self._points)
        if self.do_oct: self._oct = fit_octapole(self._center,self._points)
        return

    def points(self): return self._points
    def charge(self): return self._q
    def dipole(self): return self._dip
    def quadrupole(self): return self._quad
    def center(self): return self._center
    def add_point(self,point): self._points.append(point)
    def full_potential(self,xyz): return full_potential(xyz,self._points)

    def mp_potential(self,xyz):
        v = charge_potential(xyz,self._q,self._center) +\
            dipole_potential(xyz,self._dip,self._center) +\
            quadrupole_potential(xyz,self._quad, self._center)
        if self.do_oct: v+= octapole_potential(xyz,self._oct,self._center)
        return v


def avg(a): return sum(a)/float(len(a))

def test_cmm(n = 10000, cutoff = 50, a = 100, nbin = 10, ntrials = 100):
    "Tests multipole approximations to electrostatic potential"

    bindims = (nbin,nbin,nbin)
    bbox = (-a,a,-a,a,-a,a)
    print " n = %d, a = %d, cut = %d, nbin = %d" % (n,a,cutoff,nbin)
    tfull = []
    tbin = []
    tvbin = []
    rms = 0
    
    for i in range(ntrials):
        points = RandomQs(n,bbox)  # Create a random set of charges
        xyz = RandomPosition(bbox) # Select a random position

        t0 = time()
        vfull = full_potential(xyz,points)
        t1 = time()

        tfull.append(t1-t0)

        cmm = CMM(bindims,points)
        t2 = time()
        tbin.append(t2-t1)

        vbin = cmm.pot(xyz)
        t3 = time()
        tvbin.append(t3-t2)
        rms += pow(vfull-vbin,2)
        print "Trial %d: %10.4f %10.4f" % (i,vfull,vbin)
    print "Average times: %10.4f %10.4f %10.4f" %\
          (avg(tfull),avg(tbin),avg(tvbin))
    print "RMS error: ",sqrt(rms/ntrials)
    return

def RandomQs(n,bbox):
    "Build a test system of n particles with -1<q<1 within a bounding box."
    from random import random
    points = []
    for i in range(n):
        xyz = RandomPosition(bbox)
        q = 2*random()-1.
        points.append((q,xyz))
    return points

def RandomPosition(bbox):
    "Select a random position inside the bounding box"
    from random import random
    xmin,xmax,ymin,ymax,zmin,zmax = bbox
    dx,dy,dz = xmax-xmin,ymax-ymin,zmax-zmin
    x = dx*random()+xmin
    y = dy*random()+ymin
    z = dz*random()+zmin
    return array((x,y,z))


if __name__ == '__main__': test_cmm()

# Results:
#  n = 1000, a = 100, cut = 100, nbin = 5, ntrials = 100
#                   RMS error
#  q only           0.0086
#  q + dipoles      0.0013
#  q + dip + quad   0.0002
#  q + d + q + o    0.0002 (may not help at this point)
#  

# Change the cutoff to 50:
# q + dip + quad    0.002
# qdqo              0.002


# Move up to 10 bins in each direction, keep cutoff at 50:
# qdq       0.00026, 0.0008, 0.001

