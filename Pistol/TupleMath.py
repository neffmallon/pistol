#!/usr/bin/env python
"""\
NAME
      TupleMath.py - Module to hold math functions with 3-tuples

DESCRIPTION
      Miscellaneous math functions for manipulating 3-tuples. These
      are very slow and are included for convenience only -- if speed is
      as issue you should probably use something else.
      
Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

import math

ex = (1.0,0,0)
ey = (0,1.0,0)
ez = (0,0,1.0)

def normalize(vec):
    L = length(vec)
    return (vec[0]/L,vec[1]/L,vec[2]/L)

def cross(vec1,vec2):
    return (vec1[1]*vec2[2]-vec1[2]*vec2[1],
            vec1[2]*vec2[0]-vec1[0]*vec2[2],
            vec1[0]*vec2[1]-vec1[1]*vec2[0])

def length(vec1): return math.sqrt(dot(vec1,vec1))
def dot(vec1,vec2): return vec1[0]*vec2[0]+vec1[1]*vec2[1]+vec1[2]*vec2[2]
def minus(vec1,vec2): return vec1[0]-vec2[0],vec1[1]-vec2[1],vec1[2]-vec2[2]
def plus(vec1,vec2): return vec1[0]+vec2[0],vec1[1]+vec2[1],vec1[2]+vec2[2]
def scale(amt,vec): return (amt*vec[0],amt*vec[1],amt*vec[2])
def midpoint(vec1,vec2): return scale(0.5,plus(vec1,vec2))


