#!/usr/bin/python
"""\
NAME
   MOLF.py: Utilities for reading and writing molden molf format files.

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

import sys,re,string

def read_molf(filename):
    """\
    Reads a molf file and outputs the geometry (geo), the basis (bas),
    and the wave function (wfn).
    
    The geo is given as a list of atoms. Each atom is a tuple of the
    symbol, the atomic number, and the x,y,z coordinates in angstroms.
    
    The bas is given as a list of contracted basis functions. Each
    contracted basis function is a tuple of the bfn symbol (S, P, D, ...),
    the number of the atom on which the basis function lives, and a
    list of the primitive basis functions. The primitive basis functions
    are given as a tuple of the exponent and the contraction coefficient.
    
    The wfn is given as a list of orbitals. Each orbital is a tuple of
    the symmetry, if any, the energy in hartrees, the spin (probably unused
    for now), the occupation, and a list of the major elements. The
    major elements are given as a tuple of the basis function number
    and the coefficient.
    """
    molf_data = {}
    geosect,bassect,wfnsect = get_molf_sects(filename)
    molf_data['geometry'] = parse_geosect(geosect)
    molf_data['basis'] = parse_bassect(bassect)
    molf_data['wfn'] = parse_wfnsect(wfnsect)
    
    return molf_data

def write(filename,atoms,freqs=None,modes=None,basis=None,orbs=None):
    from Pistol.Element import symbol
    file = open(filename,'w')
    file.write("[Molden Format]\n")
    file.write("[Atoms] Angs\n")
    iat = 1
    for atno,(x,y,z) in atoms:
        file.write("%s %5.0f %5.0f %10.4f %10.4f %10.4f\n" % (symbol[atno],iat,atno,x,y,z))
        iat += 1
    if basis: raise "Molden basis output not implemented yet"
    if orbs: raise "Molden orbital output not implemented yet"
    if freqs:
        file.write("[FREQ]\n")
        for freq in freqs: file.write("%20.8f\n" % freq)
        
        file.write("[FR-COORD] Angs\n")
        for atno,(x,y,z) in atoms:
            file.write("%s %10.4f %10.4f %10.4f\n" % (symbol[atno],toBohr1(x),toBohr1(y),
                                                      toBohr1(z)))

        file.write("[FR-NORM-COORD]\n")
        for i in range(len(modes)):
            file.write('vibration %d\n' % (i+1))
            for mx,my,mz in modes[i]:
                file.write("%10.4f %10.4f %10.4f\n" % (mx,my,mz))
    file.close()
    return        

def toBohr1(x):
    return x/0.52918

def toBohr3(x,y,z):
    return toBohr1(x),toBohr1(y),toBohr1(z)

def vtk_render_molf(filename):
    from VTK import Scene,vtk_grid_data3
    from Element import color,radius
    from Numeric import zeros,Float
    molf_data = read_molf(filename)
    orbs = molf_data['wfn']
    atoms = molf_data['geometry']
    norbs = len(orbs)
    bfs = pyquante_basis(molf_data['basis'],atoms)
    nx=ny=nz = 50
    origin,dens,grid = make_bounding_grid(atoms,nx,ny,nz)
    data = zeros((nx,ny,nz),Float)
    while 1:
        print "Orbitals: "
        for i in range(norbs):
            print i+1,orbs[i][1],orbs[i][3]
        item = raw_input("Which orbital (0 to exit? ")
        iitem = int(item)
        if iitem == 0: break
        iitem = iitem - 1
        scene = Scene()
        for sym,atno,x,y,z in atoms:
            r,g,b = color[atno]
            scene.add_sphere(0.3*radius[atno],(x,y,z),(r/255.,g/255.,b/255.))
        nat = len(atoms)
        for i in range(nat):
            symi,atnoi,xi,yi,zi = atoms[i]
            for j in range(i):
                symj,atnoj,xj,yj,zj = atoms[j]
                rij2 = dist2((xi,yi,zi),(xj,yj,zj))
                rij20 = 0.25*pow(radius[atnoi]+radius[atnoj],2)
                if rij2 < rij20:
                    scene.add_cylinder((xi,yi,zi),(xj,yj,zj),(0.25,0.25,0.25))
        orb = orbs[iitem][4]
        for i,j,k,x,y,z in grid:
            x,y,z = toBohr3(x,y,z)
            data[i,j,k] = 0.
            for ibf,coef in orb:
                data[i,j,k] += coef*bfs[ibf-1].amp(x,y,z)
        vtkdata = vtk_grid_data3((nx,ny,nz),data)
        scene.add_grid_data(origin,(nx,ny,nz),dens,vtkdata)
        scene.add_contour(0.1,(0.9,0.9,0),0.9)
        scene.add_contour(-0.1,(0,0.9,0.9),0.9)
        scene.display()
    return

def make_bounding_grid(atoms,nx=20,ny=20,nz=20):
    xmin,xmax,ymin,ymax,zmin,zmax = get_bbox(atoms)
    dx = xmax-xmin
    dy = ymax-ymin
    dz = zmax-zmin
    points = []
    for i in range(nx):
        x = xmin+i*dx/float(nx)
        for j in range(ny):
            y = ymin+j*dy/float(ny)
            for k in range(nz):
                z = zmin+k*dz/float(nz)
                points.append((i,j,k,x,y,z))
    return (xmin,ymin,zmin),(dx/(nx-1.),dy/(ny-1.),dz/(nz-1.)),points

def get_bbox(atoms):
    BIG = 10000
    BOUNDARY = 4
    xmin = BIG
    ymin = BIG
    zmin = BIG
    xmax = -BIG
    ymax = -BIG
    zmax = -BIG
    for sym,atno,x,y,z in atoms:
        xmin = min(xmin,x)
        xmax = max(xmax,x)
        ymin = min(ymin,y)
        ymax = max(ymax,y)
        zmin = min(zmin,z)
        zmax = max(zmax,z)
    xmin -= BOUNDARY
    ymin -= BOUNDARY
    zmin -= BOUNDARY
    xmax += BOUNDARY
    ymax += BOUNDARY
    zmax += BOUNDARY
    return xmin,xmax,ymin,ymax,zmin,zmax
    

def pyquante_basis(molfbasis,atoms):
    from PyQuante.Ints import sym2powerlist
    from PyQuante.CGBF import CGBF
    
    bfs = []
    for type,atomnum,primlist in molfbasis:
        for power in sym2powerlist[type]:
            symi,atnoi,xi,yi,zi = atoms[atomnum-1]
            x,y,z = toBohr3(xi,yi,zi)
            bf = CGBF((x,y,z),power)
            for expnt,coef in primlist:
                bf.add_primitive(expnt,coef)
            bf.normalize()
            bfs.append(bf)
    return bfs

def get_molf_sects(filename):
    geo_pat = re.compile('\[Atoms\]')
    bas_pat = re.compile('\[GTO\]')
    wfn_pat = re.compile('\[MO\]')
    other_pat = re.compile('\[')
    file = open(filename,'r')

    ingeo = 0
    inbas = 0
    inwfn = 0

    geosect = []
    bassect = []
    wfnsect = []

    for line in file.readlines():
        if geo_pat.search(line):
            geosect.append(line)
            ingeo = 1
            inbas = 0
            inwfn = 0
        elif bas_pat.search(line):
            bassect.append(line)
            ingeo = 0
            inbas = 1
            inwfn = 0
        elif wfn_pat.search(line):
            wfnsect.append(line)
            ingeo = 0
            inbas = 0
            inwfn = 1
        elif other_pat.search(line):
            ingeo = 0
            inbas = 0
            inwfn = 0
        elif ingeo:
            geosect.append(line)
        elif inbas:
            bassect.append(line)
        elif inwfn:
            wfnsect.append(line)
    # end for file in file.readlines()
    file.close()
    return geosect,bassect,wfnsect

def parse_geosect(geosect):
    geo = []
    words = string.split(geosect[0])
    units = "Angs"
    if len(words) > 1:
        units = words[1] 
    for line in geosect[1:]:
        words = string.split(line)
        sym = words[0]
        atno = int(words[2])
        x,y,z = float(words[3]),float(words[4]),float(words[5])
        if units == "Bohr": x,y,z = bohr2angstrom(x,y,z)
        geo.append((sym,atno,x,y,z))
    return geo

def bohr2angstrom(x,y,z):
    factor = 0.52918
    return x*factor,y*factor,z*factor

def parse_bassect(bassect):
    # This is more confusing than it should be
    bas = []
    iptr = 1
    # Get all atoms
    while 1:
        iptr,line = nextline(iptr,bassect)
        if not line: break

        words = string.split(line)
        if len(words) < 1: continue

        atom_number = int(words[0])

        # Get all contracted bfs on atom
        while 1:
            iptr,line = nextline(iptr,bassect)
            if not line: break
        
            words = string.split(line)
            if len(words) < 1: break
        
            sym = words[0]
            nprim = int(words[1])

            primlist = []
        
            for i in range(nprim):
                iptr,line = nextline(iptr,bassect)
                if not line: break

                words = string.split(line)
                if len(words) < 1: break
                exp,coef = float(words[0]),float(words[1])
                primlist.append((exp,coef))
            bf = (sym,atom_number,primlist)
            bas.append(bf)
    return bas

def nextline(iptr,section):
    if iptr < len(section):
        return iptr+1,section[iptr]
    return iptr,None

def parse_wfnsect(wfnsect):
    sym_pat = re.compile('Sym')
    ene_pat = re.compile('Ene')
    spin_pat = re.compile('Spin')
    occup_pat = re.compile('Occup')
    wfn = []
    sym=en=spin=occ=None
    coefs = []
    for line in wfnsect[1:]:
        if sym_pat.search(line):
            sym = parse_equals_line(line)
            if occ:
                wfn.append((sym,en,spin,occ,coefs))
                coefs = []
        elif ene_pat.search(line):
            en = parse_equals_line(line,"f")
        elif spin_pat.search(line):
            spin = parse_equals_line(line)
        elif occup_pat.search(line):
            occ = parse_equals_line(line,"f")
        else:
            num,coef = parse_orbcoef_line(line)
            coefs.append((num,coef))
    return wfn

def parse_equals_line(line,type="s"):
    "Uses same types as sprintf, printf, PyArgs_ParseTuple, etc."
    line = string.strip(line)
    words = string.split(line,'=')
    if type == 'd' or type == 'i': return int(words[1])
    if type == 'f': return float(words[1])
    return words[1]

def parse_orbcoef_line(line):
    words = string.split(line)
    return int(words[0]),float(words[1])

def dist2((x1,y1,z1),(x2,y2,z2)):
    return pow(x1-x2,2)+pow(y1-y2,2)+pow(z1-z2,2)

if __name__ == '__main__':
    if len(sys.argv) < 2: print __doc__; sys.exit()
    filename = sys.argv[1]
    #read_molf(filename)
    vtk_render_molf(filename)
