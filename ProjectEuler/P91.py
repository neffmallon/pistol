def signed_area(x1,y1,x2,y2,x3,y3):
    return (-x2*y1+x3*y1+x1*y2-x3*y2-x1*y3+x2*y3)/2

def orientation(x1,y1,x2,y2,x3,y3):
    if signed_area(x1,y1,x2,y2,x3,y3) > 0: return 1
    return -1

def points(nmax):
    r = range(0,nmax+1)
    for xi in r:
        for yi in r:
            if xi+yi == 0: continue
            yield xi,yi
    return

def brute(nmax=2):
    r = range(0,nmax+1)
    ntriangles = 0
    for xi in r:
        xi2 = xi*xi
        for xj in r:
            xj2 = xj*xj
            xij2 = pow(xi-xj,2)
            for yi in r:
                if xi == yi == 0: continue
                yi2 = yi*yi
                for yj in r:
                    if xj == yj == 0: continue
                    if xi == xj and yi == yj: continue
                    yj2 = yj*yj
                    yij2 = pow(yi-yj,2)
                    #print (xi,yi),(xj,yj)
                    l2 = xi2+yi2
                    m2 = xj2+yj2
                    n2 = xij2+yij2
                    lmn2 = [l2,m2,n2]
                    lmn2.sort()
                    c2 = lmn2[-1]
                    if c2 == sum(lmn2)/2 and orientation(0,0,xi,yi,xj,yj) == -1:
                    #if c2 == sum(lmn2)/2:
                        print (xi,yi),(xj,yj)
                        print orientation(0,0,xi,yi,xj,yj)
                        ntriangles += 1
    print "ntriangles = ",ntriangles
    return

def brute2(nmax=2):
    ntriangles = 0
    for xyi in points(nmax):
        xi2 = xyi[0]**2
        yi2 = xyi[1]**2
        for xyj in points(nmax):
            if xyi <= xyj: continue
            xj2 = xyj[0]**2
            yj2 = xyj[1]**2
            xij2 = pow(xyi[0]-xyj[0],2)
            yij2 = pow(xyi[1]-xyj[1],2)
            l2 = xi2+yi2
            m2 = xj2+yj2
            n2 = xij2+yij2
            lmn2 = [l2,m2,n2]
            lmn2.sort()
            c2 = lmn2[-1]
            if c2 == sum(lmn2)/2:
                print xyi,xyj
                ntriangles += 1
    print "ntriangles = ",ntriangles


if __name__ == '__main__': brute2(50)
