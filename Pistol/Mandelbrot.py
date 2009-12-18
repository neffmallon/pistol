#!/usr/bin/env python
"""\
 Simple script to create Mandelbrot sets. From Dewdney's New Turning Omnibus.
"""

import os

def Mandelbrot(**kwargs):
    import Image,ImageDraw
    acorn = kwargs.get('acorn',-2.0)
    bcorn = kwargs.get('bcorn',-1.25)
    size = kwargs.get('size',2.5)
    width = kwargs.get('width',800)
    height = kwargs.get('height',800)
    iters = kwargs.get('iters',170)
    fname = kwargs.get('fname','mandelbrot.png')

    img = Image.new("RGB",(width,height),(255,255,255))
    draw = ImageDraw.Draw(img)
    for k in range(width):
        for l in range(height):
            ca = acorn + k*size/float(width)
            cb = bcorn + l*size/float(height)
            za = 0.
            zb = 0.
            for count in range(iters):
                za,zb = za*za - zb*zb + ca, 2*za*zb + cb
                if (za*za+zb*zb) > 4: break

            if count == iters-1:  color = (0,0,0)
            else:                 color = get_color(count)

            draw.point((k,l),fill=color)

    img.save(fname,'PNG')
    try:
        #os.system('display test.png')
        os.system('open %s' % fname)
    except:
        pass
    return

def get_color(a,cmin=0,cmax=100):
    # rewritten to use recipe 9.10 from the Python Cookbook
    import math
    try: a = float(a-cmin)/(cmax-cmin)
    except ZeroDivisionError: a=0.5 # cmax == cmin
    blue = min((max((4*(0.75-a),0.)),1.))
    red = min((max((4*(a-0.25),0.)),1.))
    green = min((max((4*math.fabs(a-0.5)-1.,0)),1.))
    return int(255*red),int(255*green),int(255*blue)

if __name__ == '__main__': Mandelbrot()
    

