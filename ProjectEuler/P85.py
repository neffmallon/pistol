from pprint import pprint

def gridways(nx,ny):
    totways = 0
    for x in range(1,nx+1):
        xways = nx-x+1
        for y in range(1,ny+1):
            yways = ny-y+1
            #print "For (%d,%d), there are %d ways to fit into [%d,%d]" %\
            #      (x,y,xways*yways,nx,ny)
            totways += xways*yways
    return totways

def main(nmax=100):
    results = []
    for i in range(1,nmax):
        for j in range(1,i+1):
            ways = gridways(i,j)
            results.append((abs(ways-2000000),i*j,i,j,ways))
    results.sort()
    pprint(results[:10])

if __name__ == '__main__': main()




