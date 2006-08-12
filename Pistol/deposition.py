#!/usr/bin/env python
"Ballistic deposition program"

from random import randint

steps = [(1,0),(-1,0),(0,1),(0,-1)]

def depos(npart=40000,height=400,width=400):
    is_occupied = {}
    for j in range(width): is_occupied[height-1,j] = 1

    for ipart in range(npart):
        j = randint(0,width-1)
        for i in range(height):
            if (i,j) in is_occupied: break
            if neighbor_occupied(i,j,is_occupied):
                is_occupied[i,j] = 1
                break
    pil_draw(is_occupied,height,width)
    return

def neighbor_occupied(i,j,is_occupied):
    occupied = 0
    for istep,jstep in steps:
        if (i+istep,j+jstep) in is_occupied:
            occupied = 1
            break
    return occupied

def pil_draw(is_occupied,height,width):
    import Image, ImageDraw
    img = Image.new("RGB",(width,height),(255,255,255))
    draw = ImageDraw.Draw(img)

    for i,j in is_occupied.keys():
        draw.point((j,i),(0,0,0))

    img.save("bs.png","PNG")
    return

if __name__ == '__main__': depos()
