"""
By starting at the top of the triangle below and moving to adjacent numbers on the row below, the maximum total from top to bottom is 23.

3
7 5
2 4 6
8 5 9 3

That is, 3 + 7 + 4 + 9 = 23.

Find the maximum total from top to bottom of the triangle below:

75
95 64
17 47 82
18 35 87 10
20 04 82 47 65
19 01 23 75 03 34
88 02 77 73 07 63 67
99 65 04 28 06 16 70 92
41 41 26 56 83 40 80 70 33
41 48 72 33 47 32 37 16 94 29
53 71 44 65 25 43 91 52 97 51 14
70 11 33 28 77 73 17 78 39 68 17 57
91 71 52 38 17 14 91 43 58 50 27 29 48
63 66 04 68 89 53 67 30 73 16 69 87 40 31
04 62 98 27 23 09 70 98 73 93 38 53 60 04 23
"""

from numpy import zeros
from copy import copy

datatxt = """\
75
95 64
17 47 82
18 35 87 10
20 04 82 47 65
19 01 23 75 03 34
88 02 77 73 07 63 67
99 65 04 28 06 16 70 92
41 41 26 56 83 40 80 70 33
41 48 72 33 47 32 37 16 94 29
53 71 44 65 25 43 91 52 97 51 14
70 11 33 28 77 73 17 78 39 68 17 57
91 71 52 38 17 14 91 43 58 50 27 29 48
63 66 04 68 89 53 67 30 73 16 69 87 40 31
04 62 98 27 23 09 70 98 73 93 38 53 60 04 23"""

datatxt2 = """3
7 5
2 4 6
8 5 9 3"""

N = len(datatxt.splitlines())

tuples = []

data = zeros((N,N),'i')
i = 0
for line in datatxt.splitlines():
    ints = map(int,line.split())
    for j in range(len(ints)):
        data[i,j] = ints[j]
    i += 1
#print data


def walk(i=0,j=0,stack=[]):
    stack.append(data[i,j])
    if i < N-1:
        walk(i+1,j,stack)
        stack.pop()
        walk(i+1,j+1,stack)
        stack.pop()
    else:
        tuples.append(copy(stack))
        
def method1():
    walk()

    maxtup = 0
    for tup in tuples:
        maxtup = max(maxtup,sum(tup))
    print maxtup

def method2():
    """Walk from the bottom to the top: the method suggested by
    user mather in the forum"""
    for i in range(13,-1,-1):
        for j in range(i+1):
            data[i,j] += max(data[i+1,j],data[i+1,j+1])
    print "final answer is: ",data[0,0]

if __name__ == '__main__': method2()




