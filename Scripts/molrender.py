#!/usr/bin/env python
"""\
NAME
      molrender.py - Render a molecule in different formats

SYNOPSIS
      molrender.py [options] file.xyz

DESCRIPTION
      Render a molecule using different engines. The program reads an input
      XMol xyz list of geometries and uses POV-Ray, the Python Imaging
      Library, or Scalable Vector graphics to draw the molecule.

      The following options are available:

      -h       Print this help message
      -f  #    Render only frame # (can pass in python list indices like -1)

      The camera is placed at (x,y,z), and its location is controlled by:

      -x  #    Put x-coordinate at # (default 0)
      -y  #    Put y-coordinate at # (default 10)
      -z  #    Put z-coordinate at # (default 0)

      The light is placed at (l,m,n), and its location is controlled by:

      -l  #    Put l-coordinate at # (default 50)
      -m  #    Put m-coordinate at # (default 50)
      -n  #    Put n-coordinate at # (default 50)

      Imaging/Rendering options:
      
      -I       Use Python Imaging Library to render PNG files directly
      -P       Use POV-Ray to render molecule (default)
      -S       Use Scalable Vector Graphics (SVG) to render molecule

EXTERNAL DEPENDENCIES
      This program captures all of the POV-Ray functionality in the
      associated POVRay.py module. See the notes in that module for
      more information.

      This program captures all of the SVG functionality in the
      associated SVG.py module. See the notes in that module for
      more information.

      The element-specific information is contained in the Element.py
      module.

      This program assumes that a previewing image display program is called
      by 'display' (using ImageMagick). Should this not be the case
      (i.e. should you want to use xv or some other program), redefine
      the 'display_prog' variable to point to the full path of the
      command.

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

import os
from math import sqrt,asin
from Pistol.Element import symbol,sym2no,radius,color
from Pistol import XYZ

try:
    # import fast dist2 function written in C from PyQuante, if possible
    from cints import dist2
except:
    # otherwise, use a slower Python version
    def dist2(xyz1,xyz2):
        return pow(xyz1[0]-xyz2[0],2)+pow(xyz1[1]-xyz2[1],2)\
               +pow(xyz1[2]-xyz2[2],2)

display_prog = 'display' # Command to execute to display images.

rscale=.25 # scale factor for the radii

class MolRender:
    def __init__(self):
        self.camera = (0,30,0)
        self.light = (30,30,30)
        self.root = 'molrend'
        self.renderer = "pov" # also png, svg
        self.rendwrite = self.write_pov
        self.update_bonds = 1 # update bonds for each frame
        self.iframe = 0 # number of frames to point to
        
    def set_camera(self,pos): self.camera = pos
    def set_light(self,pos): self.light = pos

    def set_renderer(self,type):
        self.renderer = type
        if type == 'pov':
            self.rendwrite = self.write_pov
        elif type == 'png':
            self.rendwrite = self.write_png
        elif type == 'svg':
            self.rendwrite = self.write_svg
        else:
            raise "Unknown rendering type: %s" % self.renderer
        return

    def read_xyz(self,filename):
        import os.path
        basename = os.path.basename(filename)
        self.root = os.path.splitext(basename)[0]
        self.frames = read_all_xyz(filename)
        self.bbox = get_bbox(self.frames[0])
        self.nframes = len(self.frames)
        return

    # Put other input formats here

    def write_pov(self,filename,atoms):
        from Pistol.POVRay import Scene,Sphere,Cylinder
        # recompute the name from the filename: this will
        #  have the _0001 on it, if applicable:
        basename = os.path.basename(filename)
        name = os.path.splitext(basename)[0]
        scene = Scene(name,self.camera,self.light,bgcolor=(1,1,1))
        for i,j in get_bonds_from_distance(atoms):
            atnoi,xyzi = atoms[i]
            atnoj,xyzj = atoms[j]
            scene.add(Cylinder(xyzi,xyzj,0.1))
        for atno,xyz in atoms:
            r,g,b  = color[atno]
            sphere = Sphere(xyz,rscale*radius[atno],(r/255.,g/255.,b/255.))
            scene.add(sphere)
        scene.write_pov(filename)
        scene.render()
        if self.nframes == 1: scene.display()
        return

    def write_svg(self,filename,atoms):
        from Pistol.SVG import Scene,Circle,Line
        # recompute the name from the filename: this will
        #  have the _0001 on it, if applicable:
        basename = os.path.basename(filename)
        name = os.path.splitext(basename)[0]

        atoms = rotate_2d(atoms,self.camera)
        if self.iframe == 0:
            # need to recompute bbox for rotated mol
            xmin,xmax,ymin,ymax,zmin,zmax = get_bbox(atoms)
            self.bbox = xmin,xmax,ymin,ymax,zmin,zmax
        else:
            xmin,xmax,ymin,ymax,zmin,zmax = self.bbox

        height,width = 800,800 # in pixels
        # readjust heigh and width based upon bbox.
        dx = xmax - xmin
        dy = ymax - ymin
        if dx > dy:
            height = height*dy/dx
        else:
            width = width*dy/dx

        scale = get_2d_scale(xmin,xmax,ymin,ymax,height,width)

        scene = Scene(name,height,width)
        
        for i,j in get_bonds_from_distance(atoms):
            atnoi,(xi,yi,zi) = atoms[i]
            atnoj,(xj,yj,zj) = atoms[j]
            Xi = int(scale*(xi-xmin))
            Yi = int(scale*(yi-ymin))
            Xj = int(scale*(xj-xmin))
            Yj = int(scale*(yj-ymin))
            scene.add(Line((Xi,Yi),(Xj,Yj)))
        
        for atno,(x,y,z) in atoms:
            X = int(scale*(x-xmin))
            Y = int(scale*(y-ymin))
            scene.add(Circle((X,Y),rscale*scale*radius[atno],color[atno]))
        scene.write_svg(filename)
        if self.nframes == 1: scene.display()
        return

    def write_png(self,filename,atoms):
        try:
            import Image,ImageDraw
        except:
            raise "You must install the Python Imaging Library"

        atoms = rotate_2d(atoms,self.camera)
        if self.iframe == 0:
            # need to recompute bbox for rotated mol
            xmin,xmax,ymin,ymax,zmin,zmax = get_bbox(atoms)
            self.bbox = xmin,xmax,ymin,ymax,zmin,zmax
        else:
            xmin,xmax,ymin,ymax,zmin,zmax = self.bbox

        
        height,width = 800,800 # in pixels
        # readjust heigh and width based upon bbox.
        dx = xmax - xmin
        dy = ymax - ymin
        if dx > dy:
            height = height*dy/dx
        else:
            width = width*dy/dx

        scale = get_2d_scale(xmin,xmax,ymin,ymax,height,width)

        img = Image.new("RGB",(width,height),(255,255,255))
        draw = ImageDraw.Draw(img)
        
        for i,j in get_bonds_from_distance(atoms):
            atnoi,(xi,yi,zi) = atoms[i]
            atnoj,(xj,yj,zj) = atoms[j]
            Xi = int(scale*(xi-xmin))
            Yi = int(scale*(yi-ymin))
            Xj = int(scale*(xj-xmin))
            Yj = int(scale*(yj-ymin))
            draw.line((Xi,Yi,Xj,Yj),fill=(0,0,0))

        for atno,(x,y,z) in atoms:
            X = int(scale*(x-xmin))
            Y = int(scale*(y-ymin))
            R = rscale*scale*radius[atno]
            RGB = color[atno]
            draw.ellipse((X-R,Y-R,X+R,Y+R),fill=RGB,outline=(0,0,0))
        img.save(filename,"PNG") 
        if self.nframes == 1: display(filename)
        return

    def render(self):
        atoms = self.frames[self.iframe]
        if self.nframes == 1:
            filename = self.root + "." + self.renderer
        else:
            filename = "%s%04d.%s" % (self.root,self.iframe,self.renderer)
        self.rendwrite(filename,atoms)
        return
    
    def renderonly(self,iframe):
        self.nframes = 1
        atoms = self.frames[iframe]
        filename = "%s.%s" % (self.root,self.renderer)
        self.rendwrite(filename,atoms)
        return
        
    def renderall(self):
        for i in range(self.nframes):
            self.iframe = i
            self.render()
        return

def rotate_2d(oldatoms,camera,oldcamera=(0,0,-1)):
    rotmat = get_rotmat(camera,oldcamera)
    atoms = []
    for atno,(x,y,z) in oldatoms:
        xyz = (rotmat[0][0]*x + rotmat[1][0]*y + rotmat[2][0]*z,
               rotmat[0][1]*x + rotmat[1][1]*y + rotmat[2][1]*z,
               rotmat[0][2]*x + rotmat[1][2]*y + rotmat[2][2]*z)
        atoms.append((atno,xyz))
    sort_by_z(atoms)
    return atoms

def cmp_z(a,b):
    "Function that compares the z values of 2 atoms"
    return cmp(a[1][2],b[1][2])

def sort_by_z(atoms):
    "Sort the atoms by their z values"
    atoms.sort(cmp_z)

def get_rotmat(newvec,oldvec):
    newvec = normalize(newvec)
    oldvec = normalize(oldvec)
    Ax,Ay,Az = cross(newvec,oldvec)
    C = dot(newvec,oldvec) # cos of angle
    S = sqrt(1-C*C)        # sin of angle
    return [[C+Ax*Ax*(1-C),Ax*Ay*(1-C)-Az*S,Ax*Az*(1-C)+Ay*S],
            [Ax*Ay*(1-C)+Az*S,C+Ay*Ay*(1-C),Ay*Az*(1-C)-Ax*S],
            [Ax*Az*(1-C)-Ay*S,Ay*Az*(1-C)+Ax*S,C+Az*Az*(1-C)]]

def normalize(vec):
    vx,vy,vz = vec
    len = sqrt(dot(vec,vec))
    return (vx/len,vy/len,vz/len)

def dot(vec1,vec2):
    return vec1[0]*vec2[0]+vec1[1]*vec2[1]+vec1[2]*vec2[2]

def cross(vec1,vec2):
    return (vec1[1]*vec2[2]-vec1[2]*vec2[1],
            vec1[2]*vec2[0]-vec1[0]*vec2[2],
            vec1[0]*vec2[1]-vec1[1]*vec2[0])
    
def get_2d_scale(xmin,xmax,ymin,ymax,height,width):
    dx = abs(xmax-xmin)
    dy = abs(ymax-ymin)
    if dy > dx:
        return height/dy
    return width/dx

def center(atoms):
    "Translate molecule to center"
    xc,yc,zc = [0,0,0]
    for atno,(x,y,z) in atoms:
        xc,yc,zc = xc+x,yc+y,zc+z
    nat = float(len(atoms))
    xc,yc,zc = xc/nat,yc/nat,zc/nat

    for i in range(len(atoms)):
        atno,(x,y,z) = atoms[i]
        atoms[i] = atno,(x-xc,y-yc,z-zc)
    return atoms

def get_bbox(atoms,boundary=2):
    BIG = 1000000
    xmin = BIG
    xmax = -BIG
    ymin = BIG
    ymax = -BIG
    zmin = BIG
    zmax = -BIG
    for atno,(x,y,z) in atoms:
        if x < xmin: xmin = x
        if x > xmax: xmax = x
        if y < ymin: ymin = y
        if y > ymax: ymax = y
        if z < zmin: zmin = z
        if z > zmax: zmax = z
    return xmin-boundary,xmax+boundary,ymin-boundary,ymax+boundary,\
           zmin-boundary,zmax+boundary

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

def display(filename): os.system("%s %s" % (display_prog,filename))

def read_all_xyz(filename):
    frames = XYZ.read(filename)
    for i in range(len(frames)):
        frames[i] = center(frames[i])
    return frames

# If we're running the code interactively (as opposed to importing it to
#  another program) execute this code at the start to drive everything.
if __name__ == '__main__':
    import sys,getopt
    if len(sys.argv) < 2:
        print __doc__
        sys.exit()

    # grab the command line options:
    opts,args = getopt.getopt(sys.argv[1:],'hIPSx:y:z:l:m:n:f:')
    
    # create a new object to render the molecule
    molrender = MolRender()
    lx,ly,lz = 50,50,50 # default light positions
    cx,cy,cz = 0,10,0   # default camera positions
    renderonly = None

    for key,value in opts:
        if key == '-h':
            print __doc__
            sys.exit()
        elif key == '-I': molrender.set_renderer('png') 
        elif key == '-S': molrender.set_renderer('svg')
        elif key == '-x': cx = float(value)
        elif key == '-y': cy = float(value)
        elif key == '-z': cz = float(value)
        elif key == '-l': lx = float(value)
        elif key == '-m': ly = float(value)
        elif key == '-n': lz = float(value)
        elif key == '-f': renderonly = int(value)

    molrender.read_xyz(args[0])
    molrender.set_camera((cx,cy,cz))
    molrender.set_light((lx,ly,lz))
    if renderonly != None:
        molrender.renderonly(renderonly)
    else:
        molrender.renderall()
