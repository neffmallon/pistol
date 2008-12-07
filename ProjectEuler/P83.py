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

def get_data(read=True):
    if read:
        lines = open("p81_matrix.txt")
    else:
        lines = short_data.splitlines()
    data = []
    for line in lines:
        if read:
            data.append(map(int,line.split(",")))
        else:
            data.append(map(int,line.split()))
    return array(data)

def adjacent_unvisited(I,J,visited):
    N = visited.shape[0]
    points = []
    for k,l in [(I+1,J),(I-1,J),(I,J+1),(I,J-1)]:
        if k < 0 or k >= N or l < 0 or l >= N: continue
        if visited[k,l]: continue
        points.append((k,l))
    return points

def find_nearest_unvisited(dist,visited):
    N = dist.shape[0]
    candidates = []
    for k in range(N):
        for l in range(N):
            if not visited[k,l]:
                candidates.append((dist[k,l],k,l))
    candidates.sort()
    return candidates[0]

def find_nearest_neighbor(dist,points):
    candidates = [(dist[k,l],k,l) for k,l in points]
    candidates.sort()
    return candidates[0]

def main():
    data = get_data()
    N = data.shape[0]
    print data

    # Step 1
    dist = zeros(data.shape,int)
    visited = zeros(data.shape,bool) # Step 3: 0->False
    previ = zeros(data.shape,int)
    prevj = zeros(data.shape,int)
    I,J = 0,0 # Step 5

    # Step 2
    dist[:,:] = 10**9
    dist[0,0] = data[0,0]
    print dist

    print visited

    # Step 4
    previ[:,:] = -1
    prevj[:,:] = -1
    print previ
    print prevj

    newdist = 0
    while True:
        if I==N-1 and J==N-1: break
        print newdist,I,J
        visited[I,J] = True # Step 6
        points = adjacent_unvisited(I,J,visited)
        for k,l in points:
            if dist[I,J] + data[k,l] < dist[k,l]:
                dist[k,l] = dist[I,J] + data[k,l]
                previ[k,l] = I
                prevj[k,l] = J
        newdist,I,J = find_nearest_unvisited(dist,visited)
        #newdist,I,J = find_nearest_neighbor(dist,points)
    print newdist,dist[N-1,N-1]

    while True:
        if I==0 and J==0: break
        I,J = previ[I,J],prevj[I,J]
        print I,J


    return

if __name__ == '__main__':
    main()
