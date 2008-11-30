#!/usr/bin/env python
"""
Find the unique positive integer whose square has the form
1_2_3_4_5_6_7_8_9_0, where each “_” is a single digit.
"""
from math import sqrt
import re

imax = 1929394959697989990
imin = 1020304050607080900

pat = re.compile("1\d2\d3\d4\d5\d6\d7\d8\d9\d0")
istart = int(sqrt(imin))
iend = int(sqrt(imax))+1

print (istart,iend)
for i in xrange(istart,iend):
    if pat.math(str(i*i)): print i


