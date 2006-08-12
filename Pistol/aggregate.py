#!/usr/bin/env python
"Diffusion limited aggregation"

from math import sqrt,sin,cos,pi
from random import choice,random

steps = [(1,0),(-1,0),(0,1),(0,-1)]

def dla(npart=1000,rad0=10,radx=20):
    occupied = {(0,0):1} # just occupy the seed position
    killed = 0
    for ipart in range(npart):
        # pick random start position
        angle = 2*pi*random()
        x,y = int(rad0*cos(angle)),int(rad0*sin(angle))
        # perform the random walk
        while 1:
            sx,sy = choice(steps)
            x += sx
            y += sy
            r = sqrt(x*x+y*y)
            if r > radx:
                killed += 1
                break
            if neighbor_occupied(x,y,occupied):
                occupied[(x,y)] = 1
                break
    print "Out of %d particles, %d were killed and %d aggregated" % (
        npart,killed,len(occupied))
    pil_draw(radx,occupied)
    return

def pil_draw(radx,occupied):
    import Image, ImageDraw
    img = Image.new("RGB",(2*radx,2*radx),(255,255,255))
    draw = ImageDraw.Draw(img)

    for x,y in occupied.keys():
        draw.point((radx+x,radx+y),(0,0,0))
    img.save("bs.png","PNG")
    return

def neighbor_occupied(x,y,occupied):
    is_occupied = 0
    for neighbor in neighbors(x,y):
        if neighbor in occupied:
            is_occupied = 1
            break
    return is_occupied

def neighbors(x,y): 
    results = []
    for sx,sy in steps: results.append((x+sx,y+sy))
    return results

if __name__ == '__main__': dla()
