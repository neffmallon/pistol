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
    #lines = short_data.splitlines()
    lines = open("p81_matrix.txt")
    data = []
    for line in lines:
        data.append(map(int,line.split(",")))
        #data.append(map(int,line.split()))
    return array(data)

def walk(data):
    n,m = data.shape
    for col in range(1,m):
        new = [None]*n
        for row in range(n):
            # Find the minimum path from an element in column col-1
            #  to column col
            choices = []
            choices.append(data[row,col-1])
            for irow in range(0,row): # Go up:
                choices.append(data[irow,col-1]+sum(data[irow:row,col]))
            for irow in range(row+1,n): # Go down:
                choices.append(data[irow,col-1]+sum(data[(row+1):(irow+1),col]))
            #if row > 0:
            #    choices.append(data[row-1,col-1]+data[row-1,col])
            #if row < n-1:
            #    choices.append(data[row+1,col-1]+data[row+1,col])
            new[row] = data[row,col] + min(choices)
        data[:,col] = new
    if m < 10: print data
    print "Result = ",min(data[:,-1])
    return
    

def main():
    data = get_data()
    if data.shape[0] < 10: print data
    walk(data)
    return

if __name__ == '__main__': main()


