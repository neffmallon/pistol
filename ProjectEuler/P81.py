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
    #lines = short_data.splitlines()
    lines = open("p81_matrix.txt")
    data = []
    for line in lines:
        data.append(map(int,line.split(",")))
    return array(data)

def diag(k,n):
    i = min(k,n-1)
    j = k-i
    yield i,j
    while True:
        i,j = i-1,j+1
        if i < 0 or j > n-1: break
        yield i,j
    return

def walk(data):
    n,m = data.shape
    assert n==m
    for k in range(2*n-1):
        for i,j in diag(k,n):
            choices = []
            if i > 0:
                choices.append(data[i-1,j])
            if j > 0:
                choices.append(data[i,j-1])
            if not choices: continue
            data[i,j] += min(choices)
    print data
    return
    

def main():
    data = get_data()
    print data
    walk(data)
    return

if __name__ == '__main__': main()


