#!/usr/bin/python
"""\
 Take a list of Jaguar log/out files as the argument and finds the final 
 energy (matching 'etot') in each one.

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

import sys,re

etotpat = re.compile('etot')

for filename in sys.argv[1:]:
    etot = ''

    file = open(filename,'r')
    root = re.sub('.out','',filename)
    root = re.sub('.log','',root)
    for line in file.readlines():
        if etotpat.search(line): etot = line.split()[6]

    # I put commas here so I can paste into spreadsheets
    print "%-20s %20s" % (root+',',etot)


