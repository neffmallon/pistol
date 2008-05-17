from sets import Set
from numpy import array

test_network = """\
-	16	12	21	-	-	-
16	-	-	17	20	-	-
12	-	-	28	-	31	-
21	17	28	-	18	19	23
-	20	-	18	-	-	11
-	-	31	19	-	-	27
-	-	-	23	11	27	-\
"""

def tryint(s):
    try:
        i = int(s)
    except:
        i = 0
    return i

def parse_network():
    data = []
    for l in test_network.splitlines():
        data.append(map(tryint,l.split()))
    return array(data)

def parse_network2():
    data = []
    for l in open('network.txt'):
        data.append(map(tryint,l.split(',')))
    return array(data)

def glength(graph,distances):
    return sum(distances[i,j] for i,j in graph)
        
network = parse_network2()
N = network.shape[0]
print "Network with %d points" % N
graph = []
graph_points = Set()
all_points = Set(range(N))
BIG = 9999999
while 1:
    if len(graph_points) == N: break
    if not graph_points:
        totlength = 0
        minpair = None,None
        mindist = BIG
        for i in range(N):
            for j in range(i):
                totlength += network[i,j]
                if network[i,j]>0 and network[i,j] < mindist:
                    minpair = i,j
                    mindist = network[i,j]
        graph.append(minpair)
        graph_points.add(minpair[0])
        graph_points.add(minpair[1])
        print "Total length of the graph is ",totlength
    else:
        minpair = None,None
        mindist = BIG
        for i in graph_points:
            for j in (all_points - graph_points):
                if network[i,j] > 0 and network[i,j] < mindist:
                    minpair = i,j
                    mindist = network[i,j]
        graph.append(minpair)
        graph_points.add(minpair[1])
print graph
print glength(graph,network)
print "Savings of %d" % (totlength - glength(graph,network))


