#!/usr/bin/env python

import sys
from Pistol.XYZ import write
from Pistol.Tinker import read_tinker_xyzs

def convert(files):
    geos = read_tinker_xyzs(files)
    write('xmol.xyz',geos)
    return

if __name__ == '__main__':
    files = sys.argv[1:]
    files.sort()
    print files
    convert(files)
