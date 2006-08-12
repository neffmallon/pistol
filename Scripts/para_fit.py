#!/usr/bin/env python
"""\
 para_fit.py - fit 3 points to a parabola and determine the minimum
 Usage: para_fit.py x1 y1 x2 y2 x3 y3

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

import sys
from Numeric import array
from LinearAlgebra import solve_linear_equations

DEBUG = 1

def para_fit((x1,y1),(x2,y2),(x3,y3)):
    a = array([[x1*x1,x1,1],
               [x2*x2,x2,1],
               [x3*x3,x3,1]])
    if DEBUG:
        print x1, y1
        print x2, y2
        print x3, y3
    b = array([y1,y2,y3])
    c = solve_linear_equations(a,b)
    ca,cb,cc = c
    print "Function fit to y = %f x^2 + %f x + %f" % (ca,cb,cc)
    print "Minimum at x = ",-0.5*cb/ca
    if DEBUG:
        print ca*x1*x1 + cb*x1 + cc - y1
        print ca*x2*x2 + cb*x2 + cc - y2
        print ca*x3*x3 + cb*x3 + cc - y3
    return

def test():
    para_fit((0,0.9),(1,1.33),(-1,0))

def main():
    if len(sys.argv) != 7:
        print __doc__
        sys.exit()
    x1,y1,x2,y2,x3,y3 = map(float,sys.argv[1:])
    para_fit((x1,y1),(x2,y2),(x3,y3))

if __name__ == '__main__':
    #main()
    x1 = 1.6
    #y1 = 12.249-5.9341      # 5.5
    y1 = -5.2021 + 13.1494  # 5.0
    #y1 = -76.7462 + 85.1592 # 4.5

    x2 = 1.59
    #y2 = 11.7612-5.9331     # 5.5
    y2 = -6.9896 + 13.4219  # 5.0
    #y2 = -81.8649 + 86.2381 # 4.5

    x3 = 1.58
    #y3 = 11.213 - 5.9241    # 5.5
    y3 = -8.8468 + 13.7162  # 5.0
    #y3 = -87.1466 + 87.3714 # 4.5

    para_fit((x1,y1),(x2,y2),(x3,y3))
    


