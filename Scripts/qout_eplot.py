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
from pylab import plot,title,xlabel,ylabel,show

if len(sys.argv) < 2:
    print __doc__
    sys.exit()

results = read_output(sys.argv[1])
energies = results['energies']
plot(energies,'b-')
title('Energies from Quest run')
xlabel('Step')
ylabel('Energy (Ry)')
show()


