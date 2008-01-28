#!/usr/bin/env python
"""\
In the 5 by 5 matrix below, the minimal path sum from the top left to
the bottom right, by only moving to the right and down, is indicated
in red and is equal to 2427.

	
131	673	234	103	18
201	96	342	965	150
630	803	746	422	111
537	699	497	121	956
805	732	524	37	331
	

Find the minimal path sum, in matrix.txt (right click and 'Save
Link/Target As...'), a 31K text file containing a 80 by 80 matrix,
from the top left to the bottom right by only moving right and down.
"""

short_data = """\
131	673	234	103	18
201	96	342	965	150
630	803	746	422	111
537	699	497	121	956
805	732	524	37	331"""

def get_data():
    from numpy import array
    data = []
    for line in short_data.splitlines():
    #for line in open("p81_matrix.txt"):
        data.append(map(int,line.split()))
    return array(data)

def walk_diags(data):
    n,m = data.shape
    assert n==m
    ndiagonals = 2*n  # Number of diagonals in the matrix
    def nelem_diag(i): # i in range(0,2*n)
        if i < n: return i+1
        return 2*n-i

def main():
    data = get_data()
    print data
    return

if __name__ == '__main__': main()


