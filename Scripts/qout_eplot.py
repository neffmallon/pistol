#!/usr/bin/env python
"""\
 NAME
   qout_eplot.py - Display the energies from a Quest run

 USAGE
   qout_eplot.py <quest output file>

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

import sys
from Pistol.SeqQuest import read_output
import biggles

if len(sys.argv) < 2:
    print __doc__
    sys.exit()

results = read_output(sys.argv[1])
energies = results['energies']
g = biggles.FramedPlot()
d = biggles.Curve(range(len(energies)),energies,color='blue')
g.add(d)
g.title = 'Energies from Quest run'
g.xlabel = 'Step'
g.ylabel = 'Energy (Ry)'
g.show()


