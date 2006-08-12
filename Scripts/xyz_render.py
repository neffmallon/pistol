#!/usr/bin/env python
"""\
 This example shows how the simple BallStick module may be
 used to create a molecular renderer.

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

import sys
from Pistol.BallStickGtkGL import BSWindow
from Pistol.Element import color,radius
from Pistol.Util import distance
from Pistol.XYZ import read


for filename in sys.argv[1:]:
    geos = read(filename,do_center=1)
    geo = geos[-1]
    spheres = []
    for atno,(x,y,z) in geo:
        r,g,b = color[atno]
        rad = radius[atno]
        rad *= 0.25
        r /= 255.
        g /= 255.
        b /= 255.
        spheres.append(((x,y,z),rad,(r,g,b),20,20))

    cyls = []
    nat = len(geo)
    for i in range(nat):
        atno1,(x1,y1,z1) = geo[i]
        for j in range(i):
            atno2,(x2,y2,z2) = geo[j]
            r12 = distance((x1,y1,z1),(x2,y2,z2))
            r12o = 0.6*(radius[atno1]+radius[atno2])
            if 0.3 < r12 < r12o:
                cyls.append(((x1,y1,z1),(x2,y2,z2),0.15,20,(0.5,0.5,0.5)))
    bs = BSWindow(spheres,cyls)
    bs.run()

