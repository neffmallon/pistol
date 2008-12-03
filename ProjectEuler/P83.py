#!/usr/bin/env python
"""
In the 5 by 5 matrix below, the minimal path sum from the top left to
the bottom right, by moving left, right, up, and down, is indicated in
red and is equal to 2297.

	
131	673	234	103	18
201	96	342	965	150
630	803	746	422	111
537	699	497	121	956
805	732	524	37	331
	

Find the minimal path sum, in matrix.txt (right click and 'Save
Link/Target As...'), a 31K text file containing a 80 by 80 matrix,
from the top left to the bottom right by moving left, right, up, and
down.

--

Using Dijkstra's algorithm. From Wikpedia:
   1. Create a distance list, a previous vertex list, a visited list,
      and a current vertex. 
   2. All the values in the distance list are set to infinity except
      the starting vertex which is set to zero.
   3. All values in visited list are set to false.
   4. All values in the previous vertex list are set to a special value
      signifying that they are undefined, such as null.
   5. Current vertex is set as the starting vertex.
   6. Mark the current vertex as visited.
   7. Update distance and previous lists based on those vertices
      which can be immediately reached from the current vertex.
   8. Update the current vertex to the unvisited vertex that can be
      reached by the shortest path from the starting vertex.
   9. Repeat (from step 6) until all nodes are visited.

Or, using a street map, suppose you're marking over the streets
(tracing the street with a marker) in a certain order, until you have a
route marked in from the starting point to the destination. The
order is conceptually simple: from all the street intersections of the
already marked routes, find the closest unmarked intersection -
closest to the starting point (the"greedy" part). It's the whole marked
route to the intersection, plus the street to the new, unmarked
intersection. Mark that street to that intersection, draw an arrow
with the direction, then repeat. Never mark to any intersection twice.
When you get to the destination, follow the arrows backwards. There
will be only one path back against the arrows, the shortest one.
"""
from numpy import array,zeros

short_data = """\
131	673	234	103	18
201	96	342	965	150
630	803	746	422	111
537	699	497	121	956
805	732	524	37	331"""

def get_data():
    lines = short_data.splitlines()
    #lines = open("p81_matrix.txt")
    data = []
    for line in lines:
        #data.append(map(int,line.split(",")))
        data.append(map(int,line.split()))
    return array(data)

def tuple2ij(i,j,N):
    return i*N+j

def ij2tuple(ij,N):
    return ij/N,ij%N

def main():
    data = get_data()
    N = data.shape[0]
    print data
    dist = zeros(data.shape,int)
    dist[:,:] = 10**9
    dist[0,0] = 0
    print dist
    visited = zeros(data.shape,bool)
    print visited
    previ = zeros(data.shape,int)
    previ[:,:] = -1
    print previ
    prevj = zeros(data.shape,int)
    prevj[:,:] = -1
    print prevj
    current = 0,0
    while True:
        
    return

if __name__ == '__main__':
    main()
