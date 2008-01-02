"""
The cube, 41063625 (345^3), can be permuted to produce two other cubes:
56623104 (384^3) and 66430125 (405^3). In fact, 41063625 is the smallest
cube which has exactly three permutations of its digits which are also
cube.

Find the smallest cube for which exactly five permutations of its
digits are cube.
"""

from sets import Set
from Utils import permute

def strsort(s):
    l = list(s)
    l.sort()
    return "".join(l)

def stripl(s): return s.replace("L","")

nterms = 10000
cubes = [pow(i,3) for i in range(1,nterms+1)]
cubeset = Set(cubes)

cubedict = {}
for c in cubes:
    s = stripl(str(c))
    ss = strsort(s)
    if ss in cubedict:
        cubedict[ss].append(s)
    else:
        cubedict[ss] = [s]

for ss in cubedict:
    if len(cubedict[ss]) > 3:
        print cubedict[ss]

