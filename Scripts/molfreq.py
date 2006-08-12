#!/usr/bin/env python

"""
molfreq.py: Print Jaguar frequencies and normal modes in a format suitable
for viewing with Molden.

Usage:
  1. molfreq.py [Jaguar output file] > freq.molf
  2. molden freq.molf

Version History

0.1    01/01/00   Original version
0.2    03/01/00   Fixed bug related to intensities and symmetries
0.3    12/04/00   Fixed bug related to reduced masses.
0.4    08/22/02   Cleaned code slightly
0.5    06/06/03   Fixed a bug related to the force constant line
                  in Jaguar v4.2
0.6    06/09/03   Put most of the functions into the appropriate parts of Pistol

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

# Things to do:
#  Put the frequency stuff into the MOLF format in Pistol

import sys

for filename in sys.argv[1:]:
    from Pistol.Jaguar import read_output_as_dict
    from Pistol.MOLF import write

    output = read_output_as_dict(filename)
    mol = output['structure']
    freqlist = output['freqs']
    modes = output['modes']

    fileout = filename.replace('.out','.molf')
    write(fileout,mol,freqlist,modes)


