#!/usr/bin/env python
"""\
The minimal path sum in the 5 by 5 matrix below, by starting in any
cell in the left column and finishing in any cell in the right column,
and only moving up, down, and right, is indicated in red; the sum is
equal to 994.

	
131	673	234	103	18
201	96	342	965	150
630	803	746	422	111
537	699	497	121	956
805	732	524	37	331
	

Find the minimal path sum, in matrix.txt (right click and 'Save
Link/Target As...'), a 31K text file containing a 80 by 80 matrix,
from the left column to the right column.
"""

short_data = """\
131	673	234	103	18
201	96	342	965	150
630	803	746	422	111
537	699	497	121	956
805	732	524	37	331"""

def get_data():
    from numpy import array
    lines = short_data.splitlines()
    #lines = open("p81_matrix.txt")
    data = []
    for line in lines:
        #data.append(map(int,line.split(",")))
        data.append(map(int,line.split()))
    return array(data)


def walk(data):
    n,m = data.shape
    for j in range(m):
        new = [None]*n
        for i in range(n):
            choices = []
            if i > 0:
                choices.append(data[i-1,j])
            if j > 0:
                choices.append(data[i,j-1])
            else:
                choices.append(0)
            if i < n-1:
                choices.append(data[i+1,j])
            if not choices: continue
            new[i] = data[i,j] + min(choices)
        data[:,j] = new
    print data
    return
    

def main():
    data = get_data()
    print data
    walk(data)
    return

if __name__ == '__main__': main()


