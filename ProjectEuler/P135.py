"""Given the positive integers, x, y, and z, are consecutive terms of
an arithmetic progression, the least value of the positive integer, n,
for which the equation, x^(2) - y^(2) - z^(2) = n, has exactly two
solutions is n = 27:

34^(2) - 27^(2) - 20^(2) = 12^(2) - 9^(2) - 6^(2) = 27

It turns out that n = 1155 is the least value which has exactly ten solutions.

How many values of n less than one million have exactly ten distinct
solutions?"""


vals = {}

for i in xrange(1,100):
    for j in range(1,100):
        ip = i+1
        ipp = i+2
        val = pow(i+2*j,2)-pow(i+j,2)-pow(i,2)
        if val in vals:
            vals[val].append((i,j))
        else:
            vals[val] = [(i,j)]

for val in vals:
    if len(vals[val]) > 2:
        print val,len(vals[val]),vals[val]
            
