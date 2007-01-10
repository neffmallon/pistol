#!/usr/bin/env python
"Conway's game of life"

from numpy import zeros,Int0
from random import randrange
import os

def init_lattice(height,width,init_occs=None):
    lattice = zeros((height,width),Int0)
    if init_occs:
        for x,y in init_occs: lattice[x,y] = 1
    else:
        for x in range(height):
            for y in range(width):
                lattice[x,y] = randrange(2)
    return lattice

def lives(is_alive,neighbors):
    if (is_alive and neighbors == 2) or neighbors == 3: return 1
    return 0

def life(height,width,nsteps=100):
    lattice = init_lattice(height,width)
    for step in range(nsteps):
        lattice = update(lattice,height,width)
    return

def update(lattice,height,width):
    for i in range(height):
        for j in range(width):
            im1 = (i-1)%height
            ip1 = (i+1)%height
            jm1 = (j-1)%width
            jp1 = (j+1)%width
            neighbors = lattice[im1,jm1] + lattice[im1,j] + lattice[im1,jp1] +\
                        lattice[ip1,jm1] + lattice[ip1,j] + lattice[ip1,jp1] +\
                        lattice[i,jm1] + lattice[i,jp1]
            lattice[i,j] = lives(lattice[i,j],neighbors)
    return lattice

def pil_image(lattice,fname="bs.png"):
    import Image, ImageDraw
    n,m = lattice.shape
    img = Image.new("RGB",(m,n),(255,255,255))
    draw = ImageDraw.Draw(img)

    for i in range(n):
        for j in range(m):
            if lattice[i,j] > 0: draw.point((i,j),(0,0,0))
    img.save(fname,"PNG")
    os.system('display %s' % fname)
    return

if __name__ == '__main__': life(100,100)
