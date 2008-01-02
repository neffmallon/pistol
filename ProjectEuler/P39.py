"""
If p is the perimeter of a right angle triangle with integral length sides, {a,b,c}, there are exactly three solutions for p = 120.

{20,48,52}, {24,45,51}, {30,40,50}

For which value of p 1000, is the number of solutions maximised?
"""

from math import sqrt

# Pythagorean triplets are in the form of (solution to prob 9):
# for m > n:
# a = 2mn, b = m^2-n^2, c = m^2+n^2

solns = {}
n = 400
for a in range(1,n):
    for b in range(1,a):
        c = sqrt(a*a+b*b)
        if int(c) < c: continue
        c = int(c)
        p = a+b+c
        if p > 1000: continue
        if p in solns:
            print "Multiple (%d) solutions for %d" % (len(solns[p])+1,p)
            solns[p].append((a,b,c))
        else:
            solns[p]= [(a,b,c)]

print solns
