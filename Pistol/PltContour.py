#!/usr/bin/env python

"""\
NAME
  plot_orbplt.py - Take Jaguar orbital amplitudes and plots in 3D

SYNOPSIS
  plot_orbplt.py <output filename> <plt filename>

DESCRIPTION
  The Jaguar eldens module outputs orbital amplitudes computed on a
  rectangular grid. This program plots that information in 3D. 

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

import sys,re,string
from Pistol.Jaguar import read_output_as_dict,read_plt
from Pistol.POVRay import Scene,Cylinder,Sphere,TriangleMesh
from Pistol.Element import radius,color
from Pistol.Constants import bohr2ang
from Pistol.MarchingCubes import contour

rscale = 0.25

def dist2((a,b,c),(d,e,f)): return (a-d)**2 + (b-e)**2 + (c-f)**2

def get_bonds_from_distance(atoms):
    bonds = []
    distcut2 = 1.6*1.6 # Only define this once
    for i in range(len(atoms)):
        atnoi,xyzi = atoms[i]
        for j in range(i):
            atnoj,xyzj = atoms[j]
            distcut2 = radius[atnoi]*radius[atnoj]
            if dist2(xyzi,xyzj) < distcut2: bonds.append((i,j))
    return bonds

def main(outname,pltname):
    mol_info = read_output_as_dict(outname)
    plt_info = read_plt(pltname)
    name = mol_info['name']
    scene = Scene(name)
    #scene.set_camera((0,4,0.5),(0,0,0.5))
    scene.set_camera((0,10,0))
    atoms = mol_info['structure']
    for i,j in get_bonds_from_distance(atoms):
        atnoi,xyzi = atoms[i]
        atnoj,xyzj = atoms[j]
        scene.add(Cylinder(xyzi,xyzj,0.1))
    for atno,xyz in atoms:
        r,g,b  = color[atno]
        sphere = Sphere(xyz,rscale*radius[atno],(r/255.,g/255.,b/255.))
        scene.add(sphere)

    ptris = mcube_contour(plt_info,0.1)
    ntris = mcube_contour(plt_info,-0.1)

    # if desired, compute normals at each vertex
    ptris = smooth_tris(ptris)
    ntris = smooth_tris(ntris)
    if ptris: scene.add(TriangleMesh(ptris,(1,0,0)))
    if ntris: scene.add(TriangleMesh(ntris,(0,0,1)))
    
    scene.write_pov()
    scene.render()
    scene.display()
    return

def mcube_contour(plt_info,value):
    origin = plt_info['origin']
    nx,ny,nz = plt_info['npts']
    xvec = plt_info['xvec']
    yvec = plt_info['yvec']
    zvec = plt_info['zvec']
    grid = plt_info['grid']

    tris = []
    for k in range(nz-1):
        for j in range(ny-1):
            for i in range(nx-1):
                cube_tris = contour(
                    value,
                    ijk2xyz((i,j,k),(nx,ny,nz),origin,xvec,yvec,zvec),
                    ijk2xyz((i+1,j,k),(nx,ny,nz),origin,xvec,yvec,zvec),
                    ijk2xyz((i+1,j+1,k),(nx,ny,nz),origin,xvec,yvec,zvec),
                    ijk2xyz((i,j+1,k),(nx,ny,nz),origin,xvec,yvec,zvec),
                    ijk2xyz((i,j,k+1),(nx,ny,nz),origin,xvec,yvec,zvec),
                    ijk2xyz((i+1,j,k+1),(nx,ny,nz),origin,xvec,yvec,zvec),
                    ijk2xyz((i+1,j+1,k+1),(nx,ny,nz),origin,xvec,yvec,zvec),
                    ijk2xyz((i,j+1,k+1),(nx,ny,nz),origin,xvec,yvec,zvec),
                    grid[i,j,k],grid[i+1,j,k],
                    grid[i+1,j+1,k],grid[i,j+1,k],
                    grid[i,j,k+1],grid[i+1,j,k+1],
                    grid[i+1,j+1,k+1],grid[i,j+1,k+1])
                for tri in cube_tris: tris.append(tri)
    return tris

def ijk2xyz((i,j,k),(nx,ny,nz),(x0,y0,z0),(xx,xy,xz),(yx,yy,yz),(zx,zy,zz)):
    zfrac = k/float(nz-1)
    yfrac = j/float(ny-1)
    xfrac = i/float(nx-1)
    x = bohr2ang*(x0 + xfrac*xx+yfrac*yx+zfrac*zx)
    y = bohr2ang*(y0 + xfrac*xy+yfrac*yy+zfrac*zy)
    z = bohr2ang*(z0 + xfrac*xz+yfrac*yz+zfrac*zz)
    return x,y,z

def smooth_tris(tris):
    "Compute normals at each vertex from a list of triangles"
    from TupleMath import minus,cross,normalize
    norms = {}
    for pt0,pt1,pt2 in tris:
        n = normalize(cross(minus(pt1,pt0),minus(pt2,pt0)))
        # This is a bad idea, since I'm keying a dictionary on floats!
        addappend(norms,fixkey(pt0),n)
        addappend(norms,fixkey(pt1),n)
        addappend(norms,fixkey(pt2),n)
    newtris = []
    for pt0,pt1,pt2 in tris:
        newtris.append((pt0,average(norms[fixkey(pt0)]),
                        pt1,average(norms[fixkey(pt1)]),
                        pt2,average(norms[fixkey(pt2)])))
    return newtris

def fixkey(key):
    "map key to an int for safer hash indexing"
    f=1e6
    return int(f*key[0]),int(f*key[1]),int(f*key[2])

def addappend(dict,key,value):
    if dict.has_key(key):
        dict[key].append(value)
    else:
        dict[key] = [value]
    return

def average(l):
    from TupleMath import normalize,plus
    avg = (0.,0.,0.)
    for xyz in l: avg = plus(avg,xyz)
    return normalize(avg)
    
if __name__ == '__main__':
    #test_mcubes()
    if len(sys.argv) != 3:
        print __doc__
        sys.exit()
    main(sys.argv[1],sys.argv[2])

