#!/usr/bin/env python
"""\
 Mandelbrot and Frame's (Binary) Fractal Trees.
 See http://www.math.union.edu/research/fractaltrees/
"""

import os
from math import sin,cos,pi

def ftree(iter,origin,t,r,theta,dtheta):
    """\
    def ftree(iter,origin,t,r,theta,dtheta):

    Extend the binary fractal tree one iteration.
    iter:     The iteration number (we stop when iter == 0)
    origin:   The x,y coordinates of the start of this branch
    t:        The current trunk length
    r:        The amount to contract the trunk each iteration
    theta:    The current orientation
    dtheta:   The angle of the branch
    """
    if iter == 0: return []
    x0,y0 = origin
    x,y = x0+t*cos(theta),y0+t*sin(theta)
    lines = [((x0,y0),(x,y))]
    lines.extend(ftree(iter-1,(x,y),t*r,r,theta+dtheta,dtheta))
    lines.extend(ftree(iter-1,(x,y),t*r,r,theta-dtheta,dtheta))
    return lines

def ftree3(iter,origin,t,r,theta,dtheta):
    """\
    def ftree3(iter,origin,t,r,theta,dtheta):

    Extend the ternary fractal tree one iteration.
    iter:     The iteration number (we stop when iter == 0)
    origin:   The x,y coordinates of the start of this branch
    t:        The current trunk length
    r:        The amount to contract the trunk each iteration
    theta:    The current orientation
    dtheta:   The angle of the branch
    """
    if iter == 0: return []
    x0,y0 = origin
    x,y = x0+t*cos(theta),y0+t*sin(theta)
    lines = [((x0,y0),(x,y))]
    lines.extend(ftree3(iter-1,(x,y),t*r,r,theta+dtheta,dtheta))
    lines.extend(ftree3(iter-1,(x,y),t*r,r,theta,dtheta))
    lines.extend(ftree3(iter-1,(x,y),t*r,r,theta-dtheta,dtheta))
    return lines

def fern(iter,origin,t,r,theta,dtheta):
    if iter == 0: return []
    x0,y0 = origin
    x,y = x0+t*cos(theta),y0+t*sin(theta)
    xm,ym = x0+r*t*cos(theta),y0+r*t*sin(theta)
    lines = [((x0,y0),(x,y))]
    lines.extend(fern(iter-1,(xm,ym),t*r,r,theta+dtheta,dtheta))
    lines.extend(fern(iter-1,(x,y),t*r,r,theta,dtheta))
    lines.extend(fern(iter-1,(x,y),t*r,r,theta-dtheta,dtheta))
    return lines
    

def pil_render_lines(lines,height=300,width=300,fname="bs.png"):
    import Image,ImageDraw
    img = Image.new("RGB",(width,height),(255,255,255))
    draw = ImageDraw.Draw(img)
    for line in lines: draw.line(line,(0,0,0))
    img.save(fname,"PNG")
    os.system("display %s" % fname)
    return

def main():
    # Here we choose initial values. These work fairly well.
    # See ftree.__doc__ for details
    t = 60
    r = 0.75
    ang2rad = pi/180.
    theta = 90.0*ang2rad
    dtheta = 30.0*ang2rad
    #lines = ftree(8,(150,0),t,r,theta,dtheta)
    #lines = ftree3(8,(150,0),t,r,theta,dtheta)
    lines = fern(8,(150,0),t,r,theta,dtheta)
    pil_render_lines(lines)
    return

if __name__ == '__main__': main()
