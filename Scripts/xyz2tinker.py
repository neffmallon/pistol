#!/usr/bin/env python

"""
xyz2tinker Convert an xyz file to a tinker xyz format
"""

import string,sys,math
from Pistol.XYZ import read,root
from Pistol.Tinker import write_tinker_xyz

def convert(xyz_filename):
    geo = read(xyz_filename)[-1]
    if xyz_filename[-5:] == '.xmol':
        tinker_filename = xyz_filename[:-5] + '.xyz'
    elif xyz_filename[-4:] == '.xyz':
        tinker_filename = xyz_filename[:-4] + '_tink.xyz'
    else:
        tinker_filename = xyz_filename + '_tink.xyz'
    write_tinker_xyz(geo,tinker_filename)
    return


if __name__ == '__main__':
    xyz_filename = sys.argv[1]
    convert(xyz_filename)
