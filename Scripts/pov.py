#!/usr/bin/env python
"""\
 pov.py - Wrapper around POVRay to render/view a .pov file

 Options:
 -h #   Use # as the height (default = 240)
 -w #   Use # as the width  (default = 320)
 -o     Use the old version of POVRay

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

import sys, os, getopt
from Pistol.POVRay import render,render_old,display

opts,args = getopt.getopt(sys.argv[1:],'oh:w:')

povray_prog = 'povray'
display_prog = 'display'
include_dir = "/usr/share/povray-3.5/include"

height=240
width=320
do_old = False

for key,val in opts:
    if key == '-h': height = int(val)
    if key == '-w': width = int(val)
    if key == '-o': do_old = True

for fname in args:
    print "Rendering ",fname
    if do_old:
        render_old(fname,povray_prog,include_dir,height,width)
    else:
        render(fname,povray_prog,include_dir,height,width)

    pngname = fname.replace('.pov','.png')
    display(pngname,display_prog)


    
