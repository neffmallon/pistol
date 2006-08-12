#!/usr/bin/env python

"""\
 An experimental pure Python/Tk viewer for molecules. I believe
 the similar feature in Hinsen's Scientific Python is better
 than this.

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

from Tkinter import *
from math import sqrt,pi,sin,cos

symbol =  ['X', 'H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O',
           'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl',
           'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe',
           'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br',
           'Kr', 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru',
           'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te',
           'I', 'Xe', 'Cs', 'Ba', 'La', None, None, None,
           None, None, None, None, None,None, None, None, None, None,
           'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os',
           'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi']

color =  ['#f19', '#fed', '#fcc', '#b22', '#282', '#0f0',
          '#789', '#0bf', '#f00', '#da2', '#f6b', '#00f',
          '#282', '#bbb', '#da2', '#fa0', '#ff0', '#0f0',
          '#fcc', '#f19', '#888', '#bbb', '#bbb', '#bbb',
          '#bbb', '#bbb', '#fa0', '#a22', '#a22', '#a22',
          '#a22', '#a22', '#562', '#ffe', '#9f9', '#a22',
          '#3c3', '#a22', '#bbb', '#bbb', '#bbb', '#bbb',
          '#f75', '#bbb', '#bbb', '#bbb', '#bbb', '#bbb',
          '#f80', '#bbb', '#bbb', '#bbb', '#bbb', '#a2f',
          '#f6b', '#a22', '#bbb', '#bbb',
          None, None, None, None, None, None, None, None,
          None, None, None, None, None,
          '#bbb', '#bbb', '#bbb', '#4ed', '#bbb', '#bbb',
          '#bbb', '#bbb', '#fd0', '#bbb', '#bbb', '#bbb', '#fbc']

radius = [1.0000,1.2000,1.4000,1.8200,1.3725,0.7950,1.7000,
          1.5500,1.5200,1.4700,1.5400,2.2700,1.7300,1.7000,
          2.1000,1.8000,1.8000,1.7500,1.8800,2.7500,2.4500,
          1.3700,1.3700,1.3700,1.3700,1.3700,1.4560,0.8800, 
          0.6900,0.7200,0.7400,1.3700,1.9500,1.8500,1.9000, 
          1.8500,2.0200,1.5800,2.1510,1.8010,1.6020,1.4680, 
          1.5260,1.3600,1.3390,1.3450,1.3760,1.2700,1.4240, 
          1.6630,2.1000,2.0500,2.0600,1.9800,2.0000,1.8400, 
          2.2430,1.8770,0.0000,0.0000,0.0000,0.0000,0.0000, 
          0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000, 
          0.0000,2.1700,1.5800,1.4670,1.5340,1.3750,1.3530, 
          1.3570,1.7500,1.6600,1.5500,1.9600,2.0200,2.1500] 

radscale = 0.3

sym2no = {}
for i in range(len(symbol)):
    if symbol[i]:
        sym2no[symbol[i]] = i
        sym2no[symbol[i].lower()] = i


class Viewer:
    def __init__(self,filename,height=400,width=400):
        self.root = Tk()
        self.height=height
        self.width=width
        self.canvas = Canvas(self.root,height=height,
                             width=width,background="White")
        self.canvas.pack()
        self.bind_keys()

        self.atoms = read_xyz(filename)
        self.nat = len(self.atoms)
        self.set_bbox()
        self.render()
        self.root.mainloop()
        return

    def bind_keys(self):
        # Key bindings
        self.root.bind("<Up>",self.rotate_plus_y)
        self.root.bind("<Down>",self.rotate_minus_y)
        self.root.bind("<Right>",self.rotate_plus_x)
        self.root.bind("<Left>",self.rotate_minus_x)

        self.root.bind("<Shift-Up>",self.pan_plus_y)
        self.root.bind("<Shift-Down>",self.pan_minus_y)
        self.root.bind("<Shift-Right>",self.pan_plus_x)
        self.root.bind("<Shift-Left>",self.pan_minus_x)

        self.root.bind("+",self.zoom_in)
        self.root.bind("-",self.zoom_out)

        self.root.bind("q",self.quit)
        return

    def quit(self,bs):
        self.canvas.postscript(file='bs.ps')
        self.root.quit()
        return

    def set_bbox(self):
        BIG = 1000000
        BOUNDARY = 2
        xmin = BIG
        xmax = -BIG
        ymin = BIG
        ymax = -BIG
        for atno,(x,y,z) in self.atoms:
            if x < xmin: xmin = x
            if x > xmax: xmax = x
            if y < ymin: ymin = y
            if y > ymax: ymax = y
        self.xmin = xmin-BOUNDARY
        self.xmax = xmax+BOUNDARY
        self.ymin = ymin-BOUNDARY
        self.ymax = ymax+BOUNDARY
        dx = abs(self.xmax-self.xmin)
        dy = abs(self.ymax-self.ymin)
        if dy > dx:
            self.scale = self.height/dy
        else:
            self.scale = self.width/dx
        self.cx,self.cy,self.cz = 0,0,0
        return
        
    def render(self):
        sort_by_z(self.atoms)
        bonds = get_bonds_from_distance(self.atoms)
        for i,j in bonds:
            atnoi,(xi,yi,zi) = self.atoms[i]
            atnoj,(xj,yj,zj) = self.atoms[j]
            Xi,Yi = self.convert(xi,yi)
            Xj,Yj = self.convert(xj,yj)
            self.canvas.create_line(Xi,Yi,Xj,Yj,width=3)

        for atno,(x,y,z) in self.atoms:
            X,Y = self.convert(x,y)
            R = self.scale*radscale*radius[atno]
            self.canvas.create_oval(X-R,Y-R,X+R,Y+R,fill=color[atno])
        return

    # The definitions here are a bit confusing, since they refer to
    #  the screen frame of reference
    def rotate_plus_y(self,bs): self.rotate(10,0,0)
    def rotate_minus_y(self,bs): self.rotate(-10,0,0)
    def rotate_plus_x(self,bs): self.rotate(0,-10,0)
    def rotate_minus_x(self,bs): self.rotate(0,10,0)
    def pan_plus_x(self,bs): self.pan(5,0,0)
    def pan_minus_x(self,bs): self.pan(-5,0,0)
    def pan_plus_y(self,bs): self.pan(0,-5,0)
    def pan_minus_y(self,bs): self.pan(0,5,0)
    def zoom_in(self,bs): self.zoom(1.1)
    def zoom_out(self,bs): self.zoom(0.9)

    def update(self):
        # Delete everything and redraw
        self.canvas.delete(ALL)
        self.render()

    def zoom(self,amt):
        self.scale *= amt
        self.update()
        return

    def pan(self,x,y,z):
        self.cx += x
        self.cy += y
        self.cz += z
        self.update()
        return

    def convert(self,x,y):
        return self.cx + int(self.scale*(x-self.xmin)),\
               self.cy + int(self.scale*(y-self.ymin))

    def rotate(self,ax,ay,az):
        ax,ay,az = ax*pi/180.,ay*pi/180.,az*pi/180.
        
        # rotate around x
        for i in range(self.nat):
            atno,(x,y,z) = self.atoms[i]
            y,z = y*cos(ax)-z*sin(ax),y*sin(ax)+z*cos(ax)
            self.atoms[i] = atno,(x,y,z)
            
        # rotate around y
        for i in range(self.nat):
            atno,(x,y,z) = self.atoms[i]
            x,z = x*cos(ay)-z*sin(ay),x*sin(ay)+z*cos(ay)
            self.atoms[i] = atno,(x,y,z)
            
        # rotate around z
        for i in range(self.nat):
            atno,(x,y,z) = self.atoms[i]
            x,y = x*cos(az)-y*sin(az),x*sin(az)+y*cos(az)
            self.atoms[i] = atno,(x,y,z)

        # Now update
        self.update()
        return
    

def read_xyz(filename):
    file = open(filename)
    atoms = []
    line = file.readline()
    nat = int(line.split()[0])
    line = file.readline()
    for i in range(nat):
        line = file.readline()
        words = line.split()
        atno = sym2no[words[0]]
        x,y,z = map(float,words[1:])
        atoms.append((atno,(x,y,z)))
    return atoms

def sort_by_z(atoms):
    "Sort the atoms by their z values"
    atoms.sort(cmp_z)

def cmp_z(a,b):
    "Function that compares the z values of 2 atoms"
    return cmp(a[1][2],b[1][2])

def get_bonds_from_distance(atoms):
    bonds = []
    for i in range(len(atoms)):
        atnoi,xyzi = atoms[i]
        for j in range(i):
            atnoj,xyzj = atoms[j]
            rij = dist(xyzi,xyzj)
            if rij < 1.6:
                bonds.append((i,j))
    return bonds

def dist(xyz1,xyz2):
    return sqrt(pow(xyz1[0]-xyz2[0],2)+pow(xyz1[1]-xyz2[1],2)\
                +pow(xyz1[2]-xyz2[2],2))

if __name__ == '__main__':
    import sys
    view = Viewer(sys.argv[1])
