#!/usr/bin/env python
"""\

We shall define a square lamina to be a square outline with a square
'hole' so that the shape possesses vertical and horizontal symmetry.
For example, using exactly thirty-two square tiles we can form two
different square laminae:

  ######             
  ######
  ##  ##   (2,2)
  ##  ##
  ######
  ######

  #########
  #       #
  #       # (7,1)
  #       #
  #       #
  #       #
  #       #
  #       #
  #########


With one-hundred tiles, and not necessarily using all of the tiles at
one time, it is possible to form forty-one different square laminae.

Using up to one million tiles how many different square laminae can be
formed?

"""

from itertools import *

def gen_lessthan(n):
    n_4 = n//4
    for linewidth in xrange(1,n_4):
        hmax = n_4//linewidth - linewidth+1
        for holewidth in xrange(1,hmax):
            ntiles = linewidth*(linewidth+holewidth)
            if ntiles <= n_4:
                yield holewidth,linewidth,ntiles
    return

for i,v in enumerate(gen_lessthan(10**6)):
    if i % 100 == 0: print i+1
print i+1


# 10**2 41
# 10**3 703
# 10**4 9955




