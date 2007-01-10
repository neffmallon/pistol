#!/usr/bin/env python
"""\
 Testing Konrad Hinsen's TkWidgets
"""

import sys

from Pistol.Element import color,radius
from Pistol.Util import distance
from Pistol.XYZ import read

from numpy import array
from Scientific.TkWidgets.TkVisualizationCanvas import *

def tkdrawer(filename):
    geos = read(filename,do_center=1)
    geo = geos[-1]
    nat = len(geo)
    objects = []
    for i in range(nat):
        atnoi,xyzi = geo[i]
        xi,yi,zi = xyzi
        for j in range(i):
            atnoj,xyzj = geo[j]
            xj,yj,zj = xyzj
            rij = distance(xyzi,xyzj)
            rij0 = 0.6*(radius[atnoi]+radius[atnoj])
            if 0.3 < rij < rij0:
                xm,ym,zm = (xi+xj)/2.,(yi+yj)/2.,(zi+zj)/2.
                objects.append(PolyLine3D(array([[xi,yi,zi],[xm,ym,zm]]),
                                          color='blue'))
                objects.append(PolyLine3D(array([[xj,yj,zj],[xm,ym,zm]]),
                                          color='red'))
    
    graphics = VisualizationGraphics(objects)

    window = Frame()
    window.pack(fill=BOTH, expand=YES)

    c = VisualizationCanvas(window, "100m", "100m", relief=SUNKEN, border=2)
    c.pack(side=TOP, fill=BOTH, expand=YES)
    c.draw(graphics)

    Button(window, text='Draw',
           command=lambda o=graphics: c.draw(o)).pack(side=LEFT)
    Button(window, text='Clear', command=c.clear).pack(side=LEFT)
    Button(window, text='Redraw', command=c.redraw).pack(side=LEFT)
    Button(window, text='Quit', command=window.quit).pack(side=RIGHT)

    window.mainloop()

if __name__ == '__main__':
    tkdrawer(sys.argv[1])
