"""
The product 7254 is unusual, as the identity, 39  186 = 7254, containing multiplicand, multiplier, and product is 1 through 9 pandigital.

Find the sum of all products whose multiplicand/multiplier/product identity can be written as a 1 through 9 pandigital.
"""

def num_to_digits(n): return map(int,str(n))

def isPandigitalProd(i,j):
    ijk = num_to_digits(i) + num_to_digits(j) + num_to_digits(i*j)
    ijk.sort()
    return ijk == [1,2,3,4,5,6,7,8,9]

psum = {}
for i in range(1,2000):
    for j in range(1,i):
        if isPandigitalProd(i,j):
            print i,j,i*j
            psum[i*j] = 1
print sum(psum.keys())

