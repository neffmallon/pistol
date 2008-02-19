
from math import sqrt
from sets import Set
from Utils import issquare,isqrt
from itertools import count

nsqs = 10**5
sqs = Set(i*i for i in range(1,2*nsqs))
def issq(n):
    if n < nsqs: return n in sqs
    return issquare(n)

# Roots found thus far:
# b, h, l, #, sum(l)
# 16 15 17 1 17
# 272 273 305 2 322
# 4896 4895 5473 3 5795
# 87840 87841 98209 4 104004
# 1576240 1576239 1762289 5 1866293
# 28284464 28284465 31622993 6 33489286
# Spacings are 17, 18, then 17.941, 17.944444, 17.944266
# These converge to sqrt(322)


def brute():
    nfound = 0
    sumfound = 0
    for bh in count(int(17.944*28284464)):
        b = 2*bh
        for h in [b-1,b+1]:
            l2 = bh**2 + h**2
            if issq(l2):
                l = int(sqrt(l2))
                nfound += 1
                sumfound += l
                print b,h,l,nfound,sumfound
    print "Done"
    return

bvals = [16,272,4896,87840,1576240,28284464,
         507544128,9107509824,163427632720,
         2932589879120,52623190191456,944284833567072]
hvals = [15,273,4895,87841,1576239,28284465,
         507544127,9107509825,163427632719,
         2932589879121,52623190191455,944284833567073]
lvals = [17,305,5473,98209,1762289,31622993,
         567451585,10182505537,182717648081, # 9
         3278735159921,58834515230497,1055742538989025]
# Sum of these is 1118049290473931, doesn't work

def clever():
    for l in lvals[6:7]:
        l2 = l*l
        # need to find roots near
        # b**2 + (2b)**2 = l2
        # 5 b2 = l2
        # b \approx sqrt(l2/5)
        b0 = int(sqrt(l2/5.))-3
        for i in xrange(-10**2,10**6):
            bh = b0 + i
            b = 2*bh
            b2 = bh*bh
            for h in [b-1,b+1]:
                trial = b2+h*h
                if issq(trial):
                    l = isqrt(b2+h*h)
                    print b,h,l
    return

def test():
    print len(lvals),sum(lvals)
    for i,(b,h,l) in enumerate(zip(bvals,hvals,lvals)):
        bh = b/2
        val = l*l == bh*bh + h*h
        print i,val
        if not val:
            print "---------------------"
            print b,h,l
            print l*l
            print bh*bh + h*h
            print "---------------------"
            

if __name__ == '__main__':
    #clever()
    test()
