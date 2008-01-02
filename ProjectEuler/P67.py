"""
By starting at the top of the triangle below and moving to adjacent numbers on the row below, the maximum total from top to bottom is 23.

3
7 5
2 4 6
8 5 9 3

That is, 3 + 7 + 4 + 9 = 23.

Find the maximum total from top to bottom in triangle.txt (right click and 'Save Link/Target As...'), a 15K text file containing a triangle with one-hundred rows.
"""

from numpy import zeros

lines = open('triangle.txt').readlines()
N = len(lines)
print N

data = zeros((N,N),'i')
i = 0
for line in lines:
    ints = map(int,line.split())
    for j in range(len(ints)):
        data[i,j] = ints[j]
    i += 1

for i in range(N-2,-1,-1):
    for j in range(i+1):
        data[i,j] += max(data[i+1,j],data[i+1,j+1])
print "final answer is: ",data[0,0]
