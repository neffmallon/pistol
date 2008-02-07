
def area(a,b): return b*sqrt(4*a*a-b*b)/4

def brute(plimit=1000):
    slimit = plimit/3+1
    sump = 0
    for a in xrange(2,slimit):
        for b in [a-1,a+1]:
            if area(a,b).is_integral():
                p = 2*a+b
                if p > plimit: continue
                sump += p
    print "sump for p < %d = %d" % (plimit,sump)
    return

            
